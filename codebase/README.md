# Draft2Life — prototype

**Mức prototype khai báo tại CP2: `Mock`** — flow chính bấm đi hết được, dữ liệu giả, **chưa có AI thật**.
Lời gọi AI thật vào ở CP3 (bắt buộc theo đề bài), tại đúng một chỗ đã chừa sẵn.

## Chạy

Mở thẳng `codebase/index.html` bằng trình duyệt. Không cần server, không cần cài gì.

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
| Hàm `decide()` — quyết định route | **MOCK**, bảng tra bằng regex. **CP3 thay đúng hàm này bằng 1 lời gọi AI thật** trả JSON `{route, params, question, reason}`; phần render giữ nguyên |
| Upload bản vẽ 2D thật → suy ra hình học | **Mock** — dùng 2 mặt bằng dựng sẵn. Ngoài lát cắt, xem non-goals trong `spec.md` |
| Xuất bản vẽ / hồ sơ | **Mock** — chỉ hiện alert |

Khối `<div class="trace">` ở bước 4 in ra route + nguồn sự thật đang dùng, và ghi rõ chỗ nào còn MOCK.

## Kiểm thử

Đã click-through toàn bộ 4 route bằng Playwright, không có lỗi runtime.
Golden set ≥20 case và bảng kết quả lượt 1 vào `eval/` ở CP3.

## `_archive-citeguard-huong-A/`

Prototype nháp theo Hướng A (tối ưu AI tutor VLearn) làm trước khi nhóm chốt Hướng C.
Giữ lại làm bằng chứng multi-prototype cho `spec.md` §8, **không phải bài nộp**.
