# LFX 2026 Term 3 pre-test evidence

This directory contains the dependency-light reproduction used for the Example
Restoration pre-test analysis of Issues #565, #700, and #731 and PRs #566,
#705, and #736. It also covers the supplementary reviews of PRs #649, #770,
and #721.

The runner fetches each PR ref, verifies its exact commit SHA, creates detached
worktrees, executes the relevant production function bodies with collaborators
stubbed only at dependency boundaries, and runs `git diff --check` on every PR
worktree.

## Run

From an Ianvs clone:

```shell
docs/lfx-term3-pretest-evidence/prepare_and_run_pretest_evidence.sh \
  /path/to/ianvs /path/to/python3
```

The Python environment needs NumPy for the RoboDK metric case. The runner
retains its temporary worktrees and prints their location so the extracted
source can be inspected after execution.

## Recorded heads

| PR | Commit |
| --- | --- |
| #566 | `176fad4cc863f8df28e6a880488d2da757661b43` |
| #705 | `b07ca3872a3fb26b238f5e40d903f4ae2a8155a7` |
| #736 | `67b59e2b38ebaf10d70d40a40d8071f5bde694d4` |
| #649 | `c24707654c5f765affceaf78936f9432465d6ad0` |
| #770 | `13d0ebeb53b505eacc069800a9d0c2a9d6ca9b5a` |
| #721 | `5b3b9978c5fe37324eb0e03b132ed5a79560e949` |

## Verification boundary

The completed checks cover the exact boundary functions and include failing
and passing controls. They do not claim full federated training, external
LLM/VLM calls, model or metric downloads, complete datasets, GPU execution, or
RoboDK hardware execution.

`pretest-contract-transcript.png` is a rendered image of the exact raw output
from the SHA-verified run. It is provided for readable evidence and is not
described as a photograph of a terminal window.
