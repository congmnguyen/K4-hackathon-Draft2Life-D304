# Reflection — Nguyễn Minh Công (2A202601945)

## 1. Vai trò và phần tôi làm

Lead nhóm. Tôi chịu trách nhiệm **quyết định trung tâm của sản phẩm** — phần AI thật sự làm việc.

| File | Tôi quyết cái gì |
|---|---|
| `codebase/prompt.py` | Hợp đồng 4 route (`apply` / `clarify` / `no_evidence` / `out_of_scope`) và luật tuyệt đối: **không bao giờ tự điền tham số người dùng chưa nói** |
| `codebase/decide.py` | Lời gọi OpenAI thật + hàm `guard()` — lớp kiểm lại kết quả AI bằng code |
| `spec.md` | Toàn bộ 9 mục, đặc biệt §4 (lát cắt, automation) và §5 (4 lớp chỗ khó) |

**Quyết định thiết kế quan trọng nhất: chọn mức Conditional, và đặt ranh giới ở đâu.**

Lý lẽ là cost-of-error, không phải "cho tiện":
- AI dựng sai hình khối → user **thấy ngay trên màn hình**, bấm Hoàn tác. Sửa rẻ → cho AI tự làm.
- AI **tự đoán kích thước user chưa nói** → con số bịa trông y hệt con số thật, user không có cách nào
  biết → mang đi xuất hồ sơ nộp đồ án. Sửa đắt → tuyệt đối không cho AI làm.

Ranh giới nằm đúng chỗ đó: **đủ 4 tham số thì tự làm, thiếu một tham số thì chuyển về người.**

**Quyết định thứ hai: không tin model tự giác, kiểm lại bằng code.** Prompt bảo model đừng bịa phòng —
nhưng prompt là lời khuyên, không phải ràng buộc. `guard()` đối chiếu `room_id` với mặt bằng thật và chặn
kích thước phi lý theo từng loại phần tử. Vi phạm thì **không dựng gì lên mô hình**.

**Quyết định thứ ba: `clarify` chỉ hỏi MỘT câu, không hỏi hết tham số thiếu một lượt.** Hỏi ba câu cùng lúc
thì thành cái form, mà form thì user đã có sẵn trong Revit rồi — họ đến đây để gõ một câu. Nên prompt xếp
thứ tự ưu tiên `element → room_id → side → width_m` và chỉ hỏi cái thiếu quan trọng nhất.

## 2. AI đã hỗ trợ tôi thế nào

Nhóm dùng **Claude Code** để build gần như toàn bộ codebase, spec và bộ đo. Tôi nói thẳng vì đó đúng là câu
hỏi đề bài đang hỏi, và vì phần đáng kể không nằm ở chỗ AI viết được bao nhiêu dòng.

**Chỗ AI làm tốt:** dựng khung nhanh — flow 4 bước, render SVG 2D/3D, server stdlib, script chạy eval sinh
bảng markdown. Những thứ tôi biết phải làm gì nhưng gõ tay thì mất cả buổi.

**Chỗ tôi phải bác lại nó — quan trọng hơn:**

1. **Nó đề xuất sai người dùng.** Vòng đầu nó chốt job executor là "chủ hộ sắp sửa nhà", nghe rất hợp lý.
   Tôi đưa file khảo sát 123 người vào, đọc lại thì **không có một chủ hộ nào** — 70 sinh viên, 53 KTS.
   Toàn bộ canvas phải viết lại. Nếu tôi gật đầu ở đó thì nhóm build đúng sản phẩm cho sai người.

2. **Nó viết `guard()` với một khoảng kích thước chung `0,3–6,0 m` cho mọi loại phần tử.** Nghe hợp lý,
   chạy eval mới lộ cửa đi 0,4 m lọt qua — không ai đi lọt cửa 40 phân. Phải tách khoảng theo từng loại.

3. **Nó đề nghị viết feedback log validation từ file CSV khảo sát cho nhanh.** Cái này tôi để nó từ chối —
   và nó đúng: R6 đòi tên/vai từng người thử, CP5 lại có mục hỏi ngẫu nhiên. Nhóm đi chạy 5 phiên thật.

