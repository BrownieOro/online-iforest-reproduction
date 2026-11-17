"""Upload completed local stationary runs to the configured W&B project."""
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from oif.tracking import log_run


ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = ROOT / "results" / "raw" / "stationary"


def main() -> None:
    """Log each local run and print its W&B URL without rerunning models."""
    load_dotenv(override=False)
    if os.getenv("WANDB_MODE", "disabled") != "online":
        raise SystemExit("Set WANDB_MODE=online and configure W&B credentials first.")
    for dataset in ("annthyroid", "mammography"):
        for run_dir in sorted((RUNS_DIR / dataset).glob("seed-*")):
            config_path, metrics_path = run_dir / "config.json", run_dir / "metrics.json"
            if not config_path.is_file() or not metrics_path.is_file():
                continue
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["tags"] = ["reproduction", "stationary"]
            config["experiment"] = "stationary_prequential"
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            url = log_run(config, metrics, run_dir)
            print(f"{dataset} seed={config['seed']} {url}", flush=True)


if __name__ == "__main__":
    main()
