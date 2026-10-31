# Cách chia việc và bố trí file

Đây là đề xuất, nhóm chưa chốt tên thành viên hoặc phạm vi thực nghiệm cuối cùng.

## Làm ở đâu?

- Máy cá nhân + VS Code + Python: viết và chạy code.
- GitHub: lưu và gộp công việc.
- W&B: hồ sơ mỗi lần chạy.
- Chạy nhỏ trước; chỉ chuyển nền tảng nếu thực tế cần thêm tài nguyên.

## Giai đoạn đầu: cả nhóm cùng hiểu, chưa chia chạy lớn

1. Cả ba đọc `bat-dau-o-day.md`, tóm tắt, mở đầu và kết luận bài.
2. Một người giải thích thuật toán bằng hình; một người chạy ví dụ tác giả; một người tổng hợp cách đánh giá và quy định môn.
3. Chỉ lại cho nhau. Thống nhất một ví dụ mà mọi người đều giải thích được.
4. Chốt giao diện thuật toán chung, cách lưu cấu hình, cách xử lý dữ liệu và metric.

## Sau đó: mỗi người ôm một gói thí nghiệm

| Gói | Câu hỏi | Thư mục chính |
|---|---|---|
| Người 1: thí nghiệm chính 1 | Dữ liệu ổn định: phát hiện tốt và chạy nhanh đến đâu? | `experiments/exp1_stationary/` |
| Người 2: thí nghiệm chính 2 | Khi dữ liệu thay đổi theo thời gian, chất lượng biến đổi ra sao? | `experiments/exp2_drift/` |
| Người 3: phân tích bổ sung | Cửa sổ nhỏ/lớn ảnh hưởng thế nào? | `experiments/exp3_window/` |

Mỗi người giao đủ: code chạy, cấu hình, W&B run, bảng/hình, phân tích và slide kèm notes. Không giao toàn bộ slide cho một người.

## Nút thắt: thuật toán chung

`model/` chỉ có một bản thuật toán dùng chung. Chọn một người viết chính và một người review; luân phiên chia nhỏ phần cây, rừng và đánh giá. Nếu người 3 viết chính thì giảm phạm vi phân tích bổ sung, không giao thêm toàn bộ việc ghép slide cho người đó.

Trong lúc thuật toán chung chưa xong, hai người còn lại có thể chuẩn bị dữ liệu, chạy bản tác giả, tích hợp phương pháp so sánh và kiểm tra metric.

## Quy tắc file

- `model/`: thuật toán do nhóm tự viết; thay đổi phải được ít nhất một người khác kiểm tra.
- `data/`: hướng dẫn nguồn và code chuẩn bị; dữ liệu lớn để ở `data/raw/` và `data/processed/`, đã được bỏ qua bởi Git.
- `experiments/exp*/`: script, cấu hình và hướng dẫn riêng từng thí nghiệm.
- `results/`: bảng kết quả nhóm; ghi dataset, model, seed, tham số, metric, thời gian và W&B URL.
- `figures/`: hình tự tạo từ kết quả nhóm.
- `papers/figures/`: hình của tác giả, chỉ đọc đối chiếu.
- `slides/`: dàn ý và notes; chỉ gộp một bản PPTX cuối, không để ba người sửa ba bản cùng tên rồi ghi đè.

## Làm chung qua GitHub

1. Mỗi người tải repo về máy bằng Clone Repository trong VS Code.
2. Tạo nhánh riêng, ví dụ `person1-exp1`, `person2-exp2`, `person3-window`.
3. Cập nhật từ nhánh `main` trước khi làm việc tiếp.
4. Ghi lại thay đổi thành commit nhỏ, đẩy lên nhánh của mình.
5. Mở Pull Request để một người khác kiểm tra rồi gộp vào `main`.

Không commit mật khẩu, API key, `.env`, toàn bộ môi trường Python hoặc thư mục log W&B. Không xóa lịch sử để làm lại repo sát hạn nộp.
