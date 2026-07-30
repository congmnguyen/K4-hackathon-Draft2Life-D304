# Nhóm Draft2Life — D304 · Hướng C (Làn mở)

> **Lát cắt:** Sinh viên kiến trúc đang có mô hình 3D dựng từ mặt bằng 2D · gõ một câu tiếng Việt
> mô tả chi tiết muốn sửa · **AI quyết định câu đó đã đủ tham số để thực thi hay còn thiếu** ·
> trả về mô hình đã cập nhật kèm thông số, hoặc đúng một câu hỏi làm rõ.

## Thành viên & phân công

| Mã HV | Tên | Phụ trách |
|---|---|---|
| 2A202601945 | **Nguyễn Minh Công** *(lead)* | Lát cắt & automation · `spec.md` · prompt + lời gọi AI thật trong `codebase/` (CP3) |
| 01252 | **Nguyễn Văn Sáng** | Evidence Đường A (`scripts/analyze_survey.py`, `evidence/`) · bảng impact · log phỏng vấn |
| 01784 | **Diệp Đức Lai** | Flow UI `codebase/index.html` · golden set `eval/` · validation log `validation/` |

## Trạng thái theo rubric 75 điểm

> Bài nộp checkpoint đi qua link riêng của ban tổ chức, **không nằm trong repo**.
> Repo này chỉ chứa artifact của 75 điểm chấm bài.

| Khối rubric | Điểm | File trong repo | Xong? |
|---|---|---|---|
| R1 · Bằng chứng & impact | 15 | `spec.md` §1-§2 + `evidence/survey-log.md` (log nguyên văn 123 người) | ✅ |
| R2 · Lát cắt & thiết kế | 15 | `spec.md` §4 + §4b (6 nguyên tắc HAX/PAIR) | ✅ |
| R3 · Chỗ khó & kịch bản | 11 | `spec.md` §5 (10 kịch bản) + §6 (6 đường đi) | ✅ |
| R4 · Kiểm thử | 15 | `spec.md` §7 + `eval/` | ✅ 30 case, 4 lượt: 80,0% → **96,7%** vs bar 85% |
| R5 · Prototype chạy được | 8 | `codebase/` | ✅ Mock + **AI thật** ở quyết định trung tâm, trace trong repo |
| R6 · Validation với user | 8 | `validation/` | ⬜ **việc còn lại — khung sẵn, cần 5 người thật ngồi thử** |

**Ngoài rubric:** `demo-slides.pdf` (6 trang, nguồn `demo/slides.html`) · `reflection/` 3 file khung, mỗi người tự viết lại.
| R7 · Quy trình & repo | 3 | cấu trúc repo + README này | ✅ |

## Bằng chứng — Đường A (khảo sát), n = 123 người ngoài nhóm

| Chỉ số | Số | % |
|---|---|---|
| Phải chỉnh sửa chi tiết (cửa/tường/nội thất) **nhiều lần** khi dựng 3D | 98/123 | 79,7% |
| Sẵn sàng dùng công cụ AI cho việc này *(ngưỡng đề bài ≥50%)* | 94/123 | **76,4%** |
| Mất ≥3 ngày cho một mô hình 3D từ bản vẽ 2D | 78/123 | 63,4% |
| Muốn thử bản demo *(nguồn willing users)* | 109/123 | 88,6% |

Tái tạo: `python3 scripts/analyze_survey.py --input "<CSV khảo sát>"`.
**File khảo sát gốc chứa họ tên/email/SĐT nên không nằm trong repo**; script chỉ ghi ra số tổng hợp đã loại PII.

## Dữ liệu

- **CSV khảo sát gốc không nằm trong repo** — nó chứa họ tên/email/SĐT của 123 người. `.gitignore` chặn `*.csv`,
  và `scripts/analyze_survey.py` có `assert` chặn PII lọt vào output.
- `data/vlearn-pack/` (data pack khoá) đi kèm sẵn trong repo gốc ban tổ chức phát. Nhóm **không dùng** data pack này
  cho hướng C — bằng chứng của nhóm là khảo sát 123 người tự thu. Nếu repo nộp là **public**, cần gỡ `data/vlearn-pack/`
  khỏi cả lịch sử commit trước khi push (mục "Bảo mật dữ liệu" bên dưới, ý 2 và 3).

---

# Đề bài gốc — Mini Hackathon AI Batch 03

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

- Thời lượng: **1,5 ngày** (một ngày build + một buổi demo)
- Nhóm: **4-5 người** · zone tối đa 5 nhóm · thi theo lớp

## Bắt đầu từ đâu?

1. Đọc **`01-de-bai.md`** để chọn hướng và hiểu tiêu chí.
2. Mở **`02-guide.md`** — hướng dẫn từng giai đoạn, đứng ở đâu đọc mục đó.
3. Viết spec theo **`03-template-ai-spec.md`** — deliverable trung tâm của cả sự kiện.
4. Đọc **`04-rubric.md`** ngay từ đầu — biết trước bài được chấm theo tiêu chí nào.

| File / thư mục | Nội dung |
|---|---|
| `01-de-bai.md` | Đề bài 3 hướng · 5 tiêu chí nghiệm thu · ràng buộc chung |
| `02-guide.md` | Hướng dẫn 5 giai đoạn: khám phá → spec → build → đo & validate → demo |
| `03-template-ai-spec.md` | Template AI Spec (nộp 23:59 ngày 1) |
| `04-rubric.md` | Rubric 100 điểm (25 nộp checkpoint + 75 chấm bài) + checklist xác minh 6 mốc |
| `data/` | Dữ liệu thật đã ẩn danh: chatlog VLearn tutor + 6 transcript bài giảng + 2 bộ slide bản hackathon — dùng để tìm bằng chứng và xây golden set |
| `tham-khao/` | JTBD Playbook (PDF) + worksheet JTBD đầy đủ — đọc khi muốn đào sâu |

