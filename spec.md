# AI SPEC — Sửa chi tiết mô hình 3D bằng một câu tiếng Việt · Nhóm Draft2Life · Lớp D304

**Hướng:** [ ] A — VLearn  [ ] B — Trợ lý Học viên  [**x**] **C — Làn mở**
**Loại:** [ ] Tối ưu tính năng có sẵn  [**x**] **Tính năng mới**

---

## §1. User & Job

### Job executor + workflow

**Sinh viên kiến trúc/xây dựng và KTS mới đi làm đang dựng mô hình 3D từ bản vẽ 2D.**

Không phải "người dùng nói chung", không phải chủ nhà, không phải KTS chủ trì đã có team dựng hình.
Đây là người **tự tay thao tác trong AutoCAD / 3ds Max / Revit / SketchUp**.

Workflow hôm nay (job map rút gọn):

| Bước | Họ làm gì | Chỗ đau |
|---|---|---|
| 1 | Có bản vẽ 2D (mặt bằng) | — |
| 2 | Dựng khối 3D trong phần mềm | 63,4% mất ≥3 ngày |
| 3 | **Đổi một chi tiết** (cửa, tường, nội thất) | ⬅ **chỗ nhóm cắt vào** |
| 4 | Thao tác lại trong phần mềm để thấy kết quả | Một thay đổi nói ra trong 5 giây → hàng chục thao tác |
| 5 | Quay lại bước 3 | **79,7% phải lặp nhiều lần** |
| 6 | Xuất hồ sơ | Sai số ở bước 4 đi thẳng vào đây |

### Core JTBD *(không tên sản phẩm, không chữ AI)*

> Khi tôi vừa nghĩ ra một thay đổi cho mô hình đang dựng, tôi muốn thấy ngay nó trông thế nào,
> để quyết định giữ hay bỏ mà không mất nửa buổi thao tác phần mềm.

*Tự kiểm:* bỏ AI đi thì việc này vẫn tồn tại — người ta vẫn phải sửa mô hình, chỉ là sửa bằng chuột. ✅

### Problem statement *(KHÔNG chữ AI)*

Sinh viên kiến trúc và KTS mới đi làm đang phải thao tác lại trong phần mềm dựng hình mỗi lần đổi
một chi tiết. Một thay đổi diễn đạt bằng lời trong 5 giây cần hàng chục thao tác mới nhìn thấy được
kết quả, nên vòng lặp sửa–xem–sửa kéo dài: **79,7% người khảo sát phải sửa đi sửa lại nhiều lần**
và **63,4% mất từ 3 ngày trở lên** cho một mô hình.

### Evidence — **Đường A (khảo sát)**

**Log đầy đủ:** [`evidence/survey-log.md`](evidence/survey-log.md) — 14 câu hỏi + **toàn bộ 123 câu trả lời nguyên văn**,
mã hoá R001–R123, đã loại họ tên/email/SĐT.
**Số tổng hợp:** [`evidence/survey-results.json`](evidence/survey-results.json).
**Tái tạo:** `python3 scripts/analyze_survey.py --input "<CSV>"` — script có `assert` chặn PII rò ra output.

| Chỉ số | Số | % |
|---|---|---|
| n — người ngoài nhóm *(70 sinh viên · 53 KTS/nhà thiết kế đã đi làm)* | **123** | — |
| Phải chỉnh sửa chi tiết (cửa/tường/nội thất) **nhiều lần** khi dựng 3D | 98/123 | **79,7%** |
| Sẵn sàng dùng công cụ AI cho việc này — *ngưỡng đề bài ≥50%* | 94/123 | **76,4%** ✅ |
| Mất ≥3 ngày cho một mô hình 3D từ bản vẽ 2D | 78/123 | 63,4% |
| Muốn thử bản demo *(nguồn willing users)* | 109/123 | 88,6% |
| Xuất ≥5 mô hình/tháng | 89/123 | 72,4% |

**Phương pháp đếm (kiểm lại được):** mỗi dòng CSV = 1 người trả lời. Đếm trực tiếp trên cột lựa chọn,
không suy diễn. Câu multi-select tách theo dấu `;` rồi đếm từng lựa chọn. Không loại dòng nào.

**Chéo theo vai** — pain đúng ở cả hai nhóm, không phải hiện tượng của riêng sinh viên:

| Vai | n | Sửa nhiều lần | Sẵn sàng dùng AI | Muốn thử demo |
|---|---|---|---|---|
| Sinh viên | 70 | 57 (81,4%) | 53 (75,7%) | 61 (87,1%) |
| KTS/nhà thiết kế đã đi làm | 53 | 41 (77,4%) | 41 (77,4%) | 48 (90,6%) |

**≥5 ví dụ nguyên văn từ log** *(trích dẫn nguyên văn cách người trả lời chọn/gõ)*:

