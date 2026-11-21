# Drift33 sau F4 — ZIP Thi bàn giao và W&B

Nguồn: results/drift33-f4-0ea3214.zip, ThiQuang push lúc18:40ngày21/11. ZIP có10run, mỗi run đủ ba file; đã tính lại ROC-AUC/AP từ predictions.csv và khớp metrics.json tới1e-12. Commit chạy0ea32145,worktree sạch,33đặc trưng,5seed0–4,chấm-trước-học,bỏ100dòng đầu.

| Run | ROC-AUC | AP | Thời gian trong ZIP (s) | W&B |
|---|---:|---:|---:|---|
| asdifor_seed0 | 0.710995 | 0.096051 | 12.068 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/ba3651aea64fb983) |
| asdifor_seed1 | 0.717698 | 0.097667 | 12.624 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/9d198f0722e04b0c) |
| asdifor_seed2 | 0.706458 | 0.094688 | 11.799 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/de93871423a827bf) |
| asdifor_seed3 | 0.717819 | 0.096742 | 10.971 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/d64517fc26a3d85b) |
| asdifor_seed4 | 0.718282 | 0.099961 | 11.364 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/f1b99640335ccd91) |
| oif_seed0 | 0.744140 | 0.107635 | 190.337 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/6b842d2492f2d875) |
| oif_seed1 | 0.696248 | 0.092857 | 190.188 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/decedf711c97d05c) |
| oif_seed2 | 0.645107 | 0.075007 | 189.263 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/a7eb5fc679012c45) |
| oif_seed3 | 0.705821 | 0.104001 | 180.569 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/b471705a259ba912) |
| oif_seed4 | 0.747694 | 0.117608 | 187.563 | [run](https://forge.coreweave.com/wandb/24122055-university-of-science-viet-nam-national-univer/intro-ml-oif/runs/d6f8d14a12828e5a) |

## Tổng hợp đúng ZIP mới

- asdifor: AUC median0.717698;AP median0.096742;thời gian median11.799giây.
- oif: AUC median0.705821;AP median0.104001;thời gian median189.263giây.

AUC/AP khớp các bảng drift33 lịch sử; thời gian mới thuộc lượt chạy lại trong ZIP này, không thay nhầm thời gian cũ của máy/lượt khác. Các thời gian phản ánh implementation trên máy người chạy, không chứng minh tốc độ thuật toán so với paper. Baseline asdifor là sklearn cửa sổ do nhóm dựng, không phải PySAD.

Biểu đồ/notes về các đoạn lấy từ báo cáo drift.md nếu dùng đúng dữ liệu và protocol; nguồn run mới là manifest drift33-wandb-links.json. Không dùng số d10thay d33.
