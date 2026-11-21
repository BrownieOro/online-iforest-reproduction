# W&B — danh mục run đã xác minh

Project: https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif

| Run | Dữ liệu và protocol | ROC-AUC | Ghi chú |
|---|---|---:|---|
| [z86dyqji](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/z86dyqji) | Annthyroid, sklearn IsolationForest, holdout ngẫu nhiên, seed 42 | 0,821244 | Baseline offline, không phải thí nghiệm stationary trực tuyến của Phúc |
| [o0jdbf4s](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/o0jdbf4s) | Annthyroid, sklearn IsolationForest, holdout ngẫu nhiên, seed 42 | 0,821244 | Chạy lặp của cùng cấu hình, thời gian khác |
| [judihdbh](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/judihdbh) | Mammography, sklearn IsolationForest, holdout ngẫu nhiên, seed 42 | 0,862427 | Baseline offline |

Các run trên là những run đã hoàn tất có trong project khi rà soát ngày 19/11. Không dùng chúng làm link cho các kết quả được tạo bởi protocol hoặc code khác. INSECTS d = 10 có 10 link cuối ở mục bên dưới.

## Run lịch sử — không dùng cho số cuối

| Run | Dữ liệu và protocol | ROC-AUC | Ghi chú |
|---|---|---:|---|
| [dqkrvfhm](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/dqkrvfhm) | INSECTS, OIF, 10 features, prequential, seed 0 | 0,735126 | Sơ bộ trước sửa warm-up; không dùng làm kết quả cuối |

## INSECTS — kết quả chính sau sửa warm-up

Các run dùng 10 đặc trưng, 5 seed, 32 cây, cửa sổ 2048; từng run có dự đoán và biểu đồ AUC. Xem bảng số liệu tại [drift-fixed-10.md](../results/drift-fixed-10.md).

- [asdifor_seed0](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/pqz5mwjq)
- [asdifor_seed1](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/8w9ds7kg)
- [asdifor_seed2](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/nijtz9s7)
- [asdifor_seed3](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5b66rbfq)
- [asdifor_seed4](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zkiiyp3g)
- [oif_seed0](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/lpprt64h)
- [oif_seed1](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/5nsp99kc)
- [oif_seed2](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/bkkazl0o)
- [oif_seed3](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/zrvo8y72)
- [oif_seed4](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/gq0qkj76)

## Chờ bàn giao và upload — mốc 21/11

| Bộ kết quả | Trạng thái ghi trong repo | Cần bổ sung |
|---|---|---|
| Stationary-f4, 120 run | Báo cáo có số liệu sau sửa node con/F4; W&B 0/120 | ZIP từ Phúc, kiểm raw, manifest URL từng run |
| Drift33, 10 run | Có bảng sau sửa node con; chưa có URL W&B | ZIP bản cuối từ Thi, xác minh nguồn thời gian, manifest riêng |
| Sweep10, 4 window, seed0 | Có bảng/biểu đồ; W&B tắt | ZIP từ Thi, manifest riêng cho từng window |

Xem [cách upload không chạy lại](wandb.md) và [bàn giao Trân](ban-giao-tran.md).
Các đường dẫn raw trong báo cáo không phải URL download vì Git bỏ qua raw.
Không lấy các link d = 10 hoặc holdout offline ở trên thay cho các bộ đang chờ.
