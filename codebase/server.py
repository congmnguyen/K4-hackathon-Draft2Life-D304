#!/usr/bin/env python3
"""Server local cho prototype Draft2Life — không phụ thuộc thư viện ngoài.

    export OPENAI_API_KEY="..."
    python3 codebase/server.py --port 8000

Mở http://127.0.0.1:8000. API key chỉ ở biến môi trường, không bao giờ xuống browser.
"""

from __future__ import annotations

import argparse
import json
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from decide import AppError, decide  # noqa: E402

MAX_BODY = 32 * 1024


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):  # bớt ồn
        if "/api/" in (self.path or ""):
            super().log_message(fmt, *args)

    def _send_json(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/decide":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Không có endpoint này."})
            return

        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Body rỗng hoặc quá lớn."})
            return

        try:
            request = json.loads(self.rfile.read(length))
            plan, text = request["plan"], request["text"]
            if not isinstance(plan, dict) or not plan.get("rooms"):
                raise ValueError("plan không hợp lệ")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("text rỗng")
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": f"Request không hợp lệ: {exc}"})
            return

        try:
            self._send_json(HTTPStatus.OK, decide(plan, text))
        except AppError as exc:
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": str(exc)})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Draft2Life prototype: http://127.0.0.1:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