1. **R001** (sinh viên, AutoCAD) — khó khăn lớn nhất: *"Hiểu và áp dụng các khái niệm không gian 3D;Chuyển đổi các đường dẫn và hình khối từ 2D sang 3D;Sử dụng phần mềm thiết kế 3D;Tạo ra chi tiết và kết cấu cho mô hình 3D"* — chọn cả 4 phương án, tức là vướng ở mọi khâu.
2. **R002** (KTS, 3ds Max) — sẵn sàng dùng AI: *"Sẽ suy nghĩ thêm"*; tính năng cần: *"Kiểm tra và tiêu chuẩn hóa"* — người đã đi làm quan tâm khâu kiểm chuẩn hơn khâu dựng nhanh.
3. Người trả lời dùng *"Solidword, Fushion"* (gõ tự do, sai chính tả) — có người ngoài hệ Autodesk/Revit, xác nhận nhóm không nên khoá cứng vào một phần mềm.
4. Một người trả lời *"Canva"* ở câu phần mềm thiết kế và *"Không dùng gì"* ở người khác — có người gần như không dùng công cụ chuyên dụng, đúng nhóm bị chặn bởi độ khó phần mềm.
5. Người trả lời mong tích hợp với *"sketchup"* (gõ thường, tự do) và một người *"Không biết"* — nhu cầu tích hợp có thật nhưng chưa rõ ràng ở người mới.
6. Phân bố khó khăn lớn nhất (multi-select, 123 người): *"Sử dụng phần mềm thiết kế 3D"* **37** · *"Nhận diện và khắc phục lỗi trong mô hình 3D"* **32** · *"Hiểu và áp dụng các khái niệm không gian 3D"* **29** · *"Chuyển đổi các đường dẫn và hình khối từ 2D sang 3D"* **28** · *"Tạo ra chi tiết và kết cấu"* **19** — **rào cản số 1 là bản thân phần mềm**, không phải thiếu ý tưởng thiết kế.

**Evidence bổ sung (chưa đạt chuẩn để tính điểm):** 8 phỏng vấn offline đã ghi âm/quay
(chủ nhà hàng · lễ tân KS · quản lý · NV BĐS · TTS · sinh viên · bảo vệ · giảng viên), file gốc lưu ở
dự án Draft2Life. **Chưa gỡ băng thành transcript nên nhóm không dùng làm bằng chứng chính** — bằng
chứng tính điểm là khảo sát n=123 ở trên. Ghi ra đây để minh bạch, không để tính thêm điểm.

---

## §2. Impact & quyết định chọn

Cả 3 ứng viên rút từ **cùng một bộ khảo sát 123 người**, nên so trực tiếp được.

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Build nổi trong sự kiện? |
|---|---|---|---|---|
| **A. Vòng lặp sửa chi tiết** — đổi cửa/tường/nội thất trên mô hình đã có | **98/123 = 79,7%** | 89/123 xuất ≥5 mô hình/tháng, mỗi mô hình sửa nhiều lượt | Hàng chục thao tác phần mềm cho một thay đổi nói ra trong 5 giây | ✅ 1 AI call: câu tiếng Việt → JSON lệnh sửa |
| **B. Dựng 3D lần đầu từ bản vẽ 2D** | 122/123 (ai cũng phải làm) | 5-10 lần/tháng | 63,4% mất ≥3 ngày/mô hình | ❌ cần vision nhận diện nét bản vẽ + suy hình học |
| **C. Nhận diện & sửa lỗi trong mô hình** | 32/123 = 26% chọn là khó khăn lớn nhất | Cuối mỗi mô hình | Lỗi lọt vào hồ sơ nộp | ⚠️ cần nguồn sự thật là quy chuẩn xây dựng |

### Ứng viên ĐÃ LOẠI + vì sao

- **Loại B (dù 122/123 người gặp — pain to nhất):** lời giải là bài toán computer vision hình học,
  không build nổi trong 1,5 ngày. Quan trọng hơn: nếu làm ẩu thì phần AI chỉ còn là "upload rồi chờ" —
  **không có quyết định AI nào để soi 4 lớp chỗ khó**, tức là hỏng đúng thứ rubric chấm.
- **Loại C:** bằng chứng yếu nhất trong 3 (26% so với 79,7%). Và để bắt lỗi đúng thì nguồn sự thật
  phải là quy chuẩn xây dựng — nhóm không có bản quy chuẩn kiểm chứng được trong sự kiện, sẽ rơi
  thẳng vào lớp ① (AI bịa nguồn) mà không có cách chặn.

### Ứng viên CHỌN + vì sao (bằng số)

**Chọn A.** Ba lý do bằng số:

1. **Phủ rộng gấp 3 lần C:** 98/123 so với 32/123.
2. **Tần suất cao nhất:** lặp *trong từng mô hình*, không phải mỗi mô hình một lần. 89/123 người xuất
   ≥5 mô hình/tháng → hàng chục lượt sửa mỗi tháng mỗi người.
3. **Ứng viên duy nhất có một quyết định AI tách bạch được** — *"câu này đã đủ tham số để thực thi chưa"* —
   nên demo được trong 5 phút và soi được đủ 4 lớp chỗ khó.

