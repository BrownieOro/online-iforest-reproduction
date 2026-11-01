import sys
from types import SimpleNamespace
import pytest
from oif.tracking import log_run


def test_disabled_needs_no_wandb(tmp_path, monkeypatch):
    monkeypatch.setenv("WANDB_MODE", "disabled")
    monkeypatch.setitem(sys.modules, "wandb", None)
    assert log_run({}, {}, tmp_path) is None


def test_offline_logs_metrics_and_artifact(tmp_path, monkeypatch):
    calls = {}
    class Run:
        id = "test"
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def log(self, metrics):
            calls["metrics"] = metrics
        def log_artifact(self, artifact):
            calls["files"] = artifact.files
    class Artifact:
        def __init__(self, *args, **kwargs):
            self.files = []
        def add_file(self, path):
            self.files.append(path)
    def init(**kwargs):
        calls["config"] = kwargs
        return Run()
    monkeypatch.setenv("WANDB_MODE", "offline")
    monkeypatch.setitem(sys.modules, "wandb", SimpleNamespace(init=init, Artifact=Artifact))
    assert log_run({"seed": 42}, {"roc_auc": None, "n_test": 10}, tmp_path) is None
    assert calls["metrics"] == {"n_test": 10}
    assert calls["config"]["mode"] == "offline"
    assert len(calls["files"]) == 3
