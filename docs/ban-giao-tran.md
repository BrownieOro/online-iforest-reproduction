# Bàn giao phần Trân — mốc 21/11/2026

Chốt dùng số liệu nhóm sau sửa khởi tạo node con, stationary lấy bản F4 mới
nhất. Các lượt thử nghiệm riêng ngoài bộ số liệu này không đưa vào slide chính.
Tài liệu này là trạng thái bàn giao; không xác nhận raw chưa nhận hoặc W&B chưa tải.

## Đã chuẩn bị để ghép deck

- Phần lý thuyết 3.1, 3.6–3.8, 4.1 đã có trên Docs của nhóm.
- [Nháp Trân](../slides/phase2-tran.md) có nội dung/notes/nguồn cho 6.3, 8.1, 8.2.
  Tổng kết đã đổi sang stationary-f4, bỏ cảnh báo dải seed chồng lấn của lượt cũ.
- [Công thức triển khai](cong-thuc-oif.md) gom công thức, ví dụ, xử lý biên,
  lựa chọn khác paper và cách cấp seed sau F4.
- [Hướng dẫn W&B](wandb.md) chỉ cách nhận, kiểm tra và upload kết quả đã chạy.
  [Danh mục link hiện có](wandb-runs.md) giữ link đúng protocol/dataset.

## Việc đang chờ

| Đầu vào | Người bàn giao | Khi nhận thì làm |
|---|---|---|
| ZIP stationary-f4, kèm runs.csv | Phúc | Kiểm 120 bộ config/metrics/predictions; đối chiếu bảng; upload W&B |
| ZIP drift d=33 bản cuối, xác nhận tên thư mục | Thi | Kiểm 10 run và đối chiếu AUC/AP; xác nhận nguồn thời gian trước khi dùng |
| ZIP window-sweep-10 | Thi | Kiểm 4 cấu hình window_size và seed0; upload từng cấu hình bằng manifest riêng |
| Link deck/file slide hiện tại | Người ghép slide | Rà đủ20–40slide, notes, hình/nguồn, số liệu/link; kiểm bản xuất |

## Những điểm cần chốt từ ZIP

1. Stationary: nhận đúng `stationary-f4`, không phải `stationary`,
   `stationary-after-bootstrap` hoặc `stationary-seedblock` lịch sử.
   Báo cáo hiện ghi commit54f1c48, worktree sạch, seed cây32×s+i.
2. Drift d=33: `results/drift.md` ghi raw `drift-v2` tại commitfb35956;
   `drift-after-bootstrap.md` ghi thư mục `drift-after-bootstrap`.
   Hai báo cáo khớp AUC nhưng thời gian khác: 182,9/10,2 giây so với
   1049,8/61,2 giây. Không tự chọn một cặp để báo cáo khi chưa kiểm config/raw.
   Nháp tổng kết Trân không đưa cặp thời gian này vào bảng trong lúc chờ xác minh.
3. Sweep: bốn cửa sổ256/512/2048/8192, d=10, seed0, chấm-trước-học.
   Một seed chưa xác định được cấu hình tối ưu. Không thay link run d=10,
   window2048 cho cả bốn cấu hình.
4. Thư mục raw bị Git bỏ qua không phải một đường dẫn download. Phải có ZIP,
   nơi lưu chung hoặc artifact thật trước khi coi là đã bàn giao.

## Sau upload

- Giữ URL từng run trong manifest, chia riêng stationary/drift33/sweep.
- Thêm link vào docs/wandb-runs.md, báo cáo tương ứng và chân slide/notes.
- Không sửa trạng thái “chưa upload” thành “đã có W&B” trước khi có URL thật.
- Rà các số tổng hợp và notes theo cùng một bảng nguồn; không trộn holdout
  offline, stationary streaming, drift10 và drift33.
- Cập nhật trạng thái cũ trên Google Docs sau khi đã kiểm; không xóa lịch sử
  hoặc viết đè tab của thành viên khác khi chưa xác định bản dùng để ghép.
- Hợp nhất nhánh tích hợp vào main là việc chung của nhóm sau khi review;
  không lấy main cũ làm nguồn số liệu.

## Câu trả lời ngắn cho các câu hỏi dễ gặp

**Điểm OIF có phải xác suất không?** Không. Điểm là biến đổi từ độ sâu hiệu
chỉnh trung bình; lớn hơn thể hiện mức bất thường cao hơn theo mô hình.

**Vì sao log₄ trong code mà paper ghi log₂?** Nhóm theo hàm của code tác giả
cho cây nhị phân; tài liệu trình bày riêng công thức paper và lựa chọn triển khai.
Không khẳng định chúng là cùng biểu thức.

**Warm-up stationary và drift khác gì?** Stationary học30% đầu rồi đánh giá70%
còn lại; drift chỉ bỏ lô100đầu, giữ thứ tự thời gian. Không so số giữa hai protocol
như cùng điều kiện.

**Baseline có đúng PySAD không?** Các số đang chốt dùng baseline sklearn của nhóm;
stationary fit cố định, drift huấn luyện lại theo cửa sổ. Không gọi là tái tạo nguyên
implementation PySAD của tác giả.

**Không phục hồi ở một mốc có nghĩa thất bại vĩnh viễn không?** Không. Chỉ là
chưa quan sát đạt lại ngưỡng trước mốc tiếp theo theo quy tắc cửa sổ đánh giá.

**Độ trễ có phải thời gian thích nghi thuần túy không?** Không. Nó còn chứa thời
gian tích lũy cửa sổ đánh giá5.000 và ảnh hưởng độ khó/phân bố của đoạn mới.
