# CP1 · Canvas — Nhóm Draft2Life (D304)

> Bản chốt tại CP1. Evidence và spec hoàn thiện dần đến `spec.md` 23:59 N1.
> Mọi con số dưới đây tái tạo được bằng `scripts/analyze_survey.py` → `evidence/survey-results.json`.

| # | Mục | Nội dung |
|---|---|---|
| 1 | **Hướng** | **C — Làn mở.** Team tự định nghĩa bài toán; pain chứng minh bằng khảo sát 123 người + 8 phỏng vấn offline (Evidence **Đường A**) |
| 2 | **Job executor** | **Sinh viên kiến trúc/xây dựng và KTS mới đi làm đang dựng mô hình 3D từ bản vẽ 2D** — không phải "người dùng nói chung", không phải chủ nhà |
| 3 | **Pain 1 câu** | Người dựng 3D **đang** phải thao tác lại trong AutoCAD/3ds Max/Revit mỗi lần đổi một chi tiết (cửa, tường, nội thất), **vướng ở chỗ** một thay đổi nói ra trong 5 giây thì phải mất hàng chục thao tác phần mềm mới thấy được kết quả, **hậu quả là** vòng lặp sửa–xem–sửa kéo dài, 79,7% người khảo sát phải sửa đi sửa lại nhiều lần và 63,4% mất từ 3 ngày trở lên cho một mô hình |
| 4 | **Bằng chứng đầu** | **(a) Khảo sát n=123 người ngoài nhóm** (70 sinh viên · 53 KTS/nhà thiết kế đã đi làm):<br>· **98/123 = 79,7%** phải chỉnh sửa chi tiết (cửa, tường, nội thất) **nhiều lần** khi dựng 3D<br>· **94/123 = 76,4%** sẵn sàng dùng công cụ AI cho việc này → vượt ngưỡng ≥50% xác nhận<br>· **78/123 = 63,4%** mất ≥3 ngày cho một mô hình 3D từ bản vẽ 2D<br>· **109/123 = 88,6%** muốn thử bản demo<br>· Khó khăn lớn nhất tự chọn: *"sử dụng phần mềm thiết kế 3D"* 37 · *"nhận diện và khắc phục lỗi trong mô hình"* 32<br>**(b) 8 phỏng vấn offline** đã ghi âm/quay, file gốc trong dự án Draft2Life |
| 5 | **Lát cắt MỘT CÂU** | **Sinh viên kiến trúc đang có mô hình 3D dựng từ mặt bằng 2D · gõ một câu tiếng Việt mô tả chi tiết muốn sửa · AI quyết định câu đó đã đủ tham số để thực thi hay còn thiếu · trả về mô hình đã cập nhật kèm thông số, hoặc đúng một câu hỏi làm rõ** |
| 6 | **Automation + lý do** | **Conditional** — AI tự thực thi khi câu lệnh đủ 3 tham số (đối tượng · vị trí · kích thước), chuyển sang hỏi lại khi thiếu. Lý do theo cost-of-error: dựng sai hình khối thì user **thấy ngay trên màn hình và bấm Hoàn tác** (sửa rẻ); nhưng nếu AI **tự đoán kích thước rồi user xuất hồ sơ nộp đồ án / gửi chủ đầu tư** thì sai lan ra điểm số và tiền vật tư (sửa đắt) → tuyệt đối không tự điền tham số thiếu |
| 7 | **Willing users** | **109/123 người khảo sát đã tick "muốn thử demo"** (61 sinh viên + 48 KTS), 122/123 để lại email hoặc SĐT liên hệ được. Chốt 4 người cho vòng validation CP5 tại `validation/willing-users.md` — vượt yêu cầu ≥3 |
| 8 | **Phân công** | **Nguyễn Minh Công** (2A202601945, lead) — lát cắt, spec, prompt + AI call (CP3)<br>**Nguyễn Văn Sáng** (01252) — evidence Đường A, bảng impact, log phỏng vấn<br>**Diệp Đức Lai** (01784) — flow UI (`codebase/`), golden set, validation log |

---

## Bảng impact — 3 ứng viên

