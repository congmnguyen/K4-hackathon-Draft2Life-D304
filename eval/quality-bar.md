# Quality bar — chốt trước lượt đo chính thức

> Bar này được chưng cất từ **lượt 1** (`run-01.md`, 24/30 = 80,0%) — đúng quy trình
> guide §2.6.1: chạy bộ input thật, đọc từng output, đặt tên cho lỗi, rồi mới định
> nghĩa "tốt". Từ thời điểm này bar **giữ nguyên**, kể cả khi số đo thấp hơn.
> Bản chính thức nằm trong `spec.md` §7 (hạn cứng 23:59 N1).

## Ba chiều chất lượng

| Chiều | Định nghĩa kiểm chứng được (người ngoài nhóm chấm ra cùng kết quả) |
|---|---|
| **D1 · Route đúng** | Route trả về khớp đúng route mong đợi ghi sẵn trong golden set |
| **D2 · Không bịa nguồn** | Không xuất hiện `room_id` nằm ngoài mặt bằng đang mở |
| **D3 · Tham số đúng** | `apply` thì cả 4 tham số khớp giá trị mong đợi; case có kích thước phi lý thì guard **phải** chặn |

**Case đạt = pass cả 3 chiều.** Chấm bằng `scripts/run_eval.py`, không chấm cảm tính.

## Bar

> **Đạt khi ≥ 85% case qua trọn bộ golden set, VÀ thoả 2 điều kiện cứng:**
>
> 1. **D2 = 100%** — không một case nào để lọt phòng không có trên mặt bằng.
> 2. **Không case `apply` nào lọt guard với tham số phi lý** — kích thước ngoài
>    khoảng hợp lệ của loại phần tử phải bị chặn, không được dựng.

## Vì sao đặt bar ở đây

Hai điều kiện cứng ở mức tuyệt đối vì đây là **lớp ① và lớp ④** — sai ở đây thì con
số phi lý đi thẳng vào hồ sơ người dùng xuất ra, hậu quả là tiền vật tư và điểm đồ án
(xem cost-of-error trong canvas). Còn 85% cho D1: route sai kiểu "hỏi lại khi lẽ ra
làm được" chỉ tốn người dùng thêm một lượt gõ — khó chịu, không nguy hiểm — nên chấp
nhận một tỉ lệ nhất định.

Ngưỡng 85% chọn từ quan sát lượt 1: 80% với 4/6 failure cùng một nguyên nhân duy nhất
(không đọc được kích thước dạng "1m5"), tức là sửa đúng một chỗ thì bar này với tới được.
