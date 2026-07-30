#!/usr/bin/env python3
"""Reproducible, dependency-free mining for the CP1/CP4 evidence.

The raw hackathon data stays under data/ and is never copied into submission
artifacts. This script emits aggregate counts plus short, anonymized examples.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ACADEMIC = re.compile(
    r"giải thích|tóm tắt|tóm gọn|là gì|tại sao|vì sao|như thế nào|so sánh|"
    r"phân biệt|ví dụ|ý nghĩa|khái niệm|cơ chế|prompt|agent|llm|transformer|"
    r"token|attention|rag|embedding|fine[- ]?tune|machine learning|deep learning|ai\b",
    re.IGNORECASE,
)
REFUSAL = re.compile(
    r"không tìm thấy|ngoài phạm vi|không (?:có khả năng|thể)|"
    r"vui lòng (?:cung cấp|kiểm tra)|rất tiếc|xin lỗi",
    re.IGNORECASE,
)
OFF_TOPIC = re.compile(
    r"\b(?:hello|helo+|hi+|chào|đẹp trai|model của hãng|mấy giờ|link|deadline|nộp bài)\b",
    re.IGNORECASE,
)


def compact(text: str, limit: int) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def parse_citations(value: str) -> list[object]:
    try:
        parsed = json.loads(value or "[]")
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv"),
    )
    parser.add_argument("--output", type=Path, default=Path("evidence/mining-results.json"))
    args = parser.parse_args()

    with args.input.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    turns: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        turns[row["turn_id"]][row["role"]] = row

    tutors = [row for row in rows if row["role"] == "tutor"]
    uncited = [row for row in tutors if not parse_citations(row["citations"])]
    substantive: list[dict[str, str]] = []
    for turn_id, pair in turns.items():
        student = pair["student"]
        tutor = pair["tutor"]
        question = compact(student["content"], 10_000)
        answer = compact(tutor["content"], 10_000)
        if (
            not parse_citations(tutor["citations"])
            and len(answer) >= 180
            and ACADEMIC.search(question)
            and not REFUSAL.search(answer)
            and not OFF_TOPIC.search(question)
        ):
            substantive.append(
                {
                    "turn_id": turn_id,
                    "question_excerpt": compact(question, 180),
                    "answer_excerpt": compact(answer, 240),
                }
            )

    rating_table = Counter()
    for tutor in tutors:
        if not tutor["rating"]:
            continue
        key = ("cited" if parse_citations(tutor["citations"]) else "uncited", tutor["rating"])
        rating_table[key] += 1

    uncited_down = rating_table[("uncited", "down")]
    uncited_up = rating_table[("uncited", "up")]
    cited_down = rating_table[("cited", "down")]
    cited_up = rating_table[("cited", "up")]
    odds_ratio = (
        (uncited_down * cited_up) / (uncited_up * cited_down)
        if uncited_up and cited_down
        else None
    )

    result = {
        "source": str(args.input),
        "rows": len(rows),
        "turns": len(turns),
        "tutor_answers": len(tutors),
        "uncited_answers": len(uncited),
        "uncited_rate": round(len(uncited) / len(tutors), 4),
        "substantive_uncited_rule": (
            "citations=[] AND answer_length>=180 AND question_has_academic_keyword "
            "AND answer_is_not_refusal_or_redirect AND question_is_not_obvious_off_topic"
        ),
        "substantive_uncited_answers": len(substantive),
        "substantive_uncited_rate": round(len(substantive) / len(tutors), 4),
        "rating_sample_size": sum(rating_table.values()),
        "rating_table": {
            "uncited_down": uncited_down,
            "uncited_up": uncited_up,
            "cited_down": cited_down,
            "cited_up": cited_up,
        },
        "uncited_down_rate": round(uncited_down / (uncited_down + uncited_up), 4),
        "cited_down_rate": round(cited_down / (cited_down + cited_up), 4),
        "downvote_odds_ratio_uncited_vs_cited": round(odds_ratio, 3) if odds_ratio else None,
        "examples": substantive[:10],
        "limitations": [
            "Rating chỉ có ở một mẫu tự chọn rất nhỏ; tương quan không chứng minh quan hệ nhân quả.",
            "Rule substantive_uncited là heuristic có thể có false positive/false negative.",
            "citations=[] không tự động đồng nghĩa câu trả lời sai; đây là tín hiệu thiếu khả năng kiểm chứng.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"MINING_OK turns={result['turns']} uncited={result['uncited_answers']}/"
        f"{result['tutor_answers']} substantive_uncited={result['substantive_uncited_answers']} "
        f"rating_n={result['rating_sample_size']}"
    )


if __name__ == "__main__":
    main()
