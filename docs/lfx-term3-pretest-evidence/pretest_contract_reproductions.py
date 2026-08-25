#!/usr/bin/env python3
"""Dependency-light reproductions for the LFX Term 3 pre-test evidence bundle."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import subprocess
from threading import RLock
from types import SimpleNamespace
from typing import Any, Dict, Optional


review_root_value = os.environ.get("IANVS_PRETEST_REVIEW_ROOT")
if not review_root_value:
    raise SystemExit(
        "IANVS_PRETEST_REVIEW_ROOT is required; use "
        "evidence/prepare_and_run_pretest_evidence.sh"
    )
ROOT = Path(review_root_value).resolve()


def extract_method(path: Path, class_name: str, method_name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                    module = ast.Module(body=[item], type_ignores=[])
                    ast.fix_missing_locations(module)
                    namespace = {
                        "Any": Any,
                        "Dict": Dict,
                        "Optional": Optional,
                        "Path": Path,
                        "os": os,
                        "json": json,
                        "RLock": RLock,
                    }
                    exec(compile(module, str(path), "exec"), namespace)
                    return namespace[method_name]
    raise LookupError(f"{class_name}.{method_name} not found in {path}")


class LoggerStub:
    def info(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass


def reproduce_pr566():
    rel = Path("core/testcasecontroller/algorithm/paradigm/federated_learning/federated_learning.py")
    base_path = ROOT / "pr566-base" / rel
    head_path = ROOT / "pr566" / rel

    class ParadigmBaseStub:
        def __init__(self, workspace, **kwargs):
            self.module_instances = kwargs["module_instances"]

    module_type = SimpleNamespace(AGGREGATION=SimpleNamespace(value="aggregation"))
    logger = LoggerStub()

    def load_init(path):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "FederatedLearning")
        init = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "__init__")
        module = ast.Module(body=[init], type_ignores=[])
        ast.fix_missing_locations(module)
        namespace = {
            "ParadigmBase": ParadigmBaseStub,
            "ModuleType": module_type,
            "LOGGER": logger,
            "RLock": RLock,
        }
        exec(compile(module, str(path), "exec"), namespace)
        return namespace["__init__"]

    base_init = load_init(base_path)
    head_init = load_init(head_path)

    def outcome(initializer, modules):
        obj = SimpleNamespace()
        try:
            initializer(obj, "/tmp/work", module_instances=modules)
            return "OK"
        except Exception as exc:  # evidence records the exact public exception contract
            return f"{type(exc).__name__}: {exc}"

    print("PR566 missing aggregation, base:", outcome(base_init, {}))
    print("PR566 missing aggregation, head:", outcome(head_init, {}))
    print("PR566 null aggregation instance, head:", outcome(head_init, {"aggregation": ("agg", None)}))
    print("PR566 valid aggregation, head:", outcome(head_init, {"aggregation": ("agg", object())}))


def reproduce_pr705():
    rel = Path("examples/GovDoc2Poster/singletask_learning_bench/testalgorithms/gen/gov_parser.py")
    parse_document = extract_method(ROOT / "pr705" / rel, "NewGovernmentDocumentParser", "parse_document")
    parser = SimpleNamespace(
        logger=LoggerStub(),
        _analyze_with_llm=lambda text: {"main_topic": "test"},
        _classify_document_type=lambda text: "policy",
        _extract_key_information=lambda text, structured: {"main_topic": "test"},
        _generate_summary=lambda text, rule_type: "summary",
    )
    try:
        parse_document(parser, {"question": "sample.pdf"})
        outcome = "OK"
    except Exception as exc:
        outcome = f"{type(exc).__name__}: {exc}"
    print("PR705 dict input at parser boundary, head:", outcome)
    string_result = parse_document(parser, "valid policy text")
    print(
        "PR705 valid string control, head:",
        {"rule_type": string_result["rule_type"], "summary": string_result["summary"]},
    )

    changed = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT / "pr705"),
            "diff",
            "--name-only",
            "36ec0087c0919989ca305eb593c739bb1e97509d..HEAD",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    print("PR705 changes gov_planner.py:", any(name.endswith("gov_planner.py") for name in changed))
    print("PR705 changes gov_painter.py:", any(name.endswith("gov_painter.py") for name in changed))

    example = ROOT / "pr705" / "examples/GovDoc2Poster"
    print("PR705 sample.pdf exists:", (example / "resources/datasets/sample.pdf").exists())
    print("PR705 sample.png exists:", (example / "resources/datasets/sample.png").exists())


def reproduce_pr736():
    import numpy as np

    rel = Path("examples/RoboDK Palletizing/singletask_learning_bench/testalgorithms/basemodel.py")
    base_predict = extract_method(ROOT / "pr736-base" / rel, "BaseModel", "predict")
    head_predict = extract_method(ROOT / "pr736" / rel, "BaseModel", "predict")
    base_predict.__globals__["np"] = np
    head_predict.__globals__["np"] = np

    class ModelStub:
        def __init__(self):
            self.calls = 0

        def predict(self, **kwargs):
            self.calls += 1
            return []

    model = ModelStub()
    obj = SimpleNamespace(model=model, device="cpu")
    print("PR736 predict([]), base:", repr(base_predict(obj, [])))
    print("PR736 predict([]), head:", repr(head_predict(obj, [])))
    print("PR736 model calls after empty input, head:", model.calls)
    zero_detection_result = head_predict(obj, ["image.png"])
    print("PR736 one-image zero-detection result, head:", repr(zero_detection_result))
    print("PR736 model calls after one-image input, head:", model.calls)
    print("PR736 downstream .get on base result:", end=" ")
    try:
        base_predict(obj, []).get("image.png", [])
        print("OK")
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}")
    print("PR736 downstream .get on head result:", head_predict(obj, []).get("image.png", []))

    metric_path = ROOT / "pr736" / Path(
        "examples/RoboDK Palletizing/singletask_learning_bench/testenv/map50.py"
    )
    tree = ast.parse(metric_path.read_text(encoding="utf-8"), filename=str(metric_path))
    selected = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {
            "xywh2xyxy_rel",
            "read_label_file",
            "map50",
        }:
            node.decorator_list = []
            selected.append(node)
    module = ast.Module(body=selected, type_ignores=[])
    ast.fix_missing_locations(module)
    metric_namespace = {
        "Path": Path,
        "np": np,
        "tqdm": lambda values, **kwargs: values,
        "torch": SimpleNamespace(),
        "ap_per_class": lambda *args: (None, None, None, None, None, np.zeros((1, 1))),
        "box_iou": None,
        "logger": LoggerStub(),
    }
    exec(compile(module, str(metric_path), "exec"), metric_namespace)
    label_path = Path(__file__).with_name("fixtures") / "robodk-label.txt"
    score = metric_namespace["map50"]([str(label_path)], head_predict(obj, []))
    print("PR736 map50 with one label and empty prediction dict:", score)


def reproduce_bonus_metric_prs():
    rel = Path("examples/federated-llm/fedllm-peft/testenv/bleu4_metric.py")

    class MetricRecorder:
        def __init__(self):
            self.arguments = None

        def compute(self, **kwargs):
            self.arguments = kwargs
            return {"bleu": 0.0}

    for pr_number in (649, 770):
        path = ROOT / f"pr{pr_number}" / rel
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        func = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
        func.decorator_list = []
        module = ast.Module(body=[func], type_ignores=[])
        ast.fix_missing_locations(module)
        recorder = MetricRecorder()
        namespace = {"load_metric": lambda name: recorder}
        exec(compile(module, str(path), "exec"), namespace)
        truth = {"a": "reference-A", "b": "reference-B"}
        predictions = {"b": "prediction-B", "a": "prediction-A"}
        namespace["bleu4_metric"](truth, predictions)
        print(f"PR{pr_number} BLEU arguments with opposite dict insertion order:", recorder.arguments)
        recorder.arguments = None
        namespace["bleu4_metric"](
            truth,
            {"a": "prediction-A", "b": "prediction-B"},
        )
        print(f"PR{pr_number} BLEU matching-order control:", recorder.arguments)


def reproduce_bonus_pr721():
    rel = Path("examples/GovDoc2Poster/singletask_learning_bench/testalgorithms/gen/basemodel.py")
    format_results = extract_method(ROOT / "pr721" / rel, "NewGovernmentPosterAgent", "_format_results")
    agent = SimpleNamespace(
        logger=LoggerStub(),
        _calculate_optimization_stats=lambda results: {},
    )
    results = [
        {"evaluation": {"score": 8.0}, "processing_time": 1.0},
        {"evaluation": None, "processing_time": 1.0},
        {"error": "parse failed", "processing_time": 1.0},
    ]
    try:
        formatted = format_results(agent, results)
        outcome = formatted["average_scores"]
    except Exception as exc:
        outcome = f"{type(exc).__name__}: {exc}"
    print("PR721 evaluation=None outcome:", outcome)
    control = format_results(
        agent,
        [
            {"evaluation": {"score": 8.0}, "processing_time": 1.0},
            {"error": "parse failed", "processing_time": 1.0},
        ],
    )
    print("PR721 missing-key control:", control["average_scores"])


if __name__ == "__main__":
    reproduce_pr566()
    reproduce_pr705()
    reproduce_pr736()
    reproduce_bonus_metric_prs()
    reproduce_bonus_pr721()
