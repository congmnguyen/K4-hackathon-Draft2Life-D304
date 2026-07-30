# CiteGuard Tutor — prototype

Prototype này tái sử dụng pattern web local + API call của Draft2Life, nhưng thu
gọn đúng lát cắt hackathon: `chọn đoạn → hỏi → AI quyết định trả lời/hỏi
lại/từ chối → hiện căn cứ`.

## Chạy

```bash
export OPENAI_API_KEY="..."
export OPENAI_MODEL="o4-mini"  # mặc định; không tự fallback
python3 codebase/server.py --port 8000
```

Mở `http://127.0.0.1:8000`.

## Phần thật / phần mock

- Thật: OpenAI Responses API quyết định route và sinh câu trả lời có căn cứ.
- Thật: trace kỹ thuật không chứa API key được ghi vào `logs/ai_trace.jsonl`.
- Mock: người dùng nhập/paste đoạn nguồn và số trang; chưa nối retrieval VLearn.
- Không có fallback giả. Thiếu key/model/network sẽ hiện lỗi rõ.

## Kiểm thử

```bash
python3 -m unittest discover -s codebase -p 'test_*.py'
python3 scripts/run_eval.py --cases eval/golden-set.jsonl
```

Nguồn OpenAI contract: `POST /v1/responses`; model có thể override bằng
`OPENAI_MODEL`.