## Lịch — 6 mốc

| Mốc | Khoá 3 | Khoá 4 |
|---|---|---|
| Khai mạc + phát đề | 09:00 ngày 1 | 14:00 ngày 1 |
| CP1 · Chốt Canvas | 10:00 ngày 1 | 15:00 ngày 1 |
| CP2 · Show được thứ bấm được | 12:00 ngày 1 | 17:00 ngày 1 |
| CP3 · AI chạy thật + đo lượt đầu | 16:00 ngày 1 | 10:30 ngày 2 |
| CP4 · Chốt tiến độ — spec nộp hạn cứng **23:59 ngày 1** | 17:30 ngày 1 | 12:00 ngày 2 |
| CP5 · Xác minh + validation + dry run | 09:00 ngày 2 | 14:00 ngày 2 |
| CP6 · Demo | 10:00 ngày 2 | 15:00 ngày 2 |

Mỗi mốc cần show gì và được xác minh thế nào: xem bảng trong `04-rubric.md`.

## Nộp bài

Một repo nhóm, cấu trúc như sau. Spec chốt lúc 23:59 ngày 1; bản hoàn chỉnh trước CP6.

```
repo/
├── README.md          ← thành viên (mã HV + tên) + phân công có tên từng phần
├── spec.md            ← AI Spec theo 03-template-ai-spec.md
├── demo-slides.pdf    ← slide 6 trang theo 02-guide.md §5.1
├── codebase/          ← prototype (ghi rõ phần nào mock)
├── eval/              ← golden set + bảng kết quả các lượt chạy
├── validation/        ← feedback log từ vòng user test
└── reflection/        ← mỗi người 1 file
```

## Chấm điểm

Tổng **100 điểm = 25 điểm nộp checkpoint + 75 điểm chấm bài nộp**. Chi tiết từng ý điểm: `04-rubric.md`.

**25 điểm nộp — mỗi checkpoint 5 điểm (CP1-CP5):** nộp đúng hạn → 5 điểm · nộp muộn → 0 điểm cho mốc đó. Mỗi thành viên nộp riêng, cả nhóm dùng chung một link repo.

**75 điểm chấm — trên artifact trong repo, mỗi con điểm trỏ về một file:**

| Khối | Điểm | Chấm trên file nào |
|---|---|---|
| R1 · Bằng chứng & impact | 15 | `spec.md` §1-§2 + log khảo sát/mining |
| R2 · Lát cắt & thiết kế | 15 | `spec.md` §4 |
| R3 · Chỗ khó & kịch bản rủi ro | 11 | `spec.md` §5-§6 |
| R4 · Kiểm thử | 15 | `spec.md` §7 + `eval/` |
| R5 · Prototype chạy được | 8 | `codebase/` + demo |
| R6 · Validation với user | 8 | `validation/` |
| R7 · Quy trình & repo | 3 | cấu trúc repo |

Ba điều nên biết trước khi làm:

- Điểm dựa trên **chuỗi quyết định và bằng chứng**, không dựa trên mức độ hoành tráng của sản phẩm.
- Kết quả đo **ghi nhận trung thực** — kể cả khi không đạt mục tiêu nhóm tự đặt — vẫn được tính đủ điểm. Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính.
- Reflection cá nhân chấm riêng theo rubric của khoá. Điểm vòng demo, chấm chéo trong zone và thưởng thêm (nếu có) theo thể lệ công bố lúc khai mạc.

## Luật chung

1. Prototype có 3 mức **Sketch / Mock / Working** — mức nào cũng bắt buộc **≥1 lời gọi AI chạy thật**.
2. **Vibe-coding rule:** dùng AI để build thoải mái, nhưng không giải thích được phần có tên mình thì phần đó 0 điểm (kiểm tra tại CP5).
3. **Quality bar** chốt tại spec.md 23:59 ngày 1 và giữ nguyên sau đó.
4. Chỉ dùng dữ liệu trong `data/` hoặc dữ liệu giả tự sinh — không dùng dữ liệu thật của người thật. Không commit API key.
5. Tuân thủ **quy định bảo mật dữ liệu** bên dưới — đây là điều kiện để được cấp data.

## Bảo mật dữ liệu được cung cấp

Dữ liệu trong `data/` là dữ liệu thật của khoá học (đã ẩn danh), cấp riêng cho hackathon này. Khi nhận data, nhóm cam kết:

1. **Chỉ dùng trong phạm vi hackathon** — cho việc tìm bằng chứng, xây golden set và build prototype. Không dùng cho mục đích khác.
2. **Không chia sẻ ra ngoài khoá học** — không đăng lên mạng xã hội, không gửi cho người ngoài, không đưa vào bất kỳ dataset hay repo công khai nào.
3. **Không commit data pack vào repo nộp bài** — repo nhóm chỉ chứa trích dẫn ngắn để minh hoạ (vài dòng); golden set trích từ data ghi rõ mã đoạn/mã hội thoại thay vì dán nguyên văn dài.
4. **Cẩn trọng khi đưa data vào công cụ ngoài** — chỉ đưa phần tối thiểu cần cho việc đang làm; lưu ý API/công cụ free tier có thể dùng dữ liệu để huấn luyện (xem `02-guide.md` §3.4).
5. **Không cố suy ngược danh tính** từ dữ liệu đã ẩn danh ([học viên], mã U/C/T/M).
6. Sau sự kiện, **xoá các bản sao data pack** khỏi máy cá nhân và các công cụ đã upload nếu ban tổ chức yêu cầu.

Vi phạm được xử lý theo quy định của khoá và có thể ảnh hưởng trực tiếp đến điểm của nhóm.
