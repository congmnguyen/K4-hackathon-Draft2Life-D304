# Reflection — Diệp Đức Lai (2A202601784)

> Bản thảo dựng từ việc thật trong repo. **Đọc lại và sửa cho khớp đúng những gì bạn đã làm** trước khi nộp —
> CP5/CP6 hỏi ngẫu nhiên "phần này hoạt động thế nào".

## 1. Vai trò và phần tôi làm

Tôi phụ trách **thứ người dùng nhìn thấy và thứ dùng để đo** — flow UI, golden set, và log validation.

| File | Phần của tôi |
|---|---|
| `codebase/index.html` | Toàn bộ flow 4 bước, render mặt bằng 2D + khối 3D isometric bằng SVG, 6 đường đi trải nghiệm |
| `eval/golden-set.jsonl` | 31 case tự xây, phủ đủ 4 lớp chỗ khó |
| `validation/feedback-log.md` | 5 biên bản phiên test, log nguyên văn |

**Ba quyết định của tôi:**

**(1) Vẽ 3D bằng SVG với phép chiếu isometric tự tính, không dùng thư viện.** Hàm `draw3d()` chiếu điểm
`(x, y, z)` xuống mặt phẳng bằng công thức `sx = (x−y)·cos30`, `sy = (x+y)·sin30 − z`, rồi sắp các mảng
tường theo độ sâu `(x+y)` để vẽ xa trước gần sau. Chọn cách này vì prototype phải mở được ngay, không cài
gì — và vì tôi phải giải thích được nó khi bị hỏi. Kéo three.js vào thì đẹp hơn nhưng thành hộp đen.

**(2) Mặt bằng A cố tình KHÔNG có phòng bếp.** Đây không phải thiếu sót. Có một phòng-không-tồn-tại nằm sẵn
trong mặt bằng thì mới demo được lớp ① — user gõ *"mở rộng phòng bếp"*, hệ thống phải nói không có và
**không dựng gì**. Nếu mặt bằng có đủ mọi phòng thì không có cách nào bày ra đường đi đó.

**(3) Golden set ghi sẵn đáp án mong đợi cho từng case, không chấm cảm tính.** Mỗi dòng có `expect_route`,
`expect_target`, và với case hiểm thì `expect_guard_block`. Nhờ vậy hai người chấm độc lập buộc phải ra
cùng kết quả — và nhờ vậy case N04 mới lòi ra (xem mục 3).

Độ phủ: ① 4 case · ② 4 · ③ 4 · ④ 4 · thường 11 · hiếm 4. **19/31 case lấy từ quan sát thực tế** — cách người
ta thật sự viết kích thước (`1m2`, `1m5`, `0.9m`, `1200mm`), tên phòng nhiều chữ, câu có từ lịch sự thừa,
gõ tiếng Anh xen tiếng Việt.

## 2. AI đã hỗ trợ tôi thế nào

Nhóm dùng **Claude Code**. Với phần của tôi, nó viết phần lớn `index.html` và dựng khung golden set.

**Chỗ nó giúp thật:** phép chiếu isometric và code sắp xếp độ sâu — tôi biết mình muốn nhìn thấy gì nhưng
không tự viết ra công thức được nhanh như vậy. Cả phần render lại khối 3D sau mỗi thay đổi cũng thế.

**Chỗ tôi phải can thiệp:**

1. **Bản đầu chỉ có happy path.** Bấm là ra kết quả, đẹp và vô dụng — vì đề bài chấm **4 đường đi trải
   nghiệm**, mà đường đáng giá nhất là lúc hệ thống **từ chối làm**. Tôi thêm 4 câu mẫu bấm được, mỗi câu
   đi một route khác nhau, để ai mở prototype cũng thấy ngay cả bốn đường mà không cần biết gõ gì.

2. **Golden set bản đầu toàn case dễ.** Toàn câu đủ tham số, chạy phát nào pass phát đó, nhìn số rất đẹp.
   Bộ đo kiểu đó không phát hiện được gì. Tôi thêm các case hiểm: đủ tham số nhưng phòng không tồn tại
   (L1-02), kích thước phi lý (L4-01, L4-02), prompt injection (H03), input rỗng (H04).

