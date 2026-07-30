"""Lời gọi AI thật + lớp chặn (guard) cho quyết định trung tâm.

Dùng chung bởi server.py (demo tương tác) và scripts/run_eval.py (chạy golden set),
để bộ đo và bản demo chạy đúng cùng một đường code.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from prompt import SYSTEM_PROMPT, build_input

ROOT = Path(__file__).resolve().parent
OPENAI_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4.1-mini"
TRACE_PATH = ROOT / "logs" / "ai_trace.jsonl"


def _load_dotenv() -> None:
    """Nạp biến từ file `.env` (codebase/.env hoặc .env ở gốc repo) vào os.environ.

    Không ghi đè biến đã set sẵn trong môi trường — `.env` chỉ là fallback tiện
    dùng cục bộ, biến môi trường thật (CI, shell) luôn thắng.
    """
    for candidate in (ROOT / ".env", ROOT.parent / ".env"):
        if not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
        break


_load_dotenv()

ROUTES = {"apply", "clarify", "no_evidence", "out_of_scope"}
ELEMENTS = {"cua_so", "cua_di", "tuong"}
SIDES = {"N", "E", "S", "W"}

# Map từ chữ chỉ hướng sang mã. Thứ tự quan trọng: khớp cụm dài trước.
SIDE_WORDS = {
    "đông bắc": "N", "đông nam": "S", "tây bắc": "N", "tây nam": "S",
    "bắc": "N", "north": "N",
    "nam": "S", "south": "S",
    "đông": "E", "east": "E",
    "tây": "W", "west": "W",
}

# Khoảng kích thước hợp lệ theo từng loại phần tử (mét). Lấy theo thực tế thi công
# dân dụng: cửa đi hẹp hơn 0,6m thì người không đi lọt; cửa sổ rộng quá 4m thì
# không còn là cửa sổ. Guard chặn ở đây để số phi lý không lọt vào hồ sơ xuất ra.
WIDTH_RANGE_M = {
    "cua_di": (0.6, 3.0),
    "cua_so": (0.4, 4.0),
    "tuong": (0.5, 8.0),
}


class AppError(RuntimeError):
    """Lỗi hiển thị được cho người dùng. Prototype không có fallback giả."""


def _extract_text(payload: dict[str, Any]) -> str:
    chunks = [
        part["text"]
        for item in payload.get("output", [])
        if item.get("type") == "message"
        for part in item.get("content", [])
        if part.get("type") == "output_text" and isinstance(part.get("text"), str)
    ]
    if not chunks:
        raise AppError("OpenAI không trả về output_text.")
    return "\n".join(chunks).strip()


def _parse_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AppError("Model không trả JSON hợp lệ.") from exc
    if not isinstance(result, dict):
        raise AppError("Model trả JSON nhưng không phải object.")
    return result


def guard(result: dict[str, Any], plan: dict) -> list[str]:
    """Kiểm tra deterministic sau khi model trả lời.

    Trả về danh sách vi phạm. Danh sách rỗng = model tuân thủ hợp đồng.
    Đây là lớp chặn lớp ① (bịa nguồn) và ④ (sai tham số domain) — không tin
    model tự giác, kiểm lại bằng code.
    """
    violations: list[str] = []
    route = result.get("route")
    if route not in ROUTES:
        return [f"route không hợp lệ: {route!r}"]

    target = result.get("target") or {}
    if not isinstance(target, dict):
        return ["target không phải object"]

    room_ids = {room["id"] for room in plan["rooms"]}
    room_id = target.get("room_id")
    # Chỉ tính là "bịa phòng" khi model đang nhận phòng đó là mục tiêu để dựng
    # hoặc để hỏi tiếp. Ở route no_evidence, gọi tên đúng cái phòng KHÔNG tồn tại
    # chính là nội dung câu trả lời — chặn ở đó là chặn nhầm.
    if route in {"apply", "clarify"} and room_id is not None and room_id not in room_ids:
        violations.append(f"bịa phòng không có trên mặt bằng: {room_id!r}")

    # Lớp ④: đối chiếu side với cụm chữ model tự trích. Model có thể đọc "nam"
    # (south) thành N vì nhìn giống "north" — guard bắt bằng code, không tin model.
    source = str(target.get("side_source") or "").lower()
    if source and target.get("side") in SIDES:
        derived = next((v for k, v in SIDE_WORDS.items() if k in source), None)
        if derived and derived != target["side"]:
            violations.append(
                f"side {target['side']!r} không khớp cụm chữ {target['side_source']!r} "
                f"(phải là {derived!r})"
            )

    if route == "apply":
        element = target.get("element")
        if element not in ELEMENTS:
            violations.append(f"element không hợp lệ: {element!r}")
        if room_id is None:
            violations.append("apply nhưng thiếu room_id")
        if target.get("side") not in SIDES:
            violations.append(f"side không hợp lệ: {target.get('side')!r}")
        width = target.get("width_m")
        if not isinstance(width, (int, float)):
            violations.append("apply nhưng thiếu width_m")
        elif element in WIDTH_RANGE_M:
            low, high = WIDTH_RANGE_M[element]
            if not low <= float(width) <= high:
                violations.append(
                    f"width_m {width}m ngoài khoảng hợp lệ của {element} ({low}-{high}m)"
                )

    if route == "clarify" and not str(result.get("question") or "").strip():
        violations.append("clarify nhưng không có câu hỏi lại")

    if route in {"no_evidence", "out_of_scope"} and not str(result.get("reason") or "").strip():
        violations.append(f"{route} nhưng không có lý do")

    return violations


def append_trace(trace: dict[str, Any]) -> None:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRACE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(trace, ensure_ascii=False) + "\n")


def decide(plan: dict, text: str, case_id: str = "interactive") -> dict[str, Any]:
    """Gọi OpenAI thật, parse, guard, ghi trace. Không có mock ngầm."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise AppError("Thiếu biến môi trường OPENAI_API_KEY.")
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)

    body = json.dumps(
        {
            "model": model,
            "instructions": SYSTEM_PROMPT,
            "input": build_input(plan, text),
            "max_output_tokens": 700,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_URL,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )

    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise AppError(f"OpenAI HTTP {exc.code}: {exc.read().decode()[:200]}") from exc
    except urllib.error.URLError as exc:
        raise AppError(f"Không gọi được OpenAI: {exc.reason}") from exc
    latency_ms = int((time.time() - started) * 1000)

    raw = _extract_text(payload)
    result = _parse_json(raw)
    violations = guard(result, plan)

    result["_meta"] = {
        "model": model,
        "latency_ms": latency_ms,
        "violations": violations,
        "blocked": bool(violations),
    }

    append_trace(
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "case_id": case_id,
            "model": model,
            "plan": plan["name"],
            "input": text,
            "raw_output": raw,
            "route": result.get("route"),
            "violations": violations,
            "latency_ms": latency_ms,
            "usage": payload.get("usage", {}),
        }
    )
    return result