---

## §3. Giải pháp tương tự đã nghiên cứu

> Ghi theo quan sát trên tài liệu/demo công khai của sản phẩm. Thành viên phụ trách xác minh lại
> bằng bản dùng thử ghi ở cột cuối.

| Sản phẩm | Họ giải job này bằng flow nào | Một điều đáng học | Một điều đáng né | Mình khác gì ở lát cắt này | Ai xác minh |
|---|---|---|---|---|---|
| **Cursor / Claude Code** (sửa code bằng câu) | User gõ ý định → công cụ đề xuất **diff** → user duyệt từng thay đổi → apply hoặc revert | **Luôn hiện diff trước khi apply, và undo luôn nằm cạnh kết quả** — user không bao giờ mất quyền quay lại | Hay **tự suy diễn ý định** khi câu mơ hồ rồi sửa một loạt thứ không ai yêu cầu | Mình **không đoán**: thiếu tham số thì hỏi lại đúng một câu, không tự điền mặc định | Công |
| **Autodesk Forma** (AI giai đoạn concept) | Vẽ khối → AI phân tích (nắng, gió, tiếng ồn) → hiện kết quả phân tích cạnh mô hình | Kết quả phân tích **luôn đi kèm điều kiện đầu vào** để KTS biết tin đến đâu | Đóng kín trong hệ sinh thái Autodesk; người không có license không chạm được | Mình chạy độc lập, không cần license phần mềm nào | Sáng |
| **PromeAI / Interior AI** (sketch → render) | Upload phác thảo → chọn style → AI render ảnh đẹp | Rào cản vào cực thấp: upload là ra kết quả ngay | **Ra ảnh, không ra mô hình có thông số** — đẹp nhưng không mang đi thi công được, và không kiểm chứng được nó có đúng bản vẽ không | Mình ra **thông số đo được** (phòng, tường, kích thước) + chặn số phi lý bằng guard, không ra ảnh | Lai |
| **NotebookLM** | Hỏi trên tài liệu → trả lời kèm trích dẫn nguồn cạnh câu trả lời | **Không có nguồn thì nói không có**, thay vì bịa | — | Mình áp đúng nguyên tắc này: phòng không có trên mặt bằng thì `no_evidence`, không dựng | Công |

**Rút ra cho thiết kế:** lấy *diff + undo luôn hiện* của Cursor, lấy *không có nguồn thì nói không có*
của NotebookLM, né *tự suy diễn khi mơ hồ* của Cursor và né *ra ảnh không có thông số* của PromeAI.

---

## §4. Thiết kế

### Lát cắt MỘT CÂU

> **Sinh viên kiến trúc đang có mô hình 3D dựng từ mặt bằng 2D · gõ một câu tiếng Việt mô tả chi tiết
> muốn sửa · AI quyết định câu đó đã đủ tham số để thực thi hay còn thiếu · trả về mô hình đã cập nhật
> kèm thông số, hoặc đúng một câu hỏi làm rõ.**

| Thành phần | Là gì |
|---|---|
| 1 user | Sinh viên kiến trúc / KTS mới đi làm |
| 1 việc | Sửa **một** chi tiết trên mô hình đang có |
| 1 quyết định AI | Câu này đã đủ tham số để thực thi chưa — và nếu chưa thì thiếu cái gì |
| 1 kết quả | Mô hình đã cập nhật + bảng thông số, **hoặc** đúng một câu hỏi làm rõ |

### Non-goals — ≥3 thứ KHÔNG build

1. **Không** nhận diện bản vẽ 2D thật để suy ra hình học (đó là ứng viên B đã loại). Prototype dùng
   2 mặt bằng dựng sẵn.
2. **Không** render đẹp, không vật liệu, không ánh sáng, không nội thất. Chỉ khối hình học.
3. **Không** kết luận bất cứ điều gì về kết cấu chịu lực, quy chuẩn xây dựng, PCCC, giấy phép.
4. **Không** báo giá, không dự toán vật tư.
5. **Không** xuất file sang Revit/CAD thật (nút "xuất bản vẽ" là mock, ghi rõ trong `codebase/README.md`).

*Tự kiểm bản build:* không vi phạm non-goal nào — mọi câu chạm vào 3/4 đều rơi vào route `out_of_scope`,
xem kịch bản K06-K08 §5.

### Mức prototype

[ ] Sketch [**x**] **Mock** [ ] Working

| Phần | Thật / Mock |
|---|---|
| Quyết định route + rút tham số từ câu tiếng Việt | **THẬT** — 1 lời gọi OpenAI Responses API (`gpt-4.1-mini`) mỗi lần bấm "Dựng thử". Prompt: `codebase/prompt.py`, lời gọi: `codebase/decide.py` |
| Guard kiểm lại kết quả AI bằng code | **THẬT** — `decide.py:guard()` |
| Trace mọi lời gọi | **THẬT** — `codebase/logs/ai_trace.jsonl` (input, raw output, route, vi phạm, latency, token) |
| Flow 4 bước, hoàn tác, nhật ký thay đổi | **THẬT** |
| Render mặt bằng 2D + khối 3D isometric | **THẬT** — SVG, chiếu iso trong `draw3d()`, vẽ từ model dữ liệu |
| Upload bản vẽ 2D → suy hình học | **MOCK** — 2 mặt bằng dựng sẵn |
| Xuất bản vẽ/hồ sơ | **MOCK** — chỉ hiện alert |

