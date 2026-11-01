"""Shared opt-in W&B logging. Local artifacts are written before this is called."""
import os
from dotenv import load_dotenv


def log_run(config, metrics, output):
    load_dotenv(override=False)
    mode = os.getenv("WANDB_MODE", "disabled")
    if mode == "disabled":
        return None
    if mode not in {"offline", "online"}:
        raise ValueError("WANDB_MODE must be disabled, offline or online")
    import wandb
    with wandb.init(project=os.getenv("WANDB_PROJECT", "intro-ml-oif"),
                    entity=os.getenv("WANDB_ENTITY") or None, mode=mode,
                    job_type="baseline", config=config) as run:
        run.log({k: v for k, v in metrics.items() if isinstance(v, (int, float))})
        artifact = wandb.Artifact(f"baseline-{run.id}", type="evaluation")
        for name in ("config.json", "metrics.json", "predictions.csv"):
            artifact.add_file(str(output / name))
        run.log_artifact(artifact)
        return run.url if mode == "online" else None
