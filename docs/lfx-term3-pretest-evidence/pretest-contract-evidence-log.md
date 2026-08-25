# LFX 2026 Term 3 - Boundary-contract evidence log

Status: published supporting evidence; observations remain time-scoped to the
recorded revisions and audit dates.

## Evidence identity

- Audit time: `2026-08-24T14:35:03Z`
- Final hardening recheck: `2026-08-24T15:16:20Z`
- Resource follow-up: `2026-08-25T09:08:58Z`
- Self-contained runner recheck: `2026-08-25T09:53:22Z`
- Host: macOS 26.4.1 (25E253), arm64
- Repository: `kubeedge/ianvs`
- Current upstream main: `37a9c60a9747af0cfe3170f84249bc349c56e8d5`
- System Python: 3.14.5
- Bundled evidence Python: 3.12.13
- Evidence script: `evidence/pretest_contract_reproductions.py`
- Preparation runner: `evidence/prepare_and_run_pretest_evidence.sh`
- Immutable line map: `evidence/pretest-source-map.md`
- Rendered execution transcript: `evidence/pretest-contract-transcript.png`
- Fixture: `evidence/fixtures/robodk-label.txt`
- Resource audit: `evidence/pretest-resource-audit.md`
- Real-model runner: `evidence/robodk_real_inference_check.py`

## Target snapshot

All targets below were open, non-draft, and mergeable when queried. DCO passed;
Tide remained pending because no project approval was present.

| Target | Exact head | Role |
| --- | --- | --- |
| PR #566 | `176fad4cc863f8df28e6a880488d2da757661b43` | Mandatory critical/Core PR |
| PR #705 | `b07ca3872a3fb26b238f5e40d903f4ae2a8155a7` | Mandatory GovDoc2Poster PR |
| PR #736 | `67b59e2b38ebaf10d70d40a40d8071f5bde694d4` | Mandatory RoboDK Palletizing PR |
| PR #649 | `c24707654c5f765affceaf78936f9432465d6ad0` | Bonus FedLLM metric PR |
| PR #770 | `13d0ebeb53b505eacc069800a9d0c2a9d6ca9b5a` | Bonus competing FedLLM metric PR |
| PR #721 | `5b3b9978c5fe37324eb0e03b132ed5a79560e949` | Bonus GovDoc2Poster aggregation PR |

The matching mandatory Issues #565, #700, and #731 were also open. None of
these six mandatory target numbers appeared in the body or comments of the
Example Restoration pre-test Discussions found in the live repository query
through Discussion #906.

The final hardening recheck found both primary and fallback sets still open and
non-draft at the recorded heads, with zero Discussion collisions for either
target-number set.

## Isolation method

Each PR head was fetched from `refs/pull/<number>/head` into a `prep/review-*`
branch and checked out into a separate temporary worktree. The base revisions
used for behavioral comparison were:

- PR #566 base: `bf0f59680cea87bd5ff32283183a61ec4cf34d00`
- PRs #705/#721/#736 base: `36ec0087c0919989ca305eb593c739bb1e97509d`
- PR #649 base: `38a5319b677c39379e2d1b6ab82db6e882c315b8`
- PR #770 base: `36ec0087c0919989ca305eb593c739bb1e97509d`

No PR branch was edited. The reproducer loads the exact target functions from
their source AST and supplies only dependency-boundary stubs. This executes the
target function bodies without claiming that unavailable ML stacks ran.

## Commands

```shell
evidence/prepare_and_run_pretest_evidence.sh /path/to/ianvs /path/to/python3
```

The runner fetches each pull-request ref, verifies its exact SHA before adding
the detached worktree, adds the recorded bases, executes the reproducer, and
runs `diff --check`. After removing the reproducer's stale temporary-path
dependency, a fresh run retained its verified worktrees at
`/tmp/ianvs-pretest.e6emVA`. `diff --check` produced no output for all six
heads.

## Raw behavioral output