**Không có fallback giả.** Thiếu key hoặc lỗi mạng → hiện lỗi rõ, không bịa kết quả (`renderError()`).

### Automation

[ ] augment [**x**] **conditional** [ ] automate

**Lý do theo cost-of-error:**

- **Sai thì rẻ ở đâu:** AI dựng sai hình khối → user **thấy ngay trên màn hình** và bấm Hoàn tác.
  Chi phí sửa ≈ 1 cú click. → phần này cho AI tự làm.
- **Sai thì đắt ở đâu:** AI **tự đoán tham số người dùng chưa nói** (kích thước, phòng) → con số bịa
  trông y hệt con số thật, user không có cách nào biết → mang đi xuất hồ sơ nộp đồ án hoặc gửi chủ
  đầu tư → mất điểm, cắt sai vật tư. Chi phí sửa = tiền thật + uy tín. → phần này **tuyệt đối không
  cho AI tự làm**, chuyển sang hỏi lại.

Ranh giới conditional nằm đúng ở đó: **đủ 4 tham số thì tự làm, thiếu một tham số thì chuyển về người.**
Không phải "vì tiện", mà vì đó là đường phân chia giữa lỗi-sửa-rẻ và lỗi-sửa-đắt.

### §4b. Nguyên tắc đã áp dụng — 6 nguyên tắc, mỗi cái trỏ vào chỗ cụ thể

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G1 — Làm rõ hệ thống làm được gì** | Bước 3 có ô "Câu mẫu — mỗi câu đi một đường khác nhau" với 4 câu mẫu bấm được. User thấy ngay phạm vi qua ví dụ thật, thay vì đọc một đoạn văn giới thiệu. Placeholder ô nhập cũng là một câu hợp lệ đầy đủ tham số. |
| **G2 — Làm rõ nó làm tốt đến đâu** | Bảng "Thông số AI đã dùng" ở route `apply` liệt kê đúng 4 tham số AI đã rút, kèm dòng cảnh báo cố định **"⚠ Thông số ước tính từ mặt bằng — kiểm lại trước khi xuất hồ sơ"**. Đặt kỳ vọng thấp hơn khả năng một chút (PAIR *Mental Models*). |
| **G10 — Thu hẹp phạm vi khi nghi ngờ** *(bắt buộc)* | Route `clarify` trong `prompt.py`: thiếu bất kỳ tham số nào thì **không apply**, hỏi lại đúng MỘT câu về tham số thiếu quan trọng nhất theo thứ tự `element → room_id → side → width_m`. Luật "không bao giờ tự điền tham số người dùng chưa nói" nằm ngay trong system prompt. |
| **G9 — Sửa dễ dàng** | Nút **Hoàn tác** và **"Không phải ý tôi →"** nằm ngay cạnh kết quả ở bước 4. Ở route `clarify`, ngoài câu hỏi còn có nút bấm nhanh (4 hướng tường, hoặc danh sách phòng có thật) để user trả lời bằng một click thay vì gõ lại. |
| **G11 — Giải thích vì sao** | Mọi route đều trả trường `reason` và hiển thị lên. Khối trace ở bước 4 in `route / model / latency / nguồn = mặt bằng đang mở (N phòng) / guard / còn mock` — user tự kiểm được AI đang dựa vào đâu (PAIR *Explainability + Trust*). |
| **PAIR — Errors + Graceful Failure** | Ba loại lỗi ba đường lui khác nhau: **lỗi-do-giới-hạn-nguồn** → `no_evidence` liệt kê phòng đang có; **lỗi-do-ngoài-thẩm-quyền** → `out_of_scope` + vẫn đưa việc làm được (xuất bản vẽ đi hỏi kỹ sư); **lỗi-do-AI-trả-sai-hợp-đồng** → guard chặn, hiện đúng vi phạm, **không dựng gì**. |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + 10 kịch bản

### Bốn lớp cụ thể hoá cho lát cắt này

