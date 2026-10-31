# Online Isolation Forest

Repo đồ án Nhập môn Học máy, nghiên cứu bài **Online Isolation Forest (ICML 2024)**.

## Cấu trúc repo

```text
online-iforest-reproduction/
├── README.md                         Sơ đồ và hướng dẫn tìm file
├── .gitignore                        Bỏ qua môi trường, khóa và dữ liệu lớn
├── .gitattributes                    Quy định định dạng file trong Git
│
├── papers/                           Tài liệu bài báo
│   ├── leveni24a-original.pdf         Paper gốc tiếng Anh
│   ├── online-isolation-forest-vi.md  Bản dịch tiếng Việt
│   ├── CITATION.bib                   Thông tin trích dẫn
│   ├── NOTICE.md                      Nguồn và ghi công tài liệu
│   └── figures/                      Hình gốc để đọc đối chiếu
│
├── docs/                             Tài liệu học và yêu cầu môn
│   ├── bat-dau-o-day.md               Giải thích pipeline bằng tiếng Việt
│   ├── ghi-chu-doi-chieu.md           Chi tiết cần kiểm tra khi triển khai
│   ├── yeu-cau-do-an.md               Yêu cầu đồ án
│   ├── checklist-nop-bai.md           Danh sách kiểm tra trước khi nộp
│   ├── tai-nguyen.md                  Link tài liệu, code và dữ liệu tham khảo
│   └── requirements/                 Bản lưu các nguồn yêu cầu
│
├── model/                            Thuật toán chung do nhóm tự viết
├── data/                             Code và hướng dẫn chuẩn bị dữ liệu
├── experiments/                      Code chạy từng thí nghiệm
│   ├── exp1_stationary/              Thí nghiệm dữ liệu ổn định
│   ├── exp2_drift/                   Thí nghiệm dữ liệu thay đổi theo thời gian
│   └── exp3_window/                  Phân tích kích thước cửa sổ
├── results/                          Bảng kết quả nhóm tự chạy
├── figures/                          Biểu đồ và hình nhóm tự tạo
└── slides/                           Nội dung trình bày
    └── README.md                     Link outline trên Google Docs; nơi đặt PPTX cuối
```

Các thư mục code hiện mới có README mô tả; chưa triển khai thuật toán hoặc chạy thí nghiệm. `papers/figures/` chứa hình của tác giả; `figures/` dành cho hình nhóm tự tạo.

## Mở nhanh

- [Paper gốc](papers/leveni24a-original.pdf) · [Bản dịch tiếng Việt](papers/online-isolation-forest-vi.md)
- [Giải thích pipeline](docs/bat-dau-o-day.md) · [Yêu cầu đồ án](docs/yeu-cau-do-an.md)
- [Outline slide và deadline trên Google Docs](https://docs.google.com/document/d/1BXscOQX-TQZYzKy0HOXoMgYcpc5V_lgIFqZvYFJ9c1g/edit?tab=t.pdo9d2xfspft)
- [Kế hoạch và phân việc trên Google Docs](https://docs.google.com/document/d/1BXscOQX-TQZYzKy0HOXoMgYcpc5V_lgIFqZvYFJ9c1g/edit?tab=t.eimsvhhx7ipi)

Nguồn bài: [PMLR](https://proceedings.mlr.press/v235/leveni24a.html) · [Repo tác giả](https://github.com/ineveLoppiliF/Online-Isolation-Forest). Xem [ghi công tài liệu](papers/NOTICE.md).