Cả 3 đều rút từ cùng bộ khảo sát 123 người, nên so được trực tiếp.

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Build nổi trong sự kiện? | Chọn? |
|---|---|---|---|---|---|
| **A. Vòng lặp sửa chi tiết** — đổi cửa/tường/nội thất trên mô hình đã có | **98/123 = 79,7%** | 89/123 xuất ≥5 mô hình/tháng, mỗi mô hình sửa nhiều lượt | Hàng chục thao tác phần mềm cho một thay đổi nói ra trong 5 giây | ✅ 1 AI call: câu tiếng Việt → JSON lệnh sửa; render bằng hình học đơn giản | ✅ **CHỌN** |
| **B. Dựng 3D lần đầu từ bản vẽ 2D** | 122/123 (ai cũng phải làm) | 5-10 lần/tháng | 63,4% mất ≥3 ngày/mô hình | ❌ cần vision nhận diện nét bản vẽ + suy ra hình học — không đủ 1,5 ngày, và không có "một quyết định AI" tách bạch | ❌ |
| **C. Nhận diện & sửa lỗi trong mô hình 3D** | 32/123 = 26% chọn là khó khăn lớn nhất | Cuối mỗi mô hình | Lỗi lọt vào hồ sơ nộp | ⚠️ cần model có sẵn để bắt lỗi + luật QCVN — không có nguồn sự thật kiểm chứng được trong sự kiện | ❌ |

**Lý do chọn A bằng số:** phủ nhiều người nhất trong 3 (98 vs 32 ở C), tần suất cao nhất (lặp trong từng mô hình chứ không phải mỗi mô hình một lần), và là ứng viên duy nhất có **một quyết định AI tách bạch được** — "câu này đủ tham số để thực thi chưa" — nên demo được trong 5 phút.

**Vì sao loại B** (dù 122/123 người gặp): pain lớn hơn nhưng lời giải là bài toán computer vision hình học, không build nổi trong 1,5 ngày; và nếu làm ẩu thì phần AI chỉ còn là "upload rồi chờ", không có quyết định nào để soi 4 lớp chỗ khó.
**Vì sao loại C:** bằng chứng yếu nhất trong 3 (26%), và để bắt lỗi đúng thì cần nguồn sự thật là quy chuẩn xây dựng — nhóm không có bản quy chuẩn kiểm chứng được, sẽ rơi thẳng vào lớp ① bịa nguồn.

---

## 4 lớp chỗ khó — bản phác *(chi tiết + ≥8 kịch bản ở spec §5)*

| Lớp | Cụ thể hoá cho lát cắt này |
|---|---|
| ① **Nguồn sự thật** | Mô hình đang mở là nguồn sự thật duy nhất. AI bịa được: phòng không có trong mặt bằng, tường không tồn tại, kích thước không đo được từ bản vẽ. Không có căn cứ → nói rõ "mặt bằng không có phòng bếp", **không dựng** |
| ② **Mơ hồ / thiếu thông tin** | *"thêm cửa sổ"* thiếu: phòng nào · tường nào · kích thước bao nhiêu. → hỏi lại đúng **một** câu về tham số thiếu quan trọng nhất; không đoán, không điền mặc định im lặng |
| ③ **Ngoài phạm vi / thẩm quyền** | User sẽ đòi: *"tường này đập được không?"* · *"mẫu này có đạt QCVN/PCCC không?"* · *"báo giá thi công bao nhiêu?"* → từ chối rõ (việc của kỹ sư kết cấu / đơn vị thẩm duyệt) nhưng vẫn đưa thứ hữu ích: xuất bản vẽ hiện trạng kèm thông số để mang đi hỏi |
| ④ **Đặc thù domain** | Sai kích thước cửa/lối đi → lọt vào hồ sơ nộp đồ án hoặc bản gửi chủ đầu tư, mất điểm / mất tiền vật tư. Sai vị trí tường chịu lực → nguy hiểm thật. Mọi thông số hiện ra bắt buộc kèm nhãn **"ước tính từ mặt bằng — kiểm lại trước khi xuất hồ sơ"** |

---

## Ghi chú bảo mật

- File khảo sát gốc chứa **họ tên · email · SĐT** của 123 người → **không commit vào repo**. Nó nằm ngoài repo; `scripts/analyze_survey.py` chỉ ghi ra số tổng hợp đã loại PII và có assert chặn rò rỉ.
- File phỏng vấn (audio/video) giữ ở dự án Draft2Life cũ, repo chỉ dẫn chiếu.