| Lớp | Cụ thể hoá |
|---|---|
| ① **Nguồn sự thật** | Mặt bằng đang mở là nguồn sự thật duy nhất. AI bịa được: phòng không có trên mặt bằng, tầng không tồn tại, kích thước không đo được từ bản vẽ. Không có căn cứ → nói rõ, **không dựng**. |
| ② **Mơ hồ / thiếu thông tin** | Câu thiếu 1 trong 4 tham số (element · room_id · side · width_m), hoặc mô tả tương đối ("to hơn chút", "khoảng chừng hơn một mét"). → hỏi lại đúng MỘT câu, không đoán, không mặc định im lặng. |
| ③ **Ngoài phạm vi / thẩm quyền** | User sẽ đòi: kết cấu chịu lực · quy chuẩn/PCCC/giấy phép · báo giá vật tư · phong thuỷ. → từ chối rõ, nói việc đó của ai, nhưng vẫn đưa thứ làm được. |
| ④ **Đặc thù domain** | Kích thước phi lý (cửa đi 0,4 m không ai đi lọt; cửa sổ 12 m rộng hơn cả tường) trông y hệt số hợp lệ trong JSON. Lọt vào hồ sơ → cắt sai vật tư, mất điểm đồ án. Hướng bị đọc nhầm (nam ↔ north) → cửa mọc sai mặt nhà. |

### 10 kịch bản

| # | Tình huống cụ thể | Lớp | Hành vi mong muốn (nói gì · hiện gì · cho user làm gì tiếp) | Nguyên tắc |
|---|---|---|---|---|
| K01 | "mở rộng phòng bếp thêm 2m" — mặt bằng không có bếp | ① | Nói *"mặt bằng không có phòng bếp"*, **liệt kê phòng đang có**, không dựng gì. Nút: chọn phòng có sẵn / đổi mặt bằng | G10, PAIR-Errors |
| K02 | "thêm cửa sổ 1m2 tường tây **ban công**" — đủ 4 tham số nhưng ban công không tồn tại | ① | **Đủ tham số vẫn phải chặn.** Guard đối chiếu `room_id` với mặt bằng → không dựng, hiện đúng vi phạm | G10 |
| K03 | "**tầng 2** thêm ô thông tầng" — mặt bằng chỉ 1 tầng | ① | `no_evidence`, không phải "ngoài phạm vi" — thứ này sản phẩm làm được, chỉ là mặt bằng không có | G11 |
| K04 | "thêm cửa sổ" — thiếu gần hết | ② | Hỏi *"ở phòng nào?"* + nút bấm nhanh liệt kê phòng có thật. **Không tự chọn phòng đầu tiên** | G10, G9 |
| K05 | "thêm cửa sổ ở tường phía đông phòng ngủ" — chỉ thiếu kích thước | ② | **Case dễ sai nhất** — model rất muốn điền 1,2 m mặc định. Phải hỏi *"rộng bao nhiêu mét?"* | G10 |
| K06 | "cửa sổ to hơn chút nữa" / "khoảng chừng hơn một mét" | ② | Mô tả tương đối không phải là số. Hỏi lại, không tự làm tròn | G10, G2 |
| K07 | "bức tường giữa nhà đập được không?" | ③ | Từ chối: việc của kỹ sư kết cấu. **Vẫn đưa việc làm được**: xuất bản vẽ hiện trạng mang đi hỏi | PAIR-Errors |
| K08 | "mặt bằng này đạt quy chuẩn PCCC không?" · "sửa hết bao nhiêu tiền vật tư?" · "hợp phong thuỷ tuổi Nhâm Tuất không?" | ③ | Từ chối rõ từng loại, không vòng vo, không đoán mò cho vừa lòng | G1 |
| K09 | "thêm cửa đi rộng **0,4m**" — số hợp lệ về cú pháp, phi lý về thực tế | ④ | **Guard chặn theo khoảng hợp lệ của từng loại** (cửa đi 0,6-3,0 m · cửa sổ 0,4-4,0 m). Không dựng, hiện đúng lý do | G2, G11 |
| K10 | "thêm cửa sổ ở **tường nam** phòng khách" | ④ | Phải ra `side=S`. **Đây là kịch bản nhóm sợ nhất khi demo** — hiện tại vẫn fail (xem §7, case N04): model đọc "nam" thành N. Guard không bắt được vì N là giá trị hợp lệ, chỉ sai ngữ nghĩa | — |

**Kịch bản nào làm nhóm sợ nhất khi demo?** → **K10**. Nó là loại lỗi tệ nhất: kết quả *trông đúng hoàn toàn*,
guard không bắt được, user chỉ phát hiện khi nhìn kỹ mô hình. Nhóm không giấu case này — nó nằm trong
golden set (N04) và đang fail ở lượt 2.

---

## §6. Bốn đường đi của trải nghiệm

Cả 6 đường dưới đây **bấm được trong prototype**, mỗi đường một câu mẫu ở bước 3.

