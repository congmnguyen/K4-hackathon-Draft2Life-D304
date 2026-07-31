# Demo script — 5 phút trình bày + 5 phút Q&A

Mỗi thành viên nói ≥1 phần (luật CP6). Bấm giờ từng chặng khi dry run, chặng nào tràn thì cắt chữ chứ
đừng cắt con số.

## Trước khi lên

```bash
export OPENAI_API_KEY="..."
python3 codebase/server.py --port 8000
```
- Mở sẵn `http://127.0.0.1:8000` ở **tab 1**, đã chọn mặt bằng **Căn hộ 48 m²**, đứng ở bước 3.
- Mở sẵn `demo-slides.pdf` ở **tab 2**.
- **Bấm thử 1 câu trước khi lên** để chắc key còn sống và mạng ổn. Latency thật ~7 giây — đừng hoảng.
- Backup nếu live hỏng: `demo/slide-*.png` + screenshot kết quả trong máy.

## Phân chặng

| # | Slide | Ai nói | Thời lượng | Nội dung |
|---|---|---|---|---|
| 1 | 1 · User & Job | **Sáng** | 45" | Job executor + con số pain |
| 2 | 2 · Vì sao chọn | **Sáng** | 45" | Bảng impact 3 ứng viên + ứng viên loại |
| 3 | 3 · Giải pháp & demo live | **Lai** (bấm) + **Công** (giải thích) | 2'00" | Lát cắt + automation + 2 case live |
| 4 | 4 · Kết quả đo | **Công** | 45" | 5 lượt + failure đáng kể nhất |
| 5 | 5 · User thật nói gì | **Lai** | 45" | 2 quote + thay đổi đã làm |
| 6 | 6 · Nếu có thêm 1 tuần | **Công** | 30" | 3 việc + bài học |

---

## Chặng 1 — Sáng · 45 giây

> "Người dựng mô hình 3D không tắc ở lúc dựng. Họ tắc ở lúc **sửa**.
>
> Nhóm khảo sát **123 người ngoài nhóm** — 70 sinh viên kiến trúc, 53 KTS đã đi làm.
> **98 trên 123, tức 79,7%, phải chỉnh sửa chi tiết cửa tường nội thất nhiều lần** khi dựng 3D.
> 63,4% mất từ 3 ngày trở lên cho một mô hình.
>
> Và khó khăn lớn nhất họ tự chọn không phải là thiếu ý tưởng thiết kế — mà là **bản thân phần mềm**:
> 37 người chọn 'sử dụng phần mềm thiết kế 3D'.
>
> Job của họ: vừa nghĩ ra một thay đổi thì muốn thấy ngay nó trông thế nào, để quyết giữ hay bỏ,
> mà không mất nửa buổi thao tác."

## Chặng 2 — Sáng · 45 giây

> "Nhóm cân nhắc 3 ứng viên, cùng rút từ một bộ 123 người nên so trực tiếp được.
>
> **Loại B** — dựng 3D lần đầu — dù 122/123 người gặp, pain to nhất. Vì lời giải là computer vision
> hình học, không build nổi trong 1,5 ngày. Và làm ẩu thì phần AI chỉ còn là 'upload rồi chờ' —
> **không có quyết định AI nào để soi 4 lớp chỗ khó**.
>
> **Loại C** — bắt lỗi mô hình — bằng chứng yếu nhất, 26%. Muốn bắt lỗi đúng thì nguồn sự thật phải
> là quy chuẩn xây dựng, nhóm không có bản kiểm chứng được.
>
> **Chọn A** — vòng lặp sửa chi tiết: phủ rộng gấp 3 lần C, lặp trong từng mô hình, và là ứng viên
> duy nhất có một quyết định AI tách bạch được."

## Chặng 3 — Lai bấm, Công giải thích · 2 phút

