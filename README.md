# Online Isolation Forest - Đồ án Nhập môn Học máy

Kho chung để nhóm đọc hiểu bài **Online Isolation Forest (ICML 2024)**, tự triển khai, tái tạo thực nghiệm và làm slide/poster theo yêu cầu môn học.

## Bắt đầu từ đâu?

1. Đọc [Giải thích luồng hoạt động bằng tiếng Việt](docs/bat-dau-o-day.md).
2. Đọc [bản dịch tiếng Việt](papers/online-isolation-forest-vi.md), mở cạnh [PDF gốc](papers/leveni24a-original.pdf) để đối chiếu.
3. Xem [yêu cầu đồ án](docs/yeu-cau-do-an.md) và [danh sách kiểm tra trước khi nộp](docs/checklist-nop-bai.md).
4. Xem [tài nguyên](docs/tai-nguyen.md), rồi thống nhất [cách chia việc và bố trí file](docs/cach-lam-viec.md).

## Trong repo có gì?

| Đường dẫn | Nội dung |
|---|---|
| `papers/leveni24a-original.pdf` | PDF gốc, sao chép nguyên vẹn từ file người dùng cung cấp |
| `papers/online-isolation-forest-vi.md` | Bản dịch nội dung bài: tóm tắt, mục 1-6, thuật toán, công thức, bảng, chú thích hình, lời cảm ơn và tác động; giữ thông tin thư mục tham khảo gốc |
| `papers/figures/` | 7 hình trích từ PDF để đọc đối chiếu, thuộc tác giả bài báo |
| `papers/CITATION.bib` | Thông tin trích dẫn bài |
| `docs/yeu-cau-do-an.md` | Yêu cầu môn học lấy từ tài liệu nhóm |
| `docs/requirements/` | Bản chụp nguồn yêu cầu và nội dung bổ sung về slide |
| `docs/ghi-chu-doi-chieu.md` | Những chỗ cần kiểm tra kỹ khi đọc và triển khai; tách khỏi bản dịch |
| `model/` | Nơi sẽ đặt thuật toán chung do nhóm tự viết |
| `data/` | Nơi sẽ đặt hướng dẫn và code chuẩn bị dữ liệu |
| `experiments/` | Ba phần: thí nghiệm 1, thí nghiệm 2 và phân tích bổ sung |
| `results/` | Nơi lưu bảng kết quả nhóm đã chạy |
| `figures/` | Nơi lưu hình do nhóm tự tạo để đưa lên slide |
| `slides/` | Nơi lưu dàn ý, speaker notes và file nộp cuối |

## Trạng thái hiện tại

- Đã có PDF gốc, bản dịch, yêu cầu đồ án và hướng dẫn bắt đầu.
- Chưa triển khai thuật toán, chưa cài môi trường thực nghiệm và chưa chạy thí nghiệm.
- Các con số trong bản dịch đều là số liệu của tác giả, không phải kết quả nhóm.
- Các phạm vi và phân công trong `docs/cach-lam-viec.md` là đề xuất để nhóm chốt, không phải yêu cầu bổ sung của giảng viên.

## Chạy ở đâu?

Viết và chạy Python trên máy cá nhân bằng VS Code. Chạy thử nhỏ trước; nếu tài nguyên không đủ thì cân nhắc nền tảng khác. GitHub lưu code chung. W&B lưu cấu hình và bằng chứng từng lần chạy. Hiện repo mới có tài liệu, nên chưa có lệnh chạy mô hình.

Khi bổ sung code, README cần có: phiên bản Python và thư viện, cách cài, cách chuẩn bị dữ liệu, lệnh chạy từng thí nghiệm, cách chọn seed và cách tạo lại bảng/hình.

## Bảng theo dõi thí nghiệm

| Thí nghiệm | Script/config | W&B run | Kết quả tóm tắt |
|---|---|---|---|
| 1. Dữ liệu ổn định | Chưa triển khai | Chưa chạy | Chưa có kết quả |
| 2. Dữ liệu thay đổi theo thời gian | Chưa triển khai | Chưa chạy | Chưa có kết quả |
| 3. Phân tích kích thước cửa sổ | Chưa triển khai | Chưa chạy | Chưa có kết quả |

## Nộp bài

Slide chiếm **45%**, hạn nộp theo thông tin được cung cấp: **23:59 ngày 21/11/2026**. Nộp `ID.pptx` gồm **20-40 slide**, dưới **20 MB**, mọi slide có speaker notes tối đa **500 từ**. Nộp link repo công khai riêng trên Moodle. Xem chi tiết tại [yêu cầu đồ án](docs/yeu-cau-do-an.md); kiểm tra Moodle nếu giảng viên cập nhật.

## Nguồn và ghi công

Leveni, F., Weigert Cassales, G., Pfahringer, B., Bifet, A., và Boracchi, G. *Online Isolation Forest*. ICML, PMLR 235:27288-27298, 2024. [Trang xuất bản](https://proceedings.mlr.press/v235/leveni24a.html) · [Repo tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest).

Bản dịch có AI hỗ trợ, phục vụ học tập và chưa được tác giả thẩm định. PDF và hình gốc thuộc các tác giả; xem [ghi công tài liệu](papers/NOTICE.md). Khi làm slide, nhóm phải tự diễn đạt và tự tạo hình theo yêu cầu môn học.