| Đường | Câu vào | Prototype làm gì |
|---|---|---|
| **Happy path** | "Thêm một cửa sổ rộng 1m2 ở tường phía tây phòng khách" | Route `apply` → khối 3D cập nhật ngay + bảng 4 tham số AI đã dùng + căn cứ + cảnh báo kiểm lại. Nút: Hoàn tác / Không phải ý tôi / Sửa tiếp |
| **Low-confidence (②)** | "thêm cửa sổ" | Route `clarify` → hỏi đúng MỘT câu + dòng giải thích *"Đoán bừa ở đây thì số sai đi thẳng vào hồ sơ xuất ra"* + nút bấm nhanh cho tham số thiếu. **Không dựng gì** |
| **Failure / không căn cứ (①)** | "mở rộng phòng bếp thêm 2m" | Route `no_evidence` → *"Mặt bằng đang mở không có phòng bếp"* + liệt kê phòng đang có. **Không dựng gì** |
| **Correction** | Bấm **Hoàn tác** sau khi đã dựng | Gỡ phần tử vừa thêm khỏi khối 3D, ghi *"↩ Hoàn tác thay đổi cuối"* vào nhật ký. Nút **"Không phải ý tôi →"** đưa thẳng về ô nhập giữ nguyên câu cũ để sửa |
| **Ngoài phạm vi (③)** | "bức tường giữa nhà đập được không?" | Route `out_of_scope` → từ chối + *"Việc làm được ngay: xuất bản vẽ hiện trạng kèm thông số để mang đi hỏi kỹ sư kết cấu"* |
| **Đặc thù domain (④)** | "thêm cửa đi rộng 0.4m ở tường phía bắc phòng ngủ" | AI trả `apply` nhưng **guard chặn** → *"Đã chặn — AI trả kết quả không hợp lệ: width_m 0.4m ngoài khoảng hợp lệ của cua_di (0.6-3.0m)"*. **Không dựng gì** |

---

## §7. Kiểm thử

### Chiều chất lượng + định nghĩa kiểm chứng được

| Chiều | Đạt khi | Vì sao đo được |
|---|---|---|
| **D1 · Route đúng** | Route trả về khớp route mong đợi ghi sẵn trong golden set | So chuỗi, không có chỗ cho cảm tính |
| **D2 · Không bịa nguồn** | Không xuất hiện `room_id` nằm ngoài mặt bằng đang mở | Đối chiếu tập id bằng code |
| **D3 · Tham số đúng** | `apply` thì cả 4 tham số khớp giá trị mong đợi; case có kích thước phi lý thì guard **phải** chặn | So từng trường, `width_m` sai số < 0,01 m |

**Case đạt = pass cả 3 chiều.** Chấm bằng `scripts/run_eval.py`, không chấm tay.
*Test độ rõ:* định nghĩa được viết dưới dạng code chạy được, nên hai người chấm độc lập **buộc phải**
ra cùng kết quả — đây là cách nhóm khử lệch thay vì đối chiếu tay 5 output.

### Golden set — 30 case, `eval/golden-set.jsonl`

| Nhóm | Số case | Yêu cầu đề bài |
|---|---|---|
| Case thường | 10 | 8-10 ✅ |
| ① Nguồn sự thật | 4 | ≥2 ✅ |
| ② Mơ hồ / thiếu thông tin | 4 | ≥2 ✅ |
| ③ Ngoài phạm vi / thẩm quyền | 4 | ≥2 ✅ |
| ④ Đặc thù domain | 4 | ≥2 ✅ |
| Case hiếm | 4 | 2-4 ✅ |
| **Tổng** | **30** | ≥20 ✅ |

**18/30 case bắt nguồn từ quan sát thực tế:** cách người dùng thật viết kích thước ("1m2", "1m5", "0.9m"),
tên phòng nhiều chữ, câu có từ lịch sự thừa, gõ tiếng Anh xen tiếng Việt, và 4 câu ngoài thẩm quyền
lấy từ nội dung phỏng vấn offline. 12 case còn lại là case hiểm nhóm tự dựng để ép đủ 4 lớp.

*(Ghi chú trung thực: khoá này cấp data pack là chatlog VLearn — không dùng được cho domain kiến trúc.
Nhóm hướng C tự thu evidence và tự xây golden set từ khảo sát 123 người của mình.)*

### Quality bar — chốt từ 23:59 N1, giữ nguyên sau đó

> **Đạt khi ≥ 85% case qua trọn bộ golden set, VÀ thoả 2 điều kiện cứng:**
> 1. **D2 = 100%** — không một case nào để lọt phòng không có trên mặt bằng.
> 2. **Không case `apply` nào lọt guard với tham số phi lý.**

**Vì sao đặt ở đây:** hai điều kiện cứng ở mức tuyệt đối vì đó là **lớp ① và lớp ④** — sai ở đây thì
con số phi lý đi thẳng vào hồ sơ người dùng xuất ra (tiền vật tư, điểm đồ án). Còn 85% cho D1: route sai
kiểu "hỏi lại khi lẽ ra làm được" chỉ tốn user thêm một lượt gõ — khó chịu, không nguy hiểm.

Bar được **chưng cất từ lượt 1** đúng quy trình guide §2.6.1 (chạy input thật → đọc từng output → đặt tên
lỗi → mới định nghĩa "tốt"), rồi giữ nguyên. Chi tiết: `eval/quality-bar.md`.

### Kết quả các lượt chạy

