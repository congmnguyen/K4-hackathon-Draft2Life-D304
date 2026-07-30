import json
import unittest

from server import AppError, extract_output_text, parse_model_json, validate_request


class ServerTest(unittest.TestCase):
    def test_extract_output_text(self):
        payload = {
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": '{"route":"answer"}'}],
                }
            ]
        }
        self.assertEqual(extract_output_text(payload), '{"route":"answer"}')

    def test_parse_answer_requires_citation(self):
        with self.assertRaises(AppError):
            parse_model_json(
                json.dumps(
                    {
                        "route": "answer",
                        "answer": "x",
                        "citation": "",
                        "confidence": "high",
                        "evidence_used": "x",
                        "next_action": "x",
                    }
                )
            )

    def test_non_answer_citation_is_removed(self):
        result = parse_model_json(
            json.dumps(
                {
                    "route": "clarify",
                    "answer": "Cần thêm dữ liệu.",
                    "citation": "[Trang 2]",
                    "confidence": "low",
                    "evidence_used": "",
                    "next_action": "Chọn thêm đoạn.",
                }
            )
        )
        self.assertEqual(result["citation"], "")

    def test_validate_request(self):
        self.assertEqual(
            validate_request({"page": 7, "excerpt": "Nguồn", "question": "Giải thích?"}),
            (7, "Nguồn", "Giải thích?", "interactive"),
        )

    def test_validate_rejects_empty_question(self):
        with self.assertRaises(AppError):
            validate_request({"page": 1, "excerpt": "x", "question": " "})


if __name__ == "__main__":
    unittest.main()
