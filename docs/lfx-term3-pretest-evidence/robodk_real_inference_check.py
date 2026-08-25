#!/usr/bin/env python3
"""Run the exact PR #736 predict method with a real YOLO model and image."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from ultralytics import YOLO


def extract_predict(source: Path):
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    cls = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "BaseModel"
    )
    method = next(
        node
        for node in cls.body
        if isinstance(node, ast.FunctionDef) and node.name == "predict"
    )
    module = ast.Module(body=[method], type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {"Path": Path, "np": np}
    exec(compile(module, str(source), "exec"), namespace)
    return namespace["predict"]


class CountingModel:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.calls = 0

    def predict(self, **kwargs):
        self.calls += 1
        return self.model.predict(**kwargs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--model", default="yolov8n.pt")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    predict = extract_predict(args.source)
    model = CountingModel(args.model)
    subject = SimpleNamespace(model=model, device=args.device)

    empty_result = predict(subject, [])
    calls_after_empty = model.calls
    image_result = predict(subject, [str(args.image.resolve())])
    calls_after_image = model.calls
    detection_count = sum(len(values) for values in image_result.values())

    print("source:", args.source)
    print("image:", args.image)
    print("model:", args.model)
    print("device:", args.device)
    print("empty result:", empty_result)
    print("model calls after empty input:", calls_after_empty)
    print("one-image result keys:", list(image_result))
    print("one-image detection count:", detection_count)
    print("model calls after one-image input:", calls_after_image)


if __name__ == "__main__":
    main()