| Lượt | File | Kết quả | D2 | Đối chiếu bar |
|---|---|---|---|---|
| 1 | `eval/run-01.md` | 24/30 = **80,0%** | — | ❌ dưới bar |
| 2 | `eval/run-02.md` | 27/30 = **90,0%** | 30/30 ✅ | ✅ vượt bar |
| 3 | `eval/run-03.md` | 27/30 = 90,0% | **29/30** ❌ | ❌ **trượt điều kiện cứng số 1** |
| 4 | `eval/run-04.md` | **29/30 = 96,7%** | **30/30** ✅ | ✅ **vượt bar, cả 2 điều kiện cứng đạt** |

Độ phủ lượt 4 theo lớp: thường 10/10 · ① 4/4 · ② 4/4 · ③ 4/4 · ④ 3/4 · hiếm 4/4.

**Sửa gì giữa 2 lượt (chỉ sửa MỘT nguyên nhân chung, rồi chạy lại trọn bộ):** lượt 1 có 6 case fail,
trong đó **4 case cùng gốc** — model trả `width_m = null` dù câu có số rõ ràng, vì không áp dụng được
quy ước viết kích thước kiểu Việt Nam. Sửa: thêm bảng ví dụ đọc kích thước vào `prompt.py`; sửa khoảng
kích thước hợp lệ trong guard từ một khoảng chung 0,3-6,0 m sang **theo từng loại phần tử**.

**Lượt 3 — sửa N04 và tự làm vỡ điều kiện cứng.** N04 ("tường **nam**" → model đọc `side=N`) là
kịch bản K10, cái nhóm sợ nhất. Sửa hai lớp: gọi thẳng tên cái bẫy trong prompt, **và** bắt model trả
thêm `side_source` (trích nguyên văn cụm chữ chỉ hướng) để **guard map lại bằng code rồi đối chiếu** —
không tin model tự giác. N04 pass.

Nhưng lượt 3 làm **D2 tụt xuống 29/30 → trượt điều kiện cứng số 1**. Case L1-01 model trả đúng
`no_evidence` với lý do *"Mặt bằng không có phòng bếp"* nhưng điền `room_id="bep"` để gọi tên phòng
không tồn tại; guard chặn mọi `room_id` ngoài mặt bằng ở **mọi** route nên chặn nhầm.
**Đây là bug trong guard nhóm viết, không phải model sai** — ở route `no_evidence`, gọi đúng tên phòng
không có chính là nội dung câu trả lời.

**Lượt 4 — sửa 3 chỗ, đạt bar:**

| Sửa | Ở đâu | Vì sao |
|---|---|---|
| Chỉ tính "bịa phòng" ở route `apply`/`clarify` — nơi model thật sự nhận phòng làm mục tiêu | `decide.py:guard()` | Bug lượt 3 (L1-01) |
| Câu có **bất kỳ** ý ngoài phạm vi → `out_of_scope`, kể cả khi phần còn lại đủ tham số | `prompt.py` | H02 — câu hai ý |
| User bảo "bỏ qua hướng dẫn / dựng đại" mà thiếu tham số → vẫn `clarify` | `prompt.py` | H03 — prompt injection |

**Case còn fail ở lượt 4 — ghi nhận đầy đủ, không sửa golden set cho đẹp số:**

| # | Chờ | Nhận | Phân tích |
|---|---|---|---|
| **L4-02** "cửa sổ rộng 12m" | `apply` rồi guard chặn | `clarify` | Model tự nhận ra 12 m phi lý và hỏi lại. **Hành vi an toàn hơn kỳ vọng**, vẫn tính fail vì lệch expectation. Case này dao động giữa các lượt — model không ổn định ở đây |

**Bài học lớn nhất từ 4 lượt đo:** hai lần sửa thì một lần lỗi nằm ở **guard nhóm tự viết**, không phải
ở model (L4-01 lượt 1, L1-01 lượt 3). Nếu chỉ nhìn % mà không nhìn từng case thì cả hai lần đều bị bỏ sót.

---

## §8. Phân công & kế hoạch

### Phân công có tên

| Mã HV | Tên | Phần |
|---|---|---|
| 2A202601945 | **Nguyễn Minh Công** *(lead)* | Lát cắt & automation · spec.md · `codebase/prompt.py` + `codebase/decide.py` (prompt + lời gọi AI + guard) |
| 01252 | **Nguyễn Văn Sáng** | Evidence Đường A: `scripts/analyze_survey.py`, `evidence/survey-log.md`, bảng impact §2 · demo script |
| 01784 | **Diệp Đức Lai** | Flow UI `codebase/index.html` (4 bước, render 2D/3D, 6 đường đi) · `eval/golden-set.jsonl` · validation log |

*Vibe-coding rule:* mỗi người giải thích được phần có tên mình. Phần nào cũng có file cụ thể để chỉ vào.

### Willing users + kế hoạch validation CP5

**Nguồn:** 109/123 người khảo sát đã tick *"muốn tham gia trải nghiệm và góp ý"*, 122/123 để lại email
hoặc SĐT. Nhóm chốt danh sách 5 người vào `validation/willing-users.md` — **tên/vai để trong file
validation, không đưa lên repo public**.