**Công nói lát cắt (20"):**
> "Một câu: sinh viên kiến trúc gõ một câu tiếng Việt mô tả chi tiết muốn sửa,
> **AI quyết định câu đó đã đủ tham số để thực thi hay còn thiếu**, trả về mô hình đã cập nhật
> kèm thông số, hoặc đúng một câu hỏi làm rõ.
>
> Mức automation là **Conditional**, và ranh giới đặt theo cost-of-error:
> dựng sai hình khối thì user thấy ngay, bấm hoàn tác — sửa rẻ, cho AI làm.
> AI tự đoán kích thước user chưa nói thì con số bịa trông y hệt số thật, mang đi xuất hồ sơ nộp đồ án —
> sửa đắt, tuyệt đối không cho AI làm."

**Case 1 — chuẩn (40"). Lai gõ:**
```
Thêm một cửa sổ rộng 1m2 ở tường phía tây phòng khách
```
> **Công:** "Đây là lời gọi AI thật, `gpt-4.1-mini`. Nó rút ra 4 tham số: cửa sổ, phòng khách,
> tường tây, 1,2 mét — chú ý `1m2` trong tiếng Việt là 1 mét 2 tấc, không phải 1,2 mét vuông.
> Khối 3D cập nhật ngay, và bảng thông số hiện đúng 4 tham số AI đã dùng, kèm dòng
> **'kiểm lại trước khi xuất hồ sơ'**."

**Case 2 — chỗ khó (50"). Lai gõ:**
```
thêm cửa đi rộng 0.4m ở tường phía bắc phòng ngủ
```
> **Công:** "Câu này đủ cả 4 tham số. AI trả về `apply` — nó định dựng.
> Nhưng **guard chặn**: cửa đi 0,4 mét thì không ai đi lọt. **Không dựng gì lên mô hình.**
>
> Đây là chỗ nhóm muốn các thầy cô chú ý: guard là code, không phải prompt.
> Prompt là lời khuyên, model nghe hay không tuỳ nó. Guard đối chiếu bằng code và chặn thật."

*(Nếu còn giờ, gõ thêm `mở rộng phòng bếp thêm 2m` → mặt bằng không có bếp → không dựng.)*

## Chặng 4 — Công · 45 giây

> "Quality bar nhóm chốt từ lượt đo đầu và giữ nguyên: **≥85%, cộng 2 điều kiện cứng** —
> không case nào bịa phòng, và không case nào lọt guard với tham số phi lý.
>
> 5 lượt: 80,0% → 90 → 90 → 96,7 → **100%** trên 31 case.
>
> Nhưng con số không phải phần đáng kể nhất. **Lượt 3 nhóm đạt 90% nhưng trượt điều kiện cứng.**
> Nhóm vừa sửa được case nguy hiểm nhất — model đọc 'tường **nam**' thành hướng Bắc, cửa mọc sai mặt nhà,
> guard không bắt được vì N vẫn là giá trị hợp lệ. Chính bản sửa đó lại làm guard chặn nhầm
> một câu trả lời **đúng**.
>
> **Ba lần sửa thì hai lần lỗi nằm ở phía nhóm, không phải ở model.** Nhìn % thì cả ba lần đều bị bỏ sót."

## Chặng 5 — Lai · 45 giây

> "5 người ngoài nhóm đã thử — 3 willing user từ khảo sát CP1, 2 người đổi chéo zone.
>
> Anh Hùng, KTS dùng 3ds Max: *'Tin hơn mấy tool ra ảnh đẹp. Vì nó ghi rõ 1,2 m tường tây phòng khách —
> sai thì em thấy ngay, bấm hoàn tác được.'*
>
> Bạn Trang: *'Hỏi lại hơi nhiều. Task bảo phòng khách rồi mà mình gõ thêm cửa sổ nó vẫn hỏi phòng nào.'*
>
> **Đã sửa:** 3/5 người kẹt ở cách gõ kích thước → thêm gợi ý format và 3 chip bấm nhanh.
> **Giữ nguyên có lý do:** route hỏi lại — chỉ 2/5 phàn nàn, dưới ngưỡng 3/5 nhóm chốt **trước** khi test.
>
> Và chính thay đổi đó lộ ra một lỗi: gợi ý mới hứa `1200mm` = 1,2 m, nhưng prompt chưa hề biết
> đơn vị mm. **Giao diện hứa thứ hệ thống chưa làm được.** Sửa xong mới ra 100%."

## Chặng 6 — Công · 30 giây

> "Ba việc nếu có thêm một tuần: **export ra SketchUp/Revit** — 3/5 người thử chặn 'dùng thật' đúng ở đó;
> **guard ngữ nghĩa cho mọi tham số**, hiện mới áp cho hướng; **làm mềm copy** khi từ chối.
>
> Bài học lớn nhất: nhóm khởi đầu với giả định người dùng là chủ hộ sắp sửa nhà. Đọc 123 câu trả lời
> thì **không có một chủ hộ nào**. Thứ nghe hợp lý mà không ai kiểm là thứ nguy hiểm nhất —
> đúng với giả định về người dùng, với khoảng kích thước trong guard, và với dòng gợi ý trên giao diện."

---

## Q&A — 5 phút

**Thẻ giám khảo: chạy 1 case lạ tại chỗ.** Ai cũng phải sẵn sàng bấm. Nếu ra kết quả lạ thì **đọc khối
trace** (route / model / guard) và giải thích, đừng chống chế.

| Câu hỏi | Ai trả lời | Trả lời gọn |
|---|---|---|
| "Augment hay automate — vì sao?" | Công | Conditional. Ranh giới theo cost-of-error: sai hình khối sửa rẻ (thấy ngay + hoàn tác) → AI làm; tự đoán tham số sửa đắt (số bịa vào hồ sơ) → chuyển về người |
| "Failure nguy hiểm nhất?" | Công | Case N04 — đọc "tường nam" thành hướng Bắc. Tệ vì **kết quả trông đúng hoàn toàn**, guard không bắt được vì N là giá trị hợp lệ. Chỉ golden set có đáp án ghi sẵn mới bắt ra |
| "Con số 79,7% đếm thế nào?" | Sáng | 98/123 dòng CSV, đếm trực tiếp trên cột lựa chọn, không loại dòng nào. Log nguyên văn 123 câu trả lời ở `evidence/survey-log.md`, chạy lại bằng `scripts/analyze_survey.py` |
| "Vì sao mặt bằng A không có phòng bếp?" | Lai | Cố ý. Phải có một phòng-không-tồn-tại thì mới demo được lớp ① — user gõ "phòng bếp", hệ thống nói không có và không dựng |
| "Phần nào còn mock?" | Lai | Upload bản vẽ 2D thật (dùng 2 mặt bằng dựng sẵn) và nút xuất hồ sơ. Khai rõ trong `codebase/README.md` và in ngay trong khối trace |
| "Sao không dùng data pack của khoá?" | Sáng | Hướng C, domain kiến trúc — chatlog VLearn không dùng được. Nhóm tự thu khảo sát 123 người |
| "31 case có tự chấm dễ không?" | Lai | Mỗi case ghi sẵn `expect_route` + `expect_target`, chấm bằng `scripts/run_eval.py` chứ không chấm tay. Không case nào bị sửa expectation qua 5 lượt |

## Checklist dry run

- [ ] Bấm giờ tổng — mục tiêu **đúng 5 phút**, không quá
- [ ] Chặng 3 chạy live thật, không nói chay
- [ ] Mỗi người nói ít nhất một chặng
- [ ] Thử ngắt giữa chừng hỏi một câu Q&A xem có trả lời được không
- [ ] Backup screenshot đã mở sẵn
