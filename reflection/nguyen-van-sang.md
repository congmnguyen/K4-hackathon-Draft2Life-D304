# Reflection — Nguyễn Văn Sáng (2A202601252)

> Bản thảo dựng từ việc thật trong repo. **Đọc lại và sửa cho khớp đúng những gì bạn đã làm** trước khi nộp —
> CP5/CP6 hỏi ngẫu nhiên "phần này hoạt động thế nào".

## 1. Vai trò và phần tôi làm

Tôi phụ trách **bằng chứng** — khối R1, 15 điểm, và là thứ mọi quyết định còn lại của nhóm đứng lên trên.

| File | Phần của tôi |
|---|---|
| `scripts/analyze_survey.py` | Script đọc CSV khảo sát → số tổng hợp + log nguyên văn, tự động loại PII |
| `evidence/survey-results.json` | Số liệu tổng hợp |
| `evidence/survey-log.md` | Log đầy đủ 14 câu hỏi × 123 câu trả lời nguyên văn, mã hoá R001–R123 |
| `spec.md` §1–§2 | Problem statement, bảng evidence, bảng impact 3 ứng viên |

**Hai quyết định của tôi:**

**(1) Không chép tay số liệu — viết script.** Chuẩn Đường A đòi *"log đủ câu hỏi + từng câu trả lời nguyên
văn"*. 123 người × 14 câu = 1.722 ô. Chép tay thì vừa lâu vừa sai, và người chấm không kiểm lại được.
Script chạy một lệnh ra cả `survey-results.json` lẫn `survey-log.md` — ai cũng tái tạo được từ file gốc.

**(2) PII phải chặn bằng code, không bằng trí nhớ.** File gốc có họ tên, email, số điện thoại của 123 người.
Repo lại là public. Nên script có `assert` quét lại output: nếu tên cột PII hoặc bất kỳ **giá trị** PII nào
lọt vào file sinh ra thì script **dừng ngay**, không ghi file. Cộng thêm `.gitignore` chặn `*.csv`.
Tôi không muốn phần an toàn phụ thuộc vào việc mình có nhớ xoá cột hay không.

**Bảng impact:** tôi rút cả 3 ứng viên từ **cùng một bộ 123 người** để so trực tiếp được — 98/123 (79,7%)
cho ứng viên A, 122/123 cho B, 32/123 (26%) cho C. Điểm mấu chốt là ghi rõ lý do loại B dù nó là pain to
nhất: build không nổi trong 1,5 ngày, và quan trọng hơn là **không có quyết định AI nào tách bạch để soi
4 lớp chỗ khó**.

## 2. AI đã hỗ trợ tôi thế nào

Nhóm dùng **Claude Code** cho phần lớn việc build. Với phần của tôi, nó viết `analyze_survey.py` và dựng
bảng evidence trong spec.

**Chỗ nó giúp thật:** phần đếm và sinh log. Đây là việc máy làm đúng hơn người — 1.722 ô, không sai sót,
chạy lại bao nhiêu lần cũng ra cùng kết quả. Nếu tôi ngồi Excel thì vừa lâu vừa không ai kiểm chéo được.

**Chỗ tôi phải can thiệp:**

1. **Bản đầu chỉ sinh `survey-results.json` — số tổng hợp, không có log nguyên văn.** Đọc kỹ rubric R1 thì
   thấy chuẩn Đường A đòi *"log đủ câu hỏi + từng câu trả lời nguyên văn"*. Thiếu file đó là mất 6 điểm dù
   nhóm có đủ 123 người. Phải bổ sung `survey-log.md`.

2. **Số liệu chỉ ra cái khác với thứ nhóm đang định làm.** Lúc đầu nhóm nhắm người dùng là chủ hộ sửa nhà.
   Đếm ra: 70 sinh viên + 53 KTS, **không một chủ hộ nào**. Và pain lớn nhất không phải "dựng 3D khó" mà là
   **79,7% phải sửa đi sửa lại**. Nhóm phải đổi cả job executor lẫn lát cắt.

**Tôi kiểm chứng bằng cách nào:** tôi mở `evidence/survey-log.md` đọc thẳng các bản ghi R001, R002 và mấy
câu trả lời tự do lạ (`"Solidword, Fushion"`, `"Canva"`, `"Không dùng gì"`) để đối chiếu với con số tổng hợp.
Số và log phải khớp nhau thì mới dám đưa vào spec.

## 3. Một bài học từ case fail của chính nhóm

**Nhóm suýt build đúng sản phẩm cho sai người.**

Ngày đầu nhóm chốt rất nhanh: người dùng là **chủ hộ sắp sửa nhà**, cần công cụ hình dung không gian trước
khi gọi thợ. Câu chuyện trơn tru, ai nghe cũng gật. Nhóm còn có sẵn 8 file phỏng vấn offline — chủ nhà hàng,
lễ tân khách sạn, quản lý, nhân viên BĐS — nghe càng khớp.

Đến lúc tôi mở file khảo sát 123 người ra đếm thì con số nói khác hẳn: **70 sinh viên kiến trúc + 53 KTS
đã đi làm, không có chủ hộ nào**. Bộ câu hỏi khảo sát ngay từ đầu đã hỏi *"bạn thường dùng phần mềm nào
(AutoCAD, Revit, SketchUp…)"* — tức là đối tượng thật sự luôn là dân trong nghề.

**Vì sao nhóm không thấy sớm.** Nhóm đã có dữ liệu **từ trước khi bắt đầu**. Nhưng nhóm dùng nó sai thứ tự:
chốt ý tưởng trước, rồi mới đi tìm số liệu chống lưng. 8 phỏng vấn offline củng cố giả định sai, vì nó là
mẫu nhóm tự chọn — hỏi người quen thì ra người quen, không ra người dùng.

**Bài học.** Bằng chứng chỉ có giá trị khi nó **được đọc trước lúc quyết định** và có quyền lật ngược quyết
định đó. Đọc sau thì nó chỉ còn là đồ trang trí cho thứ nhóm đã muốn làm.

Hệ quả thật: nhóm phải viết lại toàn bộ canvas CP1 giữa chừng. Và tôi ghi thẳng vào `spec.md` §1 rằng
8 phỏng vấn offline **chưa gỡ băng nên không dùng làm bằng chứng chính** — thà khai ít mà chắc.

## 4. Nếu làm lại

**Tôi sẽ đọc dữ liệu trước, và đọc log nguyên văn chứ không chỉ nhìn biểu đồ tổng hợp.**

Google Form tự vẽ sẵn biểu đồ tròn cho từng câu — nhìn rất tiện, và chính vì tiện nên dễ dừng ở đó. Nhưng
mấy thứ hữu ích nhất chỉ hiện ra khi đọc từng dòng: có người gõ `"Solidword, Fushion"` sai chính tả, có
người trả lời `"Canva"` ở câu phần mềm thiết kế, có người `"Không dùng gì"`. Ba dòng đó nói rằng người dùng
không đồng nhất như biểu đồ trông có vẻ — và nhóm không nên khoá cứng vào một phần mềm nào.

Cụ thể lần sau: **đọc 30–50 mẫu trước, đếm sau** — đúng thứ tự guide đã dặn mà nhóm làm ngược.