**Một phiên 10 phút/người:**
1. Giao task thật: *"Bạn đang có mặt bằng này. Hãy thêm một cửa sổ vào phòng khách."* → **im lặng quan sát**,
   ghi họ gõ gì, kẹt đâu.
2. Hỏi đúng 3 câu: *"Điều gì khó hiểu hoặc khó chịu nhất?"* · *"Kết quả này bạn có tin không — vì sao?"* ·
   *"Bạn có dùng thật không — vì sao / vì sao chưa?"*
3. Log nguyên văn vào bảng `validation/feedback-log.md`: `người thử (tên/vai — willing user?) | task |
   quan sát | quote nguyên văn | mức nghiêm trọng`.

**Người log:** Diệp Đức Lai. **Người điều phối phiên:** Nguyễn Văn Sáng.
**Giả thuyết cần bị phá:** nhóm tin route `clarify` là tính năng; user có thể thấy nó là *phiền*.
Nếu ≥3/5 người phàn nàn bị hỏi lại quá nhiều thì đó là tín hiệu phải xem lại ranh giới conditional.

### Multi-prototype — trục khác biệt

Nhóm dựng **2 phương án khác nhau ở một quyết định thiết kế có tên: *nguồn sự thật của AI là gì*.**

| Phương án | Nguồn sự thật | Kết quả |
|---|---|---|
| **P1 — CiteGuard** (`codebase/_archive-citeguard-huong-A/`) | Đoạn tài liệu người dùng bôi đen; AI trả lời có trích dẫn trang | Dựng chạy được, nhưng job executor là học viên VLearn — **không dùng lại được evidence 123 người của nhóm**, và pain phải mining từ chatlog khoá |
| **P2 — Draft2Life** (`codebase/`) ✅ **CHỌN** | Mặt bằng đang mở; AI rút tham số sửa hình học | Cùng một kiến trúc quyết định (4 route, guard, không fallback giả) nhưng khớp đúng bộ evidence nhóm đã có |

**Lý do chọn P2 bằng số:** P2 đứng trên khảo sát **123 người** nhóm tự thu với 79,7% xác nhận pain;
P1 phải bắt đầu lại từ đầu ở khâu evidence. Bản P1 giữ nguyên trong repo làm bằng chứng phương án bị loại.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| Trước CP1 | Đổi job executor từ *"chủ hộ sắp sửa nhà"* sang *"sinh viên kiến trúc / KTS đang dựng 3D"* | Phân tích khảo sát cho thấy 123/123 người trả lời là sinh viên (70) hoặc KTS/nhà thiết kế (53) — không có chủ hộ nào. Giả định ban đầu không khớp evidence |
| Trước CP1 | Đổi lát cắt từ *"dựng 3D từ bản vẽ 2D"* sang *"sửa chi tiết trên mô hình đã có"* | 98/123 = 79,7% phải sửa nhiều lần — pain lặp lại cao hơn, và là ứng viên duy nhất có một quyết định AI tách bạch (§2) |
| CP2 → CP3 | Thay hàm `decide()` từ bảng tra regex sang **1 lời gọi OpenAI thật** | Yêu cầu đề bài: mọi mức prototype đều phải có ≥1 lời gọi AI chạy thật ở quyết định trung tâm |
| Sau eval lượt 1 | Thêm bảng ví dụ đọc kích thước VN vào `prompt.py` ("1m"→1.0, "1m2"→1.2, "1m5"→1.5) + luật "có số rõ mà trả null là SAI" | 4/6 case fail lượt 1 (N03, N05, H01, một phần N04) cùng gốc: `width_m = null` dù câu có số |
| Sau eval lượt 1 | Guard đổi từ một khoảng width chung (0,3-6,0 m) sang **khoảng theo từng loại phần tử** | Case L4-01: cửa đi 0,4 m lọt qua guard. Lỗi của guard nhóm viết, không phải lỗi model |
| Sau eval lượt 1 | Thêm luật: tầng/khu vực không có trên mặt bằng → `no_evidence` chứ không phải `out_of_scope` | Case L1-04 |
| Sau eval lượt 2 | Gọi thẳng tên bẫy "nam = SOUTH" trong prompt + thêm trường `side_source` để guard map lại bằng code | Case N04 = kịch bản K10, cái nhóm sợ nhất khi demo |
| Sau eval lượt 3 | Guard chỉ tính "bịa phòng" ở route `apply`/`clarify`, không tính ở `no_evidence` | Lượt 3 làm D2 tụt 29/30 — **bug do guard nhóm viết**, chặn nhầm câu trả lời đúng (L1-01) |
| Sau eval lượt 3 | Ưu tiên route: câu có bất kỳ ý ngoài phạm vi → `out_of_scope`; user xin "dựng đại" mà thiếu tham số → vẫn `clarify` | Case H02, H03 |
| *(chờ CP5)* | *Thay đổi từ vòng validation với user thật* | *Điền sau phiên test* |
