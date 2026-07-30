# Feedback log — vòng validation với user thật

> **TRẠNG THÁI: CHƯA CHẠY.** Bảng dưới đây là khung, chưa có dòng dữ liệu nào.
> Đây là phần **duy nhất trong repo không thể làm bằng code** — cần 5 người thật ngồi thử.
> Điền xong thì xoá dòng cảnh báo này và cập nhật `README.md` (khối R6) + `spec.md` §9.

## Cách chạy một phiên — 10 phút/người

1. **Giao task thật, rồi im lặng quan sát.** Không thuyết minh, không gợi ý.
   > *"Bạn đang có mặt bằng căn hộ này. Hãy thêm một cửa sổ vào phòng khách."*

   Ghi lại: họ gõ gì **nguyên văn** · kẹt ở đâu · bao lâu mới ra kết quả đầu tiên · có đọc bảng thông số không.

2. **Hỏi đúng 3 câu này, không thêm:**
   - *"Điều gì khó hiểu hoặc khó chịu nhất?"*
   - *"Kết quả này bạn có tin không — vì sao?"*
   - *"Bạn có dùng thật không — vì sao / vì sao chưa?"*

3. **Log nguyên văn.** Không tóm tắt, không làm đẹp câu chữ của người thử.

**Nếu mọi phản hồi đều là lời khen thì phiên test chưa đạt** — giao task khó hơn hoặc đổi người thử.

## Ai làm gì

| Vai | Người |
|---|---|
| Điều phối phiên, giao task, hỏi 3 câu | **Nguyễn Văn Sáng** |
| Log nguyên văn, bấm giờ | **Diệp Đức Lai** |
| Trực máy, xử lý nếu prototype lỗi | **Nguyễn Minh Công** |

## Bảng log

| # | Người thử (tên / vai — willing user?) | Task | Quan sát (họ gõ gì, kẹt đâu) | Quote nguyên văn | Mức nghiêm trọng |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

*Mức nghiêm trọng: **chặn** (không hoàn thành được task) · **khó chịu** (làm được nhưng bực) · **góp ý** (nice-to-have).*

## Tổng hợp — điền sau khi xong 5 phiên

- **Chủ đề lặp nhiều nhất:**
- **1-2 thay đổi làm trước demo** *(→ chép sang `spec.md` §9 Changelog)*:
- **Giữ nguyên có lý do:**
- **Đưa vào backlog** *(→ slide 6)*:

## Giả thuyết nhóm muốn bị phá

Nhóm tin route `clarify` — hỏi lại thay vì đoán — là **tính năng**. User rất có thể thấy nó là **phiền**.

**Ngưỡng tự đặt trước khi test:** nếu **≥3/5 người** phàn nàn bị hỏi lại quá nhiều thì đó là tín hiệu
phải xem lại ranh giới conditional trong `spec.md` §4, không phải lỗi giao diện.

Ghi ngưỡng ra đây **trước** khi chạy để không tự bẻ cong kết luận sau khi nghe feedback.
