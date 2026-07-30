#!/usr/bin/env python3
"""Phân tích khảo sát Draft2Life → số liệu Đường A cho spec §1.

PII (họ tên / email / SĐT) KHÔNG bao giờ được ghi ra file output. File nguồn nằm
ngoài repo và không được commit; chỉ số tổng hợp + trích dẫn đã ẩn danh đi vào
evidence/.

    python3 scripts/analyze_survey.py --input "<đường dẫn CSV>"
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

PII_COLUMNS = ("Họ và tên", "Email", "Số điện thoại")


def tally(rows: list[dict], column: str, multi: bool = False) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        raw = (row.get(column) or "").strip()
        values = [v.strip() for v in raw.split(";")] if multi else [raw]
        for value in values:
            if value:
                counter[value] += 1
    return dict(counter.most_common())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("evidence/survey-results.json"))
    args = parser.parse_args()

    with args.input.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    columns = list(rows[0].keys())
    q_role, q_tool, q_time = columns[1], columns[2], columns[3]
    q_blocker, q_edit, q_ai = columns[4], columns[5], columns[7]
    q_demo, q_exports = columns[10], columns[14]

    total = len(rows)
    edits_often = sum(1 for r in rows if r[q_edit].strip() == "Có")
    ready_ai = sum(1 for r in rows if r[q_ai].strip() == "Có")
    wants_demo = sum(1 for r in rows if r[q_demo].strip() == "Có")
    slow_build = sum(
        1 for r in rows if r[q_time].startswith(("3 – 7", "Trên 1 tuần"))
    )

    by_role = {}
    for role in sorted({r[q_role].strip() for r in rows if r[q_role].strip()}):
        subset = [r for r in rows if r[q_role].strip() == role]
        by_role[role] = {
            "n": len(subset),
            "sua_nhieu_lan": sum(1 for r in subset if r[q_edit].strip() == "Có"),
            "san_sang_dung_ai": sum(1 for r in subset if r[q_ai].strip() == "Có"),
            "muon_thu_demo": sum(1 for r in subset if r[q_demo].strip() == "Có"),
        }

    result = {
        "phuong_phap": (
            "Google Form phát cho sinh viên kiến trúc/xây dựng và KTS đang đi làm, "
            "ngoài nhóm. Mỗi dòng = 1 người trả lời. Đếm trực tiếp trên cột lựa chọn, "
            "không suy diễn; câu multi-select tách theo dấu ';'."
        ),
        "n_nguoi_tra_loi": total,
        "chi_so_chinh": {
            "phai_sua_chi_tiet_nhieu_lan": edits_often,
            "phai_sua_chi_tiet_nhieu_lan_pct": round(edits_often / total * 100, 1),
            "san_sang_dung_ai_2d_3d": ready_ai,
            "san_sang_dung_ai_2d_3d_pct": round(ready_ai / total * 100, 1),
            "muon_thu_demo": wants_demo,
            "muon_thu_demo_pct": round(wants_demo / total * 100, 1),
            "dung_3d_tu_3_ngay_tro_len": slow_build,
            "dung_3d_tu_3_ngay_tro_len_pct": round(slow_build / total * 100, 1),
        },
        "theo_vai": by_role,
        "phan_bo": {
            "vai_tro": tally(rows, q_role),
            "phan_mem_dang_dung": tally(rows, q_tool, multi=True),
            "thoi_gian_dung_3d": tally(rows, q_time),
            "kho_khan_lon_nhat": tally(rows, q_blocker, multi=True),
            "so_mo_hinh_xuat_moi_thang": tally(rows, q_exports),
        },
        "pii": "Cột họ tên/email/SĐT có trong file nguồn và đã bị loại khỏi output này.",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Log đầy đủ theo chuẩn Đường A: mọi câu hỏi + từng câu trả lời nguyên văn.
    # Người trả lời được thay bằng mã R001..R123; 3 cột PII bị loại hoàn toàn.
    asked = [c for c in columns if c not in PII_COLUMNS and c != "Timestamp"]
    log_lines = [
        "# Log khảo sát Đường A — nguyên văn, đã ẩn danh",
        "",
        f"- n = {total} người ngoài nhóm · {len(asked)} câu hỏi",
        "- Sinh tự động bởi `scripts/analyze_survey.py`. File nguồn chứa họ tên/email/SĐT,",
        "  **không nằm trong repo**; ba cột đó bị loại khỏi log này.",
        "- Câu multi-select giữ nguyên dấu `;` như người trả lời chọn.",
        "",
        "## Bộ câu hỏi đã hỏi",
        "",
    ]
    log_lines += [f"{i}. {q}" for i, q in enumerate(asked, 1)]
    log_lines += ["", "## Từng câu trả lời nguyên văn", ""]
    for index, row in enumerate(rows, 1):
        log_lines.append(f"### R{index:03d}")
        log_lines.append("")
        for number, question in enumerate(asked, 1):
            answer = (row.get(question) or "").strip() or "(bỏ trống)"
            log_lines.append(f"{number}. {answer}")
        log_lines.append("")

    log_path = args.output.with_name("survey-log.md")
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    for path in (args.output, log_path):
        text = path.read_text(encoding="utf-8")
        for column in PII_COLUMNS:
            assert column not in text, f"PII leak ({column}) trong {path}"
        for row in rows:
            for column in PII_COLUMNS:
                value = (row.get(column) or "").strip()
                assert not (len(value) > 4 and value in text), f"PII leak giá trị trong {path}"

    print(
        f"SURVEY_OK n={total} sua_nhieu_lan={edits_often} "
        f"san_sang_ai={ready_ai} muon_demo={wants_demo} log={log_path}"
    )


if __name__ == "__main__":
    main()
