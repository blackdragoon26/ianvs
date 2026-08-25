# Immutable source map for the pre-test submission

Status: published supporting evidence.

## Mandatory targets

### Core aggregation contract - Issue #565 / PR #566

- [PR head guard, lines 78-85](https://github.com/kubeedge/ianvs/blob/176fad4cc863f8df28e6a880488d2da757661b43/core/testcasecontroller/algorithm/paradigm/federated_learning/federated_learning.py#L78-L85)
- [Target Issue #565](https://github.com/kubeedge/ianvs/issues/565)
- [Target PR #566](https://github.com/kubeedge/ianvs/pull/566)

### GovDoc2Poster contracts - Issue #700 / PR #705

- [Parser `.strip()` boundary, lines 61-78](https://github.com/kubeedge/ianvs/blob/b07ca3872a3fb26b238f5e40d903f4ae2a8155a7/examples/GovDoc2Poster/singletask_learning_bench/testalgorithms/gen/gov_parser.py#L61-L78)
- [Dataset item passed directly and null replaced by empty dict, lines 454-462](https://github.com/kubeedge/ianvs/blob/b07ca3872a3fb26b238f5e40d903f4ae2a8155a7/examples/GovDoc2Poster/singletask_learning_bench/testalgorithms/gen/basemodel.py#L454-L462)
- [PR file list/diff](https://github.com/kubeedge/ianvs/pull/705/files)
- [Target Issue #700](https://github.com/kubeedge/ianvs/issues/700)
- [Target PR #705](https://github.com/kubeedge/ianvs/pull/705)

### RoboDK prediction contract - Issue #731 / PR #736

- [Empty-input return, lines 270-294](https://github.com/kubeedge/ianvs/blob/67b59e2b38ebaf10d70d40a40d8071f5bde694d4/examples/RoboDK%20Palletizing/singletask_learning_bench/testalgorithms/basemodel.py#L270-L294)
- [Cleanup behavior, lines 163-172](https://github.com/kubeedge/ianvs/blob/67b59e2b38ebaf10d70d40a40d8071f5bde694d4/examples/RoboDK%20Palletizing/singletask_learning_bench/testalgorithms/basemodel.py#L163-L172)
- [Metric mapping consumer, lines 83-105](https://github.com/kubeedge/ianvs/blob/67b59e2b38ebaf10d70d40a40d8071f5bde694d4/examples/RoboDK%20Palletizing/singletask_learning_bench/testenv/map50.py#L83-L105)
- [Metric zero result paths, lines 125-142](https://github.com/kubeedge/ianvs/blob/67b59e2b38ebaf10d70d40a40d8071f5bde694d4/examples/RoboDK%20Palletizing/singletask_learning_bench/testenv/map50.py#L125-L142)
- [Target Issue #731](https://github.com/kubeedge/ianvs/issues/731)
- [Target PR #736](https://github.com/kubeedge/ianvs/pull/736)

## Bonus targets

### FedLLM key association - PRs #649 and #770

- [PR #649 independent dictionary value extraction, lines 22-26](https://github.com/kubeedge/ianvs/blob/c24707654c5f765affceaf78936f9432465d6ad0/examples/federated-llm/fedllm-peft/testenv/bleu4_metric.py#L22-L26)
- [PR #770 independent dictionary value extraction, lines 22-26](https://github.com/kubeedge/ianvs/blob/13d0ebeb53b505eacc069800a9d0c2a9d6ca9b5a/examples/federated-llm/fedllm-peft/testenv/bleu4_metric.py#L22-L26)
- [Target Issue #646](https://github.com/kubeedge/ianvs/issues/646)
- [Target PR #649](https://github.com/kubeedge/ianvs/pull/649)
- [Target PR #770](https://github.com/kubeedge/ianvs/pull/770)

### GovDoc result aggregation - PR #721

- [Missing-key selection and unchecked null aggregation, lines 872-892](https://github.com/kubeedge/ianvs/blob/5b3b9978c5fe37324eb0e03b132ed5a79560e949/examples/GovDoc2Poster/singletask_learning_bench/testalgorithms/gen/basemodel.py#L872-L892)
- [Target Issue #720](https://github.com/kubeedge/ianvs/issues/720)
- [Target PR #721](https://github.com/kubeedge/ianvs/pull/721)

## Reproduction controls

- Missing aggregation fails at the base and produces a contextual error at the
  head; a valid initialized tuple remains successful.
- GovDoc dict input fails while a valid string passes through the same extracted
  method with deterministic collaborator stubs.
- RoboDK empty input and a one-image/zero-detection run both return `{}`, while
  the model-call counter is `0` and `1` respectively. The payload alone cannot
  distinguish the states.
- FedLLM opposite dictionary insertion order mispairs samples; matching order is
  the passing control.
- GovDoc `evaluation=None` crashes; a missing-key result is counted and handled
  by the passing control.