3. **Sau vòng validation tôi thêm case N11** — lấy **nguyên văn** câu anh Đức gõ ở phiên 5:
   `"Thêm cửa sổ 1200mm tường đông phòng khách"`. Case đến từ người dùng thật thì đắt hơn case tự nghĩ.

**Tôi kiểm chứng bằng cách nào:** bấm tay hết cả 4 route sau mỗi lần sửa, và đọc `eval/run-0*.md` xem case
nào đổi trạng thái giữa các lượt — L4-02 dao động qua lại nên tôi biết chỗ đó model không ổn định.

## 3. Một bài học từ case fail của chính nhóm

**Case N04 — bộ đo bắt được thứ mắt người và guard đều không bắt được.**

Case: `"thêm cửa sổ rộng 1,2 m ở tường nam phòng khách"`. Model trả `side = "N"` — nó đọc chữ **"nam"**
thành **"north"**. Cửa sổ mọc sai hẳn mặt nhà.

**Vì sao không ai thấy.** Nhìn màn hình thì thấy một cửa sổ, nằm trên một bức tường, kích thước 1,2 m —
đúng hết. Chỉ sai **mặt nào của căn hộ**. Guard cũng không bắt, vì `N` là giá trị hợp lệ, không có gì để
raise. Bấm tay hai chục lần cũng không phát hiện ra.

Nó lòi ra **chỉ vì** golden set ghi sẵn `expect_target.side = "S"`. Nếu bộ đo chỉ hỏi "có ra kết quả không"
thay vì "có ra **đúng** kết quả không" thì case này đã lọt thẳng vào bản demo.

**Bài học.** Trước đó tôi nghĩ golden set là thủ tục để lấy điểm R4. Case này cho thấy nó là **thứ duy nhất
bắt được loại lỗi mà kết quả trông đúng hoàn toàn**. Guard chặn được cái sai về cú pháp (phòng không tồn
tại, số phi lý) nhưng không chặn được cái sai về **nghĩa** — cái đó chỉ có đáp án ghi sẵn mới bắt được.

Chuyện thứ hai từ cùng một case: bản sửa N04 lại làm hỏng case L1-01 ở lượt 3 (D2 tụt xuống 29/30). Tức là
**sửa xong phải chạy lại trọn bộ**, không được chỉ chạy lại case vừa sửa. Nếu lượt 3 tôi chỉ kiểm mỗi N04
thì đã báo với nhóm là "sửa xong rồi" trong khi bản đó tệ hơn bản cũ.

**Lần sau tôi sẽ** viết golden set **trước** khi build xong UI, và mỗi case ghi rõ đáp án mong đợi ngay từ
đầu — thay vì build trước rồi mới nghĩ cách đo.

## 4. Nếu làm lại

**Tôi sẽ cho user thử sớm hơn, thay vì đợi đến khi prototype "xong".**

Vòng validation chạy gần cuối, nhưng nó lộ ra thứ mà cả nhóm ngồi với nhau cả ngày không thấy: **3/5 người
kẹt ở cách gõ kích thước**. Chị Lan nói *"em không biết gõ kiểu nào, 1m2 hay 1,2 hay 1200mm"*. Trong khi
nhóm thì gõ `1m2` cả trăm lần nên thấy hiển nhiên.

Đau hơn: thay đổi nhóm làm để chữa việc đó — thêm dòng gợi ý format — lại **hứa `1200mm` = 1,2 m trong khi
prompt chưa hề biết đơn vị mm**. Gọi AI thật để kiểm mới lộ, phải sửa prompt và thêm case N11.

Hai chuyện đó cùng một bài học: **nhóm không phải là user**, và **thứ mình vừa thêm vào cũng phải đem đi đo
lại** chứ không mặc nhiên là đúng. Một buổi chiều bấm thử với 5 người ngoài đáng giá hơn cả ngày nhóm tự
nhìn màn hình.
