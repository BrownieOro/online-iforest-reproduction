# INSECTS 10 đặc trưng — phân tích sơ bộ seed 0

OIF seed 0 đã chạy đủ 212.514 dòng; 100 dòng đầu khởi động, 212.414 dòng còn lại đánh giá theo lô, chấm trước học. ROC-AUC = 0,735126; AP = 0,122566. [Run W&B và artifact](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/dqkrvfhm). Cấu hình: 32 cây, cửa sổ học 2.048, η = 32, 10 cột đầu. Các seed khác đang chạy; chưa suy rộng từ một seed.

So sánh định tính với Hình 7 của [paper](https://proceedings.mlr.press/v235/leveni24a.html): đường chất lượng thay đổi theo thời gian và có sụt giảm sau một số mốc, nhưng không đối chiếu trực tiếp giá trị số vì nhóm chấm trước học, tác giả học trước chấm; script tác giả còn dùng 30 lần, các cách lấy cửa sổ đánh giá và baseline khác. Không khẳng định tái lập chính xác.

## Quy ước phục hồi

Với mỗi mốc, lấy ROC-AUC của cửa sổ 5.000 mẫu hoàn chỉnh cuối cùng kết thúc trước hoặc tại mốc làm ngưỡng. Cửa sổ hoàn chỉnh sau mốc đầu tiên đạt lại ngưỡng là cửa sổ phục hồi; độ trễ tính từ mốc tới cuối cửa sổ đó. Không vượt qua mốc kế tiếp; bước di chuyển 1.000 mẫu. Vì cửa sổ có độ dài 5.000, độ trễ bao gồm thời gian tích lũy để đánh giá, không phải độ trễ thích nghi tức thời của mô hình. Các cửa sổ lân cận chồng lấn; sự dao động của nhãn và phân phối có thể ảnh hưởng AUC. Bảng theo từng run được tạo bởi `recovery_analysis.py`.

| Mốc | AUC trước | AUC cửa sổ đầu sau | Phục hồi theo quy ước |
|---:|---:|---:|---|
| 51.255 | 0,870 | 0,722 | Chưa quan sát trước mốc kế tiếp |
| 74.381 | 0,763 | 0,617 | 9.719 mẫu |
| 100.944 | 0,886 | 0,595 | Chưa quan sát trước mốc kế tiếp |
| 142.291 | 0,676 | 0,571 | 8.809 mẫu |
| 152.207 | 0,731 | 0,801 | 5.893 mẫu |

[Phân bố điểm trước và sau mốc đầu](../figures/drift-score-distribution-10.png) hiển thị riêng theo nhãn, mỗi đường chuẩn hóa thành mật độ; không phản ánh tỷ lệ lớp. Dữ liệu từ đúng run seed 0; không kết luận nguyên nhân chỉ từ biểu đồ. Số liệu, recovery và hình sẽ cập nhật khi các seed khác hoàn thành.