```text
PR566 missing aggregation, base: TypeError: cannot unpack non-iterable NoneType object
PR566 missing aggregation, head: ValueError: FederatedLearning requires an 'aggregation' module but none was found or successfully initialized. Add an 'aggregation' entry under 'modules:' in your algorithm YAML.
PR566 null aggregation instance, head: ValueError: FederatedLearning requires an 'aggregation' module but none was found or successfully initialized. Add an 'aggregation' entry under 'modules:' in your algorithm YAML.
PR566 valid aggregation, head: OK
PR705 dict input at parser boundary, head: AttributeError: 'dict' object has no attribute 'strip'
PR705 valid string control, head: {'rule_type': 'policy', 'summary': 'summary'}
PR705 changes gov_planner.py: False
PR705 changes gov_painter.py: False
PR705 sample.pdf exists: False
PR705 sample.png exists: False
PR736 predict([]), base: []
PR736 predict([]), head: {}
PR736 model calls after empty input, head: 0
PR736 one-image zero-detection result, head: {}
PR736 model calls after one-image input, head: 1
PR736 downstream .get on base result: AttributeError: 'list' object has no attribute 'get'
PR736 downstream .get on head result: []
PR736 map50 with one label and empty prediction dict: 0.0
PR649 BLEU arguments with opposite dict insertion order: {'predictions': ['prediction-B', 'prediction-A'], 'references': [['reference-A'], ['reference-B']]}
PR649 BLEU matching-order control: {'predictions': ['prediction-A', 'prediction-B'], 'references': [['reference-A'], ['reference-B']]}
PR770 BLEU arguments with opposite dict insertion order: {'predictions': ['prediction-B', 'prediction-A'], 'references': [['reference-A'], ['reference-B']]}
PR770 BLEU matching-order control: {'predictions': ['prediction-A', 'prediction-B'], 'references': [['reference-A'], ['reference-B']]}
PR721 evaluation=None outcome: AttributeError: 'NoneType' object has no attribute 'get'
PR721 missing-key control: {'avg_score': 8.0, 'evaluated_count': 1, 'skipped_count': 1}
```

## Interpretation and verification boundary

### PR #566

Executed: exact base/head `FederatedLearning.__init__` bodies with the Core
module-instance boundary stubbed. The head replaces an opaque unpacking error
with an actionable error and preserves the valid path. This verifies the guard,
not a distributed federated-learning run.

### PR #705

Executed: the exact head `parse_document` body with the Issue #700 dictionary
shape. It still calls `.strip()` on the dictionary. Source/diff inspection also
shows no planner or painter file change, and the newly declared `sample.pdf`
and `sample.png` do not exist in the tree. No external LLM/VLM API or complete
poster pipeline was run. The same extracted parser method succeeds for a valid
string with deterministic collaborator stubs, providing a negative control.

### PR #736

Executed first: the exact base/head `predict` early-return path and the exact
head `map50` function with one label fixture, an empty prediction dictionary,
and only the unavailable AP implementation stubbed. The PR eliminates
`.get()`'s type exception, but the metric emits `0.0`, making missing inference
indistinguishable from a valid zero-performing model.

The resource follow-up then downloaded the documented public dataset and
public `yolov8n.pt` weights and ran the exact PR #736 `BaseModel.predict` body
with a real YOLO model on an actual test image. Empty input returned `{}` with
zero model calls. The test image completed one CPU model call, produced zero
detections, and returned a mapping whose value was an empty detection list.
This replaces the earlier assumption that the model and dataset were
unavailable. The full 30-epoch Ianvs train/evaluate benchmark remains
unexecuted; its YAML and dataset indexes contain `/root/ianvs/project/...`
paths, and CUDA/MPS were unavailable in the isolated runtime.

### Bonus PRs

Executed: exact BLEU callback bodies from #649 and #770 with a metric recorder.
Both patches orient arguments correctly but pair dictionary values by insertion
order rather than a shared key. Exact #721 `_format_results` execution shows
that an explicit `evaluation: None` is counted as evaluated and crashes.

## Publication state

The rendered transcript, dependency-light runner, source map, and evidence log
were published in the stable evidence bundle referenced by Discussion #916.
The resource audit and real-model runner are follow-up additions that must use
a new immutable commit link before the email attachment is sent.

## Missing-fix search ledger

Live open-PR searches at the audit cutoff found:

```text
GovDoc2Poster + strip                         -> PR #705 only
RoboDK Palletizing + empty + predict         -> PR #736 and unrelated #426
"contract test" + aggregation               -> 0 results
```

PR #426 changes only `examples/government/...`, not RoboDK Palletizing. Exact
diff inspection of #705/#736 shows neither adds tests. These searches support,
but do not permanently prove, the missing-fix claim; they must be repeated just
before publication.

## Link verification

All 22 Issue, PR, diff, and immutable blob links in
`evidence/pretest-source-map.md` returned HTTP `200` on 2026-08-24. Fragment
line ranges were additionally checked against the exact local PR worktrees.
This result is time-scoped and must be repeated for the final submission link
ledger.
