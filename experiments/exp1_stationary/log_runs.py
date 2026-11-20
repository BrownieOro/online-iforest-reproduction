"""Upload completed local stationary runs to the configured W&B project."""
import argparse
import csv
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from dotenv import load_dotenv

from oif.tracking import log_run


ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = ROOT / "results" / "raw" / "stationary-seedblock"
LINKS_OUTPUT = ROOT / "results" / "stationary-wandb-links.csv"
REPORT_OUTPUT = ROOT / "results" / "stationary.md"
SLIDE_OUTPUT = ROOT / "slides" / "phase2-phuc.md"
MODEL_NAMES = {
    "isolation_forest": "sklearn.ensemble.IsolationForest",
    "online_isolation_forest": "OnlineIsolationForest",
}
LINK_FIELDS = ("dataset", "model", "seed", "url")


def read_links(path: Path) -> dict[tuple[str, str, int], dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open("r", newline="", encoding="utf-8") as stream:
        rows = csv.DictReader(stream)
        if rows.fieldnames != list(LINK_FIELDS):
            raise ValueError(f"Unexpected W&B link manifest columns in {path}")
        linked = {}
        for row in rows:
            key = (row["dataset"], row["model"], int(row["seed"]))
            if key in linked:
                raise ValueError(f"Duplicate entry in W&B link manifest: {key}")
            linked[key] = row
    return linked


def write_links(path: Path, links: dict[tuple[str, str, int], dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=LINK_FIELDS)
        writer.writeheader()
        for key in sorted(links):
            writer.writerow(links[key])
    os.replace(temporary, path)


def get_project_url(run_url: str) -> str:
    parsed = urlsplit(run_url)
    parts = [part for part in parsed.path.split("/") if part]
    if "runs" in parts:
        parts = parts[:parts.index("runs")]
    elif len(parts) >= 2:
        parts = parts[:2]
    else:
        raise ValueError(f"Cannot determine W&B project URL from {run_url}")
    return urlunsplit((parsed.scheme, parsed.netloc, "/" + "/".join(parts), "", ""))


def update_status(output_path: Path, links_path: Path,
                  links: dict[tuple[str, str, int], dict[str, str]],
                  total_runs: int) -> None:
    if not output_path.is_file() or not links:
        return
    project_url = get_project_url(next(iter(links.values()))["url"])
    relative_links_path = Path(os.path.relpath(
        links_path.resolve(), output_path.resolve().parent)).as_posix()
    begin = "<!-- W&B status begin -->"
    end = "<!-- W&B status end -->"
    block = (
        f"{begin}\n"
        f"**W&B:** {len(links)}/{max(total_runs, len(links))} run đã tải lên. "
        f"[Project]({project_url}) · [danh sách run]({relative_links_path})\n"
        f"{end}"
    )
    content = output_path.read_text(encoding="utf-8")
    marker = re.compile(re.escape(begin) + r".*?" + re.escape(end), flags=re.DOTALL)
    if marker.search(content):
        content = marker.sub(lambda _: block, content, count=1)
    else:
        heading = re.search(r"^# .+$", content, flags=re.MULTILINE)
        if heading:
            content = content[:heading.end()] + "\n\n" + block + content[heading.end():]
        else:
            content = block + "\n\n" + content
    output_path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_local_runs(runs_dir: Path) -> list[tuple[tuple[str, str, int], dict, dict, Path]]:
    if not runs_dir.is_dir():
        raise SystemExit(f"No local stationary runs found at {runs_dir}")
    runs = []
    for dataset_dir in sorted(path for path in runs_dir.iterdir() if path.is_dir()):
        for model_dir in sorted(path for path in dataset_dir.iterdir() if path.is_dir()):
            expected_model = MODEL_NAMES.get(model_dir.name)
            if expected_model is None:
                raise ValueError(f"Unknown model directory: {model_dir}")
            for run_dir in sorted(model_dir.glob("seed-*")):
                paths = [run_dir / name for name in
                         ("config.json", "metrics.json", "predictions.csv")]
                if not all(path.is_file() for path in paths):
                    raise ValueError(f"Run is missing a required artifact: {run_dir}")
                config = json.loads(paths[0].read_text(encoding="utf-8"))
                if config.get("dataset") != dataset_dir.name:
                    raise ValueError(f"Dataset path does not match config: {run_dir}")
                try:
                    seed = int(run_dir.name.removeprefix("seed-"))
                except ValueError as exc:
                    raise ValueError(f"Invalid seed directory: {run_dir}") from exc
                if config.get("model") != expected_model or config.get("seed") != seed:
                    raise ValueError(f"Run path does not match config: {run_dir}")
                metrics = json.loads(paths[1].read_text(encoding="utf-8"))
                key = (dataset_dir.name, expected_model, seed)
                runs.append((key, config, metrics, run_dir))
    if not runs:
        raise SystemExit(f"No complete stationary runs found at {runs_dir}")
    return runs


def main() -> None:
    """Log each local run, saving its W&B link and updating the result report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=RUNS_DIR,
                        help="root directory containing dataset/model/seed run artifacts")
    parser.add_argument("--links-output", type=Path, default=LINKS_OUTPUT,
                        help="CSV file where per-run W&B URLs are kept")
    parser.add_argument("--report-output", type=Path, default=REPORT_OUTPUT,
                        help="results Markdown file to update with the W&B project link")
    parser.add_argument("--slide-output", type=Path, default=SLIDE_OUTPUT,
                        help="Phúc's slide Markdown file to update with W&B run links")
    args = parser.parse_args()
    load_dotenv(override=False)
    if os.getenv("WANDB_MODE", "disabled") != "online":
        raise SystemExit("Set WANDB_MODE=online and configure W&B credentials first.")
    try:
        import wandb
    except ImportError as exc:
        raise SystemExit('Install W&B with `python -m pip install -e ".[wandb]"`.') from exc
    try:
        wandb.Api()
    except wandb.errors.UsageError as exc:
        raise SystemExit(
            "No W&B API key is available. Run `wandb login` locally, or set "
            "WANDB_API_KEY in the ignored .env file."
        ) from exc

    runs = load_local_runs(args.runs_dir)
    links = read_links(args.links_output)
    uploaded_now = 0
    for key, config, metrics, run_dir in runs:
        if key in links:
            continue
        url = log_run(config, metrics, run_dir)
        if not url:
            raise RuntimeError(f"W&B did not return a run URL for {run_dir}")
        links[key] = {
            "dataset": key[0], "model": key[1], "seed": str(key[2]), "url": url,
        }
        write_links(args.links_output, links)
        update_status(args.report_output, args.links_output, links, len(runs))
        update_status(args.slide_output, args.links_output, links, len(runs))
        print(f"{key[0]} {key[1]} seed={key[2]} {url}", flush=True)
        uploaded_now += 1

    update_status(args.report_output, args.links_output, links, len(runs))
    update_status(args.slide_output, args.links_output, links, len(runs))
    print(f"Uploaded {uploaded_now} new run(s); {len(links)} link(s) in {args.links_output}")


if __name__ == "__main__":
    main()
