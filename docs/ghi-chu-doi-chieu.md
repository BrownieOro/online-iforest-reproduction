# Ghi chú đối chiếu khi đọc và triển khai

Đây là ghi chú của người biên soạn, **không phải nội dung tác giả bổ sung** và không phải kết luận nhóm đã kiểm chứng.

## 1. “Chiều cao ô” và “độ sâu cây” là hai thứ khác nhau

`h` là số điểm/khối lượng thống kê ở ô; `k` là độ sâu node trong cây. Không dịch hoặc dùng hai đại lượng này thay cho nhau. Ngưỡng tách là `η·2^k`, không phải chỉ `η` ở mọi độ sâu.

## 2. Tập điểm khi tách là tập được lấy mẫu

Mục 4.1 nói lấy các điểm từ phân phối đều trên miền bao R để khởi tạo hai ô con. Không được tự đổi thành giữ mọi điểm thật ở từng lá rồi chia lại mà vẫn coi đó là triển khai nguyên phương pháp.

## 3. Thứ tự cập nhật và tính điểm

Thuật toán 1 trong PDF: học điểm mới → quên điểm cũ nếu quá cửa sổ → tính điểm. Phần thực nghiệm nói xử lý theo lô 100 điểm. Khi triển khai và đối chiếu repo tác giả, ghi rõ thứ tự thực tế theo lô; không mặc định đánh giá trước cập nhật là cùng protocol.

## 4. Ký hiệu cửa sổ trong bài

Bài viết W = [x_(t-ω), ..., x_t] và gọi kích thước là ω; nếu đếm cả hai đầu chỉ số thì biểu thức này có thể gây nhầm một điểm. Thuật toán 1 mô tả thêm mới rồi bỏ điểm cũ khi độ dài vượt ω. Dùng mô tả thao tác để làm rõ, ghi quyết định và kiểm tra với code tác giả.

## 5. Hệ số hiệu chỉnh độ sâu

Trang 3 viết c(ω,η) = log₂(ω/η), còn phương trình (4) ở trang 6 suy ra độ sâu trung bình dưới giả thiết cây cân bằng là floor(0.5·log₂(ω/η)+1). Bản dịch giữ cả hai biểu thức đúng như PDF, không tự đồng nhất hoặc sửa bài. Cần đối chiếu code tác giả trước khi chọn cách tính trong code nhóm.

Thuật toán 4 có hiệu chỉnh k + c(h,η). Các trường hợp h nhỏ, h = 0, miền bao suy biến và phép tách ra ô rỗng cần được kiểm tra trong code đối chiếu; không thể suy ra toàn bộ xử lý biên chỉ từ giả mã.

## 6. Độ phức tạp là phân tích của tác giả

Bảng 1 giữ đúng kết quả đã nêu trong bài. Khi phê bình, cần xét giả thiết cây cân bằng, chi phí theo số chiều d, chi phí lấy mẫu khi tách và cách lưu miền bao. Bản dịch không xác nhận độc lập tính đầy đủ của phân tích.

## 7. Cửa sổ học khác cửa sổ đánh giá

ω = 2048 là cửa sổ học mặc định của oIFOR trong thí nghiệm. Cửa sổ 5000 điểm có tâm trong Hình 7 dùng để tổng hợp AUC khi đánh giá, không phải cửa sổ học. Không dùng nhãn hoặc dữ liệu tương lai của cửa sổ đánh giá để huấn luyện.

## 8. Giả định i.i.d. và dữ liệu thay đổi

Mục 2 nêu i.i.d., trong khi động lực và INSECTS xét phân phối thay đổi. Đây là chỗ cần hiểu phạm vi giả định, không tự viết lại phát biểu của tác giả trong bản dịch cho có vẻ nhất quán.

## 9. Trung vị tổng hợp không phải trung vị của 11 con số in trong bảng

Phần 5.2-5.3 mô tả 30 lần chạy và tổng hợp trên 330 lần thực thi. Bản dịch giữ nguyên dòng Median/Mean Rank, không tính lại chúng chỉ từ các trung vị theo dataset đã làm tròn trong Bảng 4.

## 10. Kết luận cần đúng mức

oIFOR nhanh nhất trong thí nghiệm được báo cáo, không có nghĩa AUC luôn cao nhất hoặc chắc chắn thắng trên máy và dữ liệu của nhóm. Hình 7 cũng không chứng minh nó luôn thích nghi tốt nhất sau drift. Mọi tuyên bố của nhóm phải dựa trên lần chạy thực tế của nhóm.

## Bản đồ trang để đối chiếu

| Trang PDF gốc | Nội dung |
|---|---|
| 1 | Tóm tắt và mở đầu |
| 2 | Hình 1, phát biểu bài toán, related work |
| 3 | Related work, phương pháp, Thuật toán 1, công thức (1) |
| 4 | Hình 2, Online-iTree, Thuật toán 2 |
| 5 | Hình 3, Thuật toán 3-4, học và quên |
| 6 | Bảng 1, công thức (2)-(7), đánh đổi cửa sổ |
| 7 | Bảng 2-3, dữ liệu và protocol thực nghiệm |
| 8 | Bảng 4, Hình 4, phân tích kết quả |
| 9 | Hình 5-7, drift, kết luận và hướng tương lai |
| 10-11 | Lời cảm ơn, tác động và tài liệu tham khảo |
