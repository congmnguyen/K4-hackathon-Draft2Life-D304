#!/usr/bin/env python3
"""Chạy trọn bộ golden set qua đúng đường code của bản demo.

    export OPENAI_API_KEY="..."
    python3 scripts/run_eval.py --out eval/run-01.md

Ghi ra bảng đủ MỌI case kể cả case fail. Không sửa số, không giấu case.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "codebase"))

from decide import DEFAULT_MODEL, AppError, decide  # noqa: E402

# Mặt bằng phải khớp hằng số PLANS trong codebase/index.html
PLANS = {
    "A": {
        "name": "Căn hộ 48 m² — hiện trạng",
        "rooms": [
            {"id": "khach", "label": "Phòng khách", "w": 5, "h": 6},
            {"id": "ngu", "label": "Phòng ngủ", "w": 3, "h": 3.5},
            {"id": "wc", "label": "WC", "w": 3, "h": 2.5},
        ],
    },
    "B": {
        "name": "Văn phòng nhỏ 48 m² — hiện trạng",
        "rooms": [
            {"id": "lam", "label": "Khu làm việc", "w": 5, "h": 6},
            {"id": "hop", "label": "Phòng họp", "w": 3, "h": 3.5},
            {"id": "kho", "label": "Kho hồ sơ", "w": 3, "h": 2.5},
        ],
    },
}

LOP_LABEL = {
    "thuong": "thường",
    "hiem": "hiếm",
    "1_nguon_su_that": "① nguồn sự thật",
    "2_mo_ho": "② mơ hồ",
    "3_ngoai_tham_quyen": "③ ngoài thẩm quyền",
    "4_dac_thu_domain": "④ đặc thù domain",
}


def score(case: dict, result: dict | None, error: str | None) -> dict:
    """Ba chiều chất lượng, mỗi chiều pass/fail độc lập.

    D1 route đúng      — route trả về khớp expect_route.
    D2 không bịa nguồn — không có vi phạm "bịa phòng" trong guard.
    D3 tham số đúng    — apply thì target khớp expect_target; guard chặn đúng
                         chỗ đáng chặn (expect_guard_block).
    Case đạt = cả 3 chiều pass.
    """
    if error is not None:
        return {"d1": False, "d2": False, "d3": False, "dat": False, "note": f"LỖI: {error}"}

    route = result.get("route")
    meta = result.get("_meta", {})
    violations = meta.get("violations", [])
    target = result.get("target") or {}

    d1 = route == case["expect_route"]
    d2 = not any("bịa phòng" in v for v in violations)

    d3, notes = True, []
    if case.get("expect_guard_block"):
        d3 = bool(violations)
        if not d3:
            notes.append("guard KHÔNG chặn case đáng chặn")
    elif case["expect_route"] == "apply" and "expect_target" in case:
        for key, want in case["expect_target"].items():
            got = target.get(key)
            ok = abs(float(got) - float(want)) < 0.01 if key == "width_m" and isinstance(
                got, (int, float)
            ) else got == want
            if not ok:
                d3 = False
                notes.append(f"{key}: chờ {want!r} nhận {got!r}")
    elif case["expect_route"] == "clarify":
        if violations:
            d3 = False
            notes.append("guard bắt lỗi: " + " | ".join(violations))
        if "expect_missing" in case and result.get("missing") != case["expect_missing"]:
            notes.append(f"missing: chờ {case['expect_missing']!r} nhận {result.get('missing')!r} (không trừ điểm)")
    elif violations:
        d3 = False
        notes.append("guard bắt lỗi: " + " | ".join(violations))

    if not d1:
        notes.insert(0, f"route: chờ {case['expect_route']} nhận {route}")

    return {"d1": d1, "d2": d2, "d3": d3, "dat": d1 and d2 and d3, "note": " · ".join(notes) or "—"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=ROOT / "eval/golden-set.jsonl")
    parser.add_argument("--out", type=Path, default=ROOT / "eval/run-01.md")
    args = parser.parse_args()

    cases = [json.loads(line) for line in args.cases.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = []

    for case in cases:
        plan = PLANS[case["plan"]]
        result, error = None, None
        try:
            result = decide(plan, case["input"] or "(rỗng)", case_id=case["id"])
        except AppError as exc:
            error = str(exc)
        verdict = score(case, result, error)
        rows.append((case, result, verdict))
        flag = "✅" if verdict["dat"] else "❌"
        print(f"{flag} {case['id']:7s} {case['expect_route']:13s} -> "
              f"{(result or {}).get('route', 'LỖI'):13s} {verdict['note'][:70]}")

    total = len(rows)
    passed = sum(1 for _, _, v in rows if v["dat"])
    d2_fail = [c["id"] for c, _, v in rows if not v["d2"]]

    by_lop: dict[str, list[bool]] = {}
    for case, _, verdict in rows:
        by_lop.setdefault(case["lop"], []).append(verdict["dat"])

    lines = [
        "# eval lượt 1 — golden set",
        "",
        f"- Chạy lúc: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        f"- Model: `{DEFAULT_MODEL}` (OpenAI Responses API), lời gọi thật, trace ở `codebase/logs/ai_trace.jsonl`",
        f"- Bộ case: `{args.cases.relative_to(ROOT)}` — {total} case",
        "",
        "## Ba chiều chất lượng (định nghĩa kiểm chứng được)",
        "",
        "| Chiều | Đạt khi |",
        "|---|---|",
        "| D1 · Route đúng | Route trả về khớp route mong đợi của case |",
        "| D2 · Không bịa nguồn | Không xuất hiện `room_id` nằm ngoài mặt bằng đang mở |",
        "| D3 · Tham số đúng | `apply` thì 4 tham số khớp; case đáng chặn thì guard có chặn |",
        "",
        "**Case đạt = pass cả 3 chiều.**",
        "",
        "## Kết quả tổng",
        "",
        f"- **{passed}/{total} case đạt = {passed / total * 100:.1f}%**",
        f"- D2 (không bịa nguồn): **{total - len(d2_fail)}/{total}**"
        + (f" — fail ở: {', '.join(d2_fail)}" if d2_fail else " — không case nào bịa phòng"),
        "",
        "| Lớp | Đạt / Tổng |",
        "|---|---|",
    ]
    for lop, results in by_lop.items():
        lines.append(f"| {LOP_LABEL.get(lop, lop)} | {sum(results)}/{len(results)} |")

    lines += ["", "## Bảng đầy đủ — mọi case, kể cả case chưa đạt", "",
              "| # | Lớp | Input | Chờ | Nhận | D1 | D2 | D3 | Đạt | Ghi chú |",
              "|---|---|---|---|---|:--:|:--:|:--:|:--:|---|"]
    tick = lambda ok: "✅" if ok else "❌"  # noqa: E731
    for case, result, verdict in rows:
        got = (result or {}).get("route", "LỖI")
        text = (case["input"] or "(rỗng)").replace("|", "\\|")
        lines.append(
            f"| {case['id']} | {LOP_LABEL.get(case['lop'], case['lop'])} | {text} | "
            f"{case['expect_route']} | {got} | {tick(verdict['d1'])} | {tick(verdict['d2'])} | "
            f"{tick(verdict['d3'])} | {tick(verdict['dat'])} | {verdict['note'].replace('|', '\\|')} |"
        )

    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n{passed}/{total} = {passed / total * 100:.1f}%  →  {args.out}")


if __name__ == "__main__":
    main()
