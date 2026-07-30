#!/usr/bin/env python3
"""Dependency-free local web prototype adapted from Draft2Life's web flow.

The server intentionally keeps the hackathon slice small:
select source -> ask -> AI decides answer/clarify/refuse -> show evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from prompt import SYSTEM_PROMPT, build_input

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
TRACE_PATH = ROOT / "logs" / "ai_trace.jsonl"
OPENAI_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "o4-mini"
ALLOWED_ROUTES = {"answer", "clarify", "no_evidence", "out_of_scope"}


class AppError(RuntimeError):
    pass


def extract_output_text(payload: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                chunks.append(part["text"])
    if not chunks:
        raise AppError("OpenAI response không có output_text.")
    return "\n".join(chunks).strip()


def parse_model_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AppError("Model không trả JSON hợp lệ.") from exc
    if result.get("route") not in ALLOWED_ROUTES:
        raise AppError("Model trả route không hợp lệ.")
    for key in ("answer", "citation", "confidence", "evidence_used", "next_action"):
        if not isinstance(result.get(key), str):
            raise AppError(f"Model thiếu field chuỗi: {key}")
    if result["route"] == "answer" and not re.fullmatch(r"\[Trang \d+\]", result["citation"]):
        raise AppError("Câu trả lời route=answer nhưng thiếu citation đúng format.")
    if result["route"] != "answer":
        result["citation"] = ""
    return result


def append_trace(trace: dict[str, Any]) -> None:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRACE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(trace, ensure_ascii=False) + "\n")


def call_openai(page: int, excerpt: str, question: str, case_id: str = "interactive") -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise AppError("Thiếu OPENAI_API_KEY. Prototype không dùng mock ngầm.")
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    body = {
        "model": model,
        "instructions": SYSTEM_PROMPT.format(page=page),
        "input": build_input(page, excerpt, question),
        "max_output_tokens": 500,
        "store": False,
    }
    request = urllib.request.Request(
        OPENAI_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise AppError(f"OpenAI HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise AppError(f"Không gọi được OpenAI: {exc.reason}") from exc
    latency_ms = round((time.perf_counter() - started) * 1000)
    payload = json.loads(raw)
    result = parse_model_json(extract_output_text(payload))
    usage = payload.get("usage") or {}
    trace = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "case_id": case_id,
        "provider": "openai",
        "endpoint": "/v1/responses",
        "response_id": payload.get("id"),
        "model_requested": model,
        "model_returned": payload.get("model"),
        "status": payload.get("status"),
        "route": result["route"],
        "citation_present": bool(result["citation"]),
        "latency_ms": latency_ms,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "stored": False,
    }
    append_trace(trace)
    return {**result, "trace": trace}


def validate_request(payload: dict[str, Any]) -> tuple[int, str, str, str]:
    try:
        page = int(payload.get("page"))
    except (TypeError, ValueError) as exc:
        raise AppError("page phải là số nguyên dương.") from exc
    excerpt = str(payload.get("excerpt", "")).strip()
    question = str(payload.get("question", "")).strip()
    case_id = str(payload.get("case_id", "interactive"))[:80]
    if not 1 <= page <= 999:
        raise AppError("page phải nằm trong 1..999.")
    if not question:
        raise AppError("Câu hỏi không được để trống.")
    if len(excerpt) > 6000 or len(question) > 1000:
        raise AppError("Input vượt giới hạn prototype.")
    return page, excerpt, question, case_id


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/health":
            self._json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "model": os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
                    "api_key_configured": bool(os.environ.get("OPENAI_API_KEY")),
                },
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/ask":
            self._json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 16_000:
                raise AppError("Request quá lớn.")
            payload = json.loads(self.rfile.read(size) or b"{}")
            page, excerpt, question, case_id = validate_request(payload)
            result = call_openai(page, excerpt, question, case_id)
            self._json(HTTPStatus.OK, result)
        except (AppError, json.JSONDecodeError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception as exc:  # narrow prototype boundary
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Lỗi nội bộ: {exc}"})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[web] {self.address_string()} {fmt % args}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        f"CiteGuard running at http://{args.host}:{args.port} "
        f"model={os.environ.get('OPENAI_MODEL', DEFAULT_MODEL)}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
