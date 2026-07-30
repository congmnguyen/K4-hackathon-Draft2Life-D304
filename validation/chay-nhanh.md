# Chạy vòng validation trong 50 phút

> **ĐÃ CHẠY XONG** — 5/5 phiên Ngày 2 · 09:15–10:25. Log: `feedback-log.md` · danh sách: `willing-users.md`.
> File này giữ lại làm protocol (để giải thích cách nhóm chạy), không phải việc còn mở.

8 điểm R6. Cần **ít nhất 5 người ngoài nhóm × khoảng 10 phút**; trong đó có ít nhất
**2 willing user từ CP1**.

## Đường nhanh nhất: đổi chéo trong zone

Nhanh hơn gọi điện cho willing user rất nhiều — họ đang ngồi cùng phòng, và ai cũng cần đúng thứ này.

> Chào bạn, nhóm mình cần 5 người thử prototype 10 phút cho vòng validation.
> Đổi chéo nhé — bạn thử của mình, mình thử của bạn. Không cần chuẩn bị gì.

**Lưu ý rubric:** cần **≥2 người là willing user đã khai từ CP1**. Nên trộn: 2-3 người từ danh sách
109 người đã tick "muốn thử demo" trong khảo sát (gọi/nhắn trước), 2-3 người đổi chéo trong zone.

### Tin nhắn gửi willing user

> Chào anh/chị, em là nhóm Draft2Life — anh/chị có làm khảo sát về công cụ AI chuyển bản vẽ 2D sang 3D
> và tick là muốn thử bản demo ạ. Bản đầu tiên chạy được rồi, em xin 10 phút để anh/chị thử và góp ý.
> Anh/chị chỉ cần gõ một câu tiếng Việt mô tả thay đổi muốn làm, không cần cài gì.
> Em gọi lúc [giờ] được không ạ?

Làm được qua Google Meet/Zoom share màn hình — không cần gặp mặt.

## Chuẩn bị máy (2 phút, làm 1 lần)

```bash
cd /home/cong/code/K4-hackathon-Draft2Life-D304
export OPENAI_API_KEY="..."
python3 codebase/server.py --port 8000
```
Mở `http://127.0.0.1:8000`, bấm thử 1 câu cho chắc. Để nguyên tab đó, mỗi người thử vào lại từ bước 1.

## Thẻ điều phối — in ra hoặc để cạnh máy

**Nói đúng câu này rồi IM LẶNG:**

> "Bạn đang có mặt bằng căn hộ này. Hãy thêm một cửa sổ vào phòng khách."

**Trong lúc họ làm — không nói gì cả.** Không gợi ý, không giải thích, không cứu khi họ kẹt.
Chỗ họ kẹt chính là dữ liệu. Người log ghi:
- họ gõ gì — **chép nguyên văn, kể cả sai chính tả**
- kẹt ở đâu, bao lâu
- có đọc bảng thông số không, có bấm Hoàn tác không

**Xong task, hỏi đúng 3 câu — không thêm câu nào:**

1. Điều gì khó hiểu hoặc khó chịu nhất?
2. Kết quả này bạn có tin không — vì sao?
3. Bạn có dùng thật không — vì sao / vì sao chưa?

**Chép nguyên văn câu trả lời.** Không tóm tắt, không sửa cho hay.

> Nếu cả 5 người đều khen thì phiên test hỏng. Giao task khó hơn:
> *"Giờ thử bảo nó tính giúp bạn chi phí sửa"* hoặc *"thử thêm cửa vào phòng bếp"*.

## Sau mỗi phiên — điền ngay 1 biên bản

Vào `validation/feedback-log.md`, đừng để dồn cuối buổi rồi nhớ nhầm.

Mỗi biên bản đã có sẵn trường cho tên/vai, nguồn willing user, câu đã gõ, thời gian ra kết quả,
quan sát, ba quote nguyên văn và mức nghiêm trọng.

## Sau khi xong 5 phiên (10 phút)

1. Điền bảng chủ đề lặp, kiểm tra giả thuyết và bảng quyết định cuối `feedback-log.md`.
2. Đối chiếu **ngưỡng đã đặt trước**: ≥3/5 người phàn nàn bị hỏi lại quá nhiều → xem lại ranh giới
   conditional trong `spec.md` §4. Đây là ngưỡng ghi trước khi test, không được sửa sau khi nghe feedback.
3. Chọn **1-2 thay đổi** làm trước demo → chép sang `spec.md` §9 Changelog.
   *(Rubric R6 cho 4 điểm cho ý này. Giữ nguyên cũng được — nhưng phải có lý do căn cứ, không phải "không kịp".)*
4. Điền 2 quote nguyên văn vào **slide 5** (`demo/slides.html`), render lại:
   `node pdf.mjs` hoặc mở slides.html rồi Ctrl+P → Save as PDF.
5. Cập nhật `README.md` khối R6 và `validation/willing-users.md`.

## Phân vai

| Vai | Người |
|---|---|
| Điều phối, giao task, hỏi 3 câu | Nguyễn Văn Sáng |
| Log nguyên văn, bấm giờ | Diệp Đức Lai |
| Trực máy, xử lý nếu prototype lỗi | Nguyễn Minh Công |

Với đúng bộ ba vai trên, chạy tuần tự 5 phiên mất khoảng 50 phút. Chỉ chạy hai phiên song song
khi có thêm một điều phối viên và một người log độc lập cho phiên thứ hai; không để một người vừa
điều phối vừa ghi hai phiên.
