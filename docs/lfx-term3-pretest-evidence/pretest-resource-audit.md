# LFX 2026 Term 3 - Resource and real-inference audit

Audit time: `2026-08-25T09:08:58Z`

## RoboDK Palletizing

The benchmark path reviewed in PR #736 consumes an exported image/label
dataset. The RoboDK application or physical robotics hardware is not required
to execute this prediction/metric boundary after the dataset has been
generated.

Completed checks:

- The documented Kaggle archive was reachable without Kaggle credentials.
- Downloaded size: `81,930,557` bytes.
- Archive SHA-256:
  `2e080d93ef358e2245eb899d280ccd06cc799f9cd9a6998d5995236ce325ea43`.
- Archive inventory: `10,598` files, including `1,004` training-index rows and
  `455` test-index rows.
- The archive includes paired train/test images and YOLO label files.
- Public `yolov8n.pt` weights downloaded successfully from the Ultralytics
  release used by the installed runtime.
- Ultralytics `8.4.128` and PyTorch `2.13.0` were installed in an isolated
  temporary Python 3.12 environment.
- A real CPU inference on
  `snapshot_20250903_105659.png` completed and produced zero detections.
- The exact PR #736 `BaseModel.predict` body returned `{}` for empty input with
  zero model calls, and a one-image mapping after one real model call. This
  confirms the two states can share an empty-prediction payload even when the
  model genuinely executes for the second state.
- `robodk-real-inference.mp4` is a 15-second rendered evidence summary showing
  the exact command boundary, the dataset image, and the observed control/result.
  Its SHA-256 is
  `6b8b695038285f6c0db9fd40532e4fb881e8c0fd57e5b65a03b33dc388a970ca`.
  It is not represented as a live terminal screen recording; the runnable
  script and raw observations remain the authoritative evidence.

The full Ianvs train/evaluate benchmark remains unexecuted. Its committed YAML
and dataset indexes contain `/root/ianvs/project/...` paths that do not match
this macOS checkout, it requests 30 training epochs, and the current temporary
PyTorch build reports CUDA and MPS unavailable. These are full-run setup and
compute constraints, not absence of the public dataset or pretrained model.

## GovDoc2Poster

The committed train/test JSONL rows reference
`resources/datasets/sample.pdf` and `resources/datasets/sample.png`, but those
files are absent at PR #705 head. The code contains the placeholder
`self.api_key = 'your_api'`; no `DASHSCOPE_API_KEY` is configured in the current
environment. Therefore the external LLM/VLM poster pipeline was not executed.
The exact parser boundary and deterministic string control remain the completed
verification for the reviewed defect.

## Core federated path

The exact base/head constructor behavior is verified. A distributed federated
training run was not attempted because the reviewed claim concerns required
aggregation-module initialization, and the dependency-light missing/null/valid
controls execute that changed boundary directly.

## Reproduction commands

```shell
curl -L -o robodk-palletizing.zip \
  https://www.kaggle.com/api/v1/datasets/download/kubeedgeianvs/the-robodk-palletizing-dataset

python3 -m venv .venv
.venv/bin/pip install ultralytics

.venv/bin/python evidence/robodk_real_inference_check.py \
  --source /path/to/pr736/examples/RoboDK\ Palletizing/singletask_learning_bench/testalgorithms/basemodel.py \
  --image /path/to/RoboDK_Palletizing_Dataset/images/test/snapshot_20250903_105659.png \
  --model yolov8n.pt \
  --device cpu
```