**Tôi kiểm chứng bằng gì:** tôi không tin con số % của bảng eval. Mỗi lượt tôi mở
`codebase/logs/ai_trace.jsonl` đọc `raw_output` của những case fail để biết model **nghĩ gì** rồi mới quyết
sửa prompt hay sửa guard. Hai lỗi đáng kể nhất của cả dự án đều tìm ra theo đường đó, không phải từ con số.

## 3. Một bài học từ case fail của chính nhóm

**Case N04 → lượt eval 3 → lượt eval 4.**

**Chuyện gì xảy ra.** Golden set có case `"thêm cửa sổ rộng 1,2 m ở tường nam phòng khách"`. Model trả về
`side = "N"` — nó đọc chữ **"nam"** thành **"north"**. Cửa sổ mọc sai hẳn mặt nhà.

**Vì sao suýt không thấy.** `guard()` không bắt được, vì `N` **là** một giá trị hợp lệ. Không exception,
không cảnh báo, JSON đẹp đẽ. Đây là loại lỗi tệ nhất: **kết quả trông đúng hoàn toàn**. Chỉ vì golden set
ghi sẵn đáp án mong đợi nên mới lòi ra.

**Sửa thế nào.** Hai lớp: (1) gọi thẳng tên cái bẫy trong prompt — *"nam" → S, chữ "nam" tiếng Việt nghĩa là
SOUTH*; (2) bắt model trả thêm trường `side_source` trích **nguyên văn** cụm chữ chỉ hướng, rồi `guard()`
map lại bằng code và đối chiếu. Không tin model tự khai.

**Rồi bản sửa đó làm vỡ điều kiện cứng.** Lượt 3 vẫn 90% nhưng D2 tụt xuống 29/30 — trượt điều kiện
"không bịa nguồn = 100%". Case `"mở rộng phòng bếp"`: model trả **đúng** `no_evidence` với lý do
*"Mặt bằng không có phòng bếp"*, nhưng điền `room_id="bep"` để **gọi tên** cái phòng không tồn tại.
`guard()` của tôi chặn mọi `room_id` ngoài mặt bằng ở **mọi** route → chặn nhầm chính câu trả lời đúng.

**Bài học.** Hai lần trong năm lượt đo, lỗi nằm ở **guard tôi tự viết**, không ở model. Tôi vào việc với
định kiến "model hay bịa, mình phải canh nó" — hoá ra lớp canh cũng sai được, và sai theo kiểu tự tin hơn.

Cụ thể: tôi viết `guard()` như một cái lưới chặn đặt ngoài, không nghĩ theo từng route. Nhưng cùng một
dữ kiện — `room_id` không có trên mặt bằng — mang **hai nghĩa trái ngược** tuỳ route: ở `apply` là bịa,
ở `no_evidence` là nội dung câu trả lời. Luật kiểm phải gắn với ngữ cảnh, không áp phẳng được.

**Lần sau tôi sẽ** viết case kiểm cho **chính lớp guard** trước khi tin nó, chứ không chỉ viết case kiểm cho
model. Và mỗi lần sửa xong chạy lại **trọn bộ** — lượt 3 nếu chỉ chạy lại mỗi N04 thì đã ship một bản tệ
hơn mà tưởng là tốt hơn.

## 4. Nếu làm lại

**Tôi sẽ đọc dữ liệu trước khi build, không phải ngược lại.**

Nhóm có sẵn file khảo sát 123 người **từ đầu** — nó nằm trong máy tôi suốt. Nhưng tôi vào việc bằng cách
chốt ý tưởng rồi mới đi tìm số liệu chống lưng cho ý tưởng đó. Kết quả: job executor sai, lát cắt sai, phải
viết lại canvas giữa chừng.

Cái đáng nói không phải là mất thời gian — mà là **tôi suýt không phát hiện ra**. Giả định "chủ hộ sắp sửa
nhà cần công cụ dựng 3D" nghe rất thuyết phục, ai nghe cũng gật. Nếu hôm đó tôi không mở file CSV ra đếm
thì nhóm đã mang một câu chuyện hợp lý và sai đi thi.

Đó cũng đúng là bài học lặp lại ở phần kỹ thuật: **thứ nghe hợp lý mà không ai kiểm là thứ nguy hiểm nhất** —
giả định về người dùng, khoảng kích thước trong guard, hay dòng gợi ý UI hứa `1200mm` mà prompt chưa hề
hỗ trợ. Ba lỗi khác nhau, cùng một gốc.
