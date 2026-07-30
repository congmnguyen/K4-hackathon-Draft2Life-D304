# Reflection — Nguyễn Minh Công (2A202601945)

> **Bản nháp khung — người có tên tự viết lại bằng lời của mình.**
> Rubric reflection chấm riêng. **Vibe-coding rule:** bị hỏi ngẫu nhiên tại CP5/CP6 mà không giải thích
> được phần có tên mình thì phần đó 0 điểm. Đừng nộp bản khung này nguyên xi.

## 1. Vai trò và phần tôi làm

Lát cắt & automation · spec.md · prompt.py + decide.py (lời gọi AI thật + guard)

*(Viết cụ thể: file nào, quyết định nào là của bạn, chỗ nào bạn tự nghĩ ra chứ không phải AI gợi ý.)*

## 2. AI đã hỗ trợ tôi thế nào

*(Cụ thể: dùng công cụ gì, cho việc gì, chỗ nào bạn phải sửa lại output của AI vì nó sai hoặc không hợp.
Tránh viết chung chung kiểu "AI giúp code nhanh hơn".)*

## 3. Một bài học từ case fail của chính nhóm

*(Chọn MỘT case thật trong `eval/` hoặc một quyết định nhóm đã phải đảo ngược. Gợi ý — chọn cái bạn
thật sự hiểu, vì có thể bị hỏi lại:)*

- **Đổi job executor sau khi đọc khảo sát** — nhóm bắt đầu với giả định "chủ hộ sắp sửa nhà";
  123 câu trả lời không có một chủ hộ nào, toàn sinh viên kiến trúc và KTS.
- **Case N04** — model đọc "tường **nam**" thành hướng Bắc. Guard không bắt được vì N vẫn là giá trị
  hợp lệ, chỉ sai ngữ nghĩa. Loại lỗi tệ nhất: kết quả trông đúng hoàn toàn.
- **Lượt eval 3** — bản sửa N04 lại làm vỡ điều kiện cứng D2, vì guard chặn nhầm ở route `no_evidence`.
  Hai lần sửa thì một lần lỗi nằm ở guard nhóm tự viết, không phải ở model.
- **Case L4-01** — cửa đi 0,4 m lọt qua guard vì khoảng kích thước để chung cho mọi loại phần tử.

*(Viết: chuyện gì xảy ra → tại sao nhóm không thấy trước → lần sau bạn sẽ làm khác thế nào.)*

## 4. Nếu làm lại

*(Một điều duy nhất bạn sẽ làm khác.)*
