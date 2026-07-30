# Draft2Life — prototype

**Mức prototype khai báo: `Mock`** — flow bấm được, mặt bằng dựng sẵn,
**AI thật ở quyết định trung tâm**.

## Chạy

```bash
export OPENAI_API_KEY="..."        # key chỉ ở biến môi trường, không bao giờ xuống browser
python3 codebase/server.py --port 8000
```

Mở http://127.0.0.1:8000. Không cần cài thư viện ngoài (chỉ stdlib Python).
Model mặc định `gpt-4.1-mini`, đổi bằng `OPENAI_MODEL`.

## Lát cắt đang build

> Sinh viên kiến trúc đang có mô hình 3D dựng từ mặt bằng 2D · gõ một câu tiếng Việt mô tả
> chi tiết muốn sửa · **AI quyết định câu đó đã đủ tham số để thực thi hay còn thiếu** ·
> trả về mô hình đã cập nhật kèm thông số, hoặc đúng một câu hỏi làm rõ.

## Flow bấm được (4 bước)

1. Chọn mặt bằng (2 mặt bằng dựng sẵn)
2. Xem hiện trạng — mặt bằng 2D + khối 3D isometric, render từ cùng một model dữ liệu
3. Gõ câu sửa (hoặc bấm 1 trong 4 câu mẫu)
4. Xem quyết định + khối 3D sau thay đổi + nhật ký

## 4 đường đi trải nghiệm — bấm được hết ngay ở CP2

| Đường đi | Câu mẫu | Hành vi |
|---|---|---|
| **Happy** | "Thêm một cửa sổ rộng 1m2 ở tường phía tây phòng khách" | Dựng luôn, hiện bảng thông số + cảnh báo kiểm lại trước khi xuất hồ sơ |
| **Low-confidence** (lớp ②) | "thêm cửa sổ" | Hỏi lại đúng **một** câu về tham số thiếu, kèm 4 nút chọn nhanh. Không tự đoán |
| **Failure / không có căn cứ** (lớp ①) | "mở rộng phòng bếp thêm 2m" | Mặt bằng không có phòng bếp → **không dựng**, liệt kê phòng đang có |
| **Correction** | nút *Hoàn tác* / *Không phải ý tôi →* | Gỡ thay đổi cuối, ghi vào nhật ký, quay lại ô nhập |
| **Ngoài thẩm quyền** (lớp ③) | "bức tường giữa nhà đập được không?" | Từ chối rõ, vẫn đưa việc làm được: xuất bản vẽ hiện trạng để mang đi hỏi kỹ sư |

## Phần nào thật / phần nào mock

| | Trạng thái |
|---|---|
| Flow 4 bước, điều hướng, hoàn tác, nhật ký | **Thật** |
| Render mặt bằng 2D + khối 3D isometric (SVG, chiếu iso trong `draw3d()`) | **Thật** — vẽ từ model dữ liệu, thay đổi hiện ra ngay |
| Quyết định route + rút tham số | **THẬT** — 1 lời gọi OpenAI Responses API mỗi lần bấm "Dựng thử". Prompt: `prompt.py`, lời gọi: `decide.py`. Trace đầy đủ ở `logs/ai_trace.jsonl` |
| Guard sau lời gọi AI | **THẬT** — `decide.py:guard()` kiểm bằng code: phòng có trên mặt bằng không, kích thước có nằm trong khoảng hợp lệ của loại phần tử không. Vi phạm → **không dựng gì**, hiện lý do |
| Upload bản vẽ 2D thật → suy ra hình học | **Mock** — dùng 2 mặt bằng dựng sẵn. Ngoài lát cắt, xem non-goals trong `spec.md` |
| Xuất bản vẽ / hồ sơ | **Mock** — chỉ hiện alert |

Khối `<div class="trace">` ở bước 4 in ra route + nguồn sự thật đang dùng, và ghi rõ chỗ nào còn MOCK.

## Kiểm thử

- Click-through toàn bộ 4 route qua server thật bằng Playwright — không lỗi runtime.
- Golden set 30 case: `eval/golden-set.jsonl`. Lượt 1 **80,0%** → lượt 2 **90,0%** (bar 85%).
- Bộ đo gọi đúng `decide.py` mà bản demo dùng — không có đường code riêng cho eval.

## File

| File | Vai trò |
|---|---|
| `index.html` | Toàn bộ UI + render 2D/3D (SVG). Gọi `POST /api/decide` |
| `prompt.py` | Hợp đồng prompt: 4 route, luật không tự điền tham số, quy ước đọc kích thước VN |
| `decide.py` | Lời gọi OpenAI thật + `guard()` + ghi trace |
| `server.py` | Server local stdlib, giữ API key phía server |
| `logs/ai_trace.jsonl` | Trace mọi lời gọi: input, raw output, route, vi phạm guard, latency, token |

## `_archive-citeguard-huong-A/`

Prototype nháp theo Hướng A (tối ưu AI tutor VLearn) làm trước khi nhóm chốt Hướng C.
Giữ lại làm bằng chứng multi-prototype cho `spec.md` §8, **không phải bài nộp**.
