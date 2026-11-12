# W&B — cách chạy và truy vết kết quả

Project dùng chung: `intro-ml-oif`.

```powershell
$env:WANDB_MODE="online"
$env:WANDB_PROJECT="intro-ml-oif"
python scripts/run_baseline.py --data data/processed/annthyroid.csv --label-column label --output results/raw/baseline/annthyroid-42-online
```

Mỗi run ghi cấu hình, metrics và artifact gồm `config.json`, `metrics.json`, `predictions.csv`. CSV nguồn không upload. Nếu chưa đăng nhập, dùng `WANDB_MODE=offline`; không dùng link offline trên slide.

Run online đã kiểm tra: project `intro-ml-oif`, run `z86dyqji` (`stellar-oath-2`). Mọi số liệu trên slide phải trỏ tới run tương ứng.
