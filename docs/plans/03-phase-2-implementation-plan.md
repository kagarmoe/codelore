# CodeLore Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the corpus audit, kernel specs, and git-first ingestion path that turns `gastown v1.1.0 -> v1.2.0` into a canonical, byte-identical-on-rebuild evidence pack of artifact and link records.

**Architecture:** Staged pipeline per `docs/plans/00b-development-plan-evidence-first.md`: acquire (git) -> window -> normalize -> assemble, with a run manifest recording per-stage counts. The pack is a directory of canonical JSONL collections (manifest, project, window, artifacts, links). All identifiers are content-addressed via a canonical byte encoding; run-scoped metadata lives only in the manifest so record bytes replay identically.

**Tech Stack:** Python 3.13, uv, pydantic v2 (frozen models), typer CLI, plain `git` subprocess for ingestion (decision recorded in Task 3), pytest + Hypothesis, ruff, GitHub Actions.

## Global Constraints

- Python `>=3.13`; dependency management via `uv`; ruff line-length 88 (existing pyproject).
- Zero model (LLM) calls anywhere in Phase 2 — this phase is hard-deterministic.
- Record bodies must contain no run-scoped or wall-clock fields; run provenance lives in the run manifest (amends the `LinkRecord` field list in `docs/plans/02-data-engineering-infrastructure-plan.md`: `run_id`/`created_at` move to the manifest).
- Canonical serialization: UTF-8, NFC-normalized strings, sorted keys, compact separators, RFC3339 UTC `Z` timestamps, no floats, record arrays sorted by ID, LF newlines.
- Canonical pack form: directory with `manifest.json`, `project.json`, `window.json`, `artifacts.jsonl`, `links.jsonl` (per adopted plan 02).
- IDs: `{prefix}:{sha256(canonical_encode(fields)).hexdigest()[:16]}`; input fields per record type are fixed in `docs/architecture/11-id-and-serialization-spec.md` (Task 3).
- Release/tag resolution happens only at the CLI edge; core builder receives resolved SHAs.
- Every task ends with `uv run ruff check .` and `uv run pytest -q` passing before commit.

---

### Task 1: Corpus audit memo

**Files:**
- Create: `docs/validation/08-gastown-corpus-audit.md`

**Interfaces:**
- Produces: audited counts (all-ancestry commits, first-parent commits, merges, changed files, docs, tests, PRs, issues) and the window-membership policy consumed by Tasks 2 and 12.

- [ ] **Step 1: Repoint the local gastown clone and fetch**

```bash
git -C /home/kimberly/repos/gastown remote set-url origin https://github.com/gastownhall/gastown.git
git -C /home/kimberly/repos/gastown fetch origin --tags --prune
git -C /home/kimberly/repos/gastown tag -l 'v1.1.0' 'v1.2.0'
```

Expected: both tags listed.

- [ ] **Step 2: Collect ingester-side counts**

```bash
cd /home/kimberly/repos/gastown
git rev-list --count v1.2.0 ^v1.1.0                 # all-ancestry commits
git rev-list --count --first-parent v1.2.0 ^v1.1.0  # first-parent commits
git rev-list --count --merges v1.2.0 ^v1.1.0        # merges
git log --oneline v1.1.0..v1.2.0 | grep -cE '\(#[0-9]+\)' # squash-suffix commits
git diff --name-only v1.1.0..v1.2.0 | wc -l          # changed files
git diff --name-only v1.1.0..v1.2.0 | grep -cE '(^docs/|\.md$)'  # doc changes
git diff --name-only v1.1.0..v1.2.0 | grep -cE '(^tests?/|(^|/)test_)' # test changes
ls CHANGELOG.md docs/release/ 2>/dev/null            # changelog / release evidence
```

- [ ] **Step 3: Collect independent counts (not via the local ingester path)**

```bash
gh api repos/gastownhall/gastown/compare/v1.1.0...v1.2.0 --jq '{total_commits, files: (.files|length)}'
gh api --paginate 'repos/gastownhall/gastown/pulls?state=closed&base=main&per_page=100' \
  --jq '[.[] | select(.merged_at != null)] | length'   # sanity count; window-scope by merged_at manually
```

Record tag dates to bound PR/issue windowing: `git log -1 --format=%cI v1.1.0` and `v1.2.0`.

- [ ] **Step 4: Write the memo**

Write `docs/validation/08-gastown-corpus-audit.md` with these sections (fill counts from Steps 2–3; do not leave blanks):

```markdown
# Gastown Corpus Audit: v1.1.0 -> v1.2.0

## Window-Membership Policy (normative for Phase 2)
- Reachability: `v1.2.0 ^v1.1.0` (all commits reachable from end, not start).
- Traversal: all-ancestry is the window set; first-parent membership is
  annotated per commit, not a separate window.
- Timestamp authority: committer date, rendered RFC3339 UTC.
- Out-of-window author dates: counted and reported as a known artifact class.

## Merge Style
[merge-commit / squash / mixed, from step-2 ratios]

## Counts (ingester-side)
[all-ancestry, first-parent, merges, squash-suffixed, changed files, docs, tests]

## Counts (independent cross-check)
[GitHub compare API totals; note any divergence and its cause]

## Artifact-Class Inventory
[PRs merged in window, issues closed in window, changelog present?, release
notes / release-evidence docs present?]

## Verification Record
- [ ] Phase 2 exit check: `codelore build-window` counts match this memo (Task 12)
```

- [ ] **Step 5: Commit**

```bash
git add docs/validation/08-gastown-corpus-audit.md
git commit -m "docs: gastown v1.1.0->v1.2.0 corpus audit with window-membership policy"
```

---

### Task 2: Golden question set

**Files:**
- Create: `docs/validation/09-golden-question-set.md`

**Interfaces:**
- Consumes: audit counts and artifact inventory from Task 1.
- Produces: the disconfirmation baseline cited by Phases 3–5 exit criteria.

- [ ] **Step 1: Draft five concrete questions**

Instantiate the five acceptance categories from `docs/validation/04-gastown-slice-acceptance.md` against the real window. Template:

```markdown
# Golden Question Set: gastown v1.1.0 -> v1.2.0

Each question lists the expected supporting artifacts (commit SHAs, PR
numbers, file paths) found by hand. Verification status is per question.

## Q1 (what changed): What changed in v1.2.0 relative to v1.1.0?
Expected support: [top-level change list drawn from release notes/changelog,
each item paired with >=1 commit SHA or PR number]
Verified by hand: [ ]

## Q2 (provenance): Which issues, PRs, commits, and diffs support <specific
change picked from Q1>?
Expected support: [exact PR number, commit SHAs, file paths]
Verified by hand: [ ]

## Q3 (explicit problem): Which problems are explicitly stated in release
artifacts for this window?
Expected support: [issue/PR bodies with the stating text located]
Verified by hand: [ ]

## Q4 (explicit decision): Which decisions or tradeoffs are explicitly stated?
Expected support: [PR discussion / commit message / doc with the stating text]
Verified by hand: [ ]

## Q5 (unresolved): Which meaningful questions remain unresolved because
evidence is weak or absent?
Expected support: [named gaps; e.g. changes with no stated rationale]
Verified by hand: [ ]

## Single-rater limitation
This set is single-rater verified; declared per the Phase 3b audit protocol.
```

- [ ] **Step 2: Hand-verify each expected artifact exists (checkpoint: Kimberly)**

Each `Verified by hand` box is checked only after opening the named artifact and confirming the text/diff supports the question.

- [ ] **Step 3: Commit**

```bash
git add docs/validation/09-golden-question-set.md
git commit -m "docs: golden question set for the gastown slice"
```

---

### Task 3: ID and serialization specification

**Files:**
- Create: `docs/architecture/11-id-and-serialization-spec.md`

**Interfaces:**
- Produces: the normative spec Tasks 4–6 implement; ID input-field table; volatile-field policy; tooling decision record.

- [ ] **Step 1: Write the spec**

```markdown
# ID And Serialization Specification

## Canonical encoding (canonical_encode)
- dicts: keys sorted lexicographically; keys must be str
- strings: unicode-normalized to NFC
- integers and booleans: as-is; floats: rejected (ValueError)
- None: JSON null; lists/tuples: element order preserved
- datetimes: timezone-aware only; rendered RFC3339 UTC with "Z"
- output: UTF-8 bytes, compact separators ("," and ":"), ensure_ascii=False

## Record IDs
id = "{prefix}:{sha256(canonical_encode(fields)).hexdigest()[:16]}"
64-bit truncation is collision-safe at corpus scale; the spec permits
lengthening in a new pack_schema_version if a collision is ever observed
(collision handling: assembly fails closed on duplicate ID with distinct
canonical bytes).

## ID input fields per record type
| type      | prefix | fields                                              |
|-----------|--------|-----------------------------------------------------|
| Project   | (user-assigned slug, e.g. "gastown"; not hashed)             |
| Window    | win    | project_id, window_type, start_sha, end_sha         |
| Artifact  | art    | project_id, artifact_type, source_locator           |
| Link      | lnk    | window_id, relation_type, source_id, target_id      |

## Volatile-field policy
Record bodies never contain run IDs or wall-clock reads. `captured_at` on
artifacts is the committer timestamp (source-derived, deterministic).
`normalized_by` is a static component tag ("codelore-normalize/1"). Run
provenance (run_id, timestamps, invocation) lives only in manifest.json.
This amends plan 02's LinkRecord field list: run_id/created_at are
manifest-level.

## Pack layout (canonical form, pack_schema_version = "1")
evidence-pack/
  manifest.json     # run manifest; compared modulo volatile fields
  project.json      # single canonical JSON record
  window.json       # single canonical JSON record
  artifacts.jsonl   # one canonical JSON record per line, sorted by id
  links.jsonl       # one canonical JSON record per line, sorted by id
All files LF-terminated.

## Byte-identity contract
Replay (same inputs, same code) produces byte-identical files for every pack
file except manifest.json; manifest.json is compared after dropping
run_id/started_at/completed_at/invocation.

## Tooling decision (Phase 2 entry record)
Evaluated PyDriller and Perceval. Phase 2 uses plain `git` subprocess:
the needed surface (rev-list, show, diff name-status/numstat) is small,
transparent, and dependency-free, and window-membership policy control
(first-parent annotation) is explicit. PyDriller remains the fallback if
rename-detection or richer diff modeling is needed in Phase 3; Perceval
remains the reference model for forge snapshotting in Phase 3b.
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/11-id-and-serialization-spec.md
git commit -m "docs: ID scheme and canonical serialization specification"
```

---

### Task 4: Domain model updates (LinkRecord, enums, pack fields)

**Files:**
- Modify: `src/codelore/models.py`
- Test: `tests/test_models.py`

**Interfaces:**
- Produces: `RelationType`, `LinkMethod`, `MembershipType` (StrEnums); `LinkRecord` (frozen pydantic model with fields `link_id, window_id, relation_type, source_id, target_id, link_method, confidence: Confidence | None = None, membership_type: MembershipType | None = None, evidence_ids: tuple[str, ...] = ()`); `EvidencePack.links: tuple[LinkRecord, ...]` and `EvidencePack.pack_schema_version: str`; `Warrant` without `claim_id`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_models.py`:

```python
from codelore.models import (
    EvidencePack, LinkMethod, LinkRecord, MembershipType, RelationType, Warrant,
)


def test_link_record_is_frozen_and_typed():
    link = LinkRecord(
        link_id="lnk:abc",
        window_id="win:1",
        relation_type=RelationType.NATIVE_TO_WINDOW,
        source_id="win:1",
        target_id="art:1",
        link_method=LinkMethod.STRUCTURAL,
        membership_type=MembershipType.NATIVE,
    )
    assert link.confidence is None
    assert link.evidence_ids == ()


def test_warrant_has_no_claim_id():
    assert "claim_id" not in Warrant.model_fields


def test_evidence_pack_carries_links_and_schema_version():
    assert "links" in EvidencePack.model_fields
    assert "pack_schema_version" in EvidencePack.model_fields
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_models.py -q`
Expected: FAIL (ImportError: cannot import name 'LinkRecord').

- [ ] **Step 3: Implement in `src/codelore/models.py`**

Add after `AbstentionReason`:

```python
class RelationType(StrEnum):
    NATIVE_TO_WINDOW = "native_to_window"
    LINKED_TO_WINDOW = "linked_to_window"
    PARENT_OF = "parent_of"
    INCLUDES_DIFF = "includes_diff"


class LinkMethod(StrEnum):
    EXPLICIT = "explicit"
    STRUCTURAL = "structural"
    HEURISTIC = "heuristic"
    INFERRED = "inferred"


class MembershipType(StrEnum):
    NATIVE = "native"
    LINKED = "linked"
    INFERRED = "inferred"


class LinkRecord(CodeLoreModel):
    link_id: str
    window_id: str
    relation_type: RelationType
    source_id: str
    target_id: str
    link_method: LinkMethod
    confidence: Confidence | None = None
    membership_type: MembershipType | None = None
    evidence_ids: tuple[str, ...] = Field(default_factory=tuple)
```

In `Warrant`, delete the `claim_id: str` line. In `EvidencePack`, add:

```python
    pack_schema_version: str = "1"
    links: tuple[LinkRecord, ...] = Field(default_factory=tuple)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest -q` — Expected: PASS (all tests, including pre-existing).

- [ ] **Step 5: Commit**

```bash
git add src/codelore/models.py tests/test_models.py
git commit -m "feat: LinkRecord, relation enums, pack schema version; drop Warrant.claim_id"
```

---

### Task 5: ID scheme (`codelore.ids`)

**Files:**
- Create: `src/codelore/ids.py`
- Test: `tests/test_ids.py`
- Modify: `pyproject.toml` (add hypothesis to dev group)

**Interfaces:**
- Produces: `canonical_encode(value: object) -> bytes`; `record_id(prefix: str, fields: dict[str, object]) -> str`.

- [ ] **Step 1: Add Hypothesis**

Run: `uv add --group dev hypothesis` — Expected: resolves and updates `uv.lock`.

- [ ] **Step 2: Write the failing tests**

Create `tests/test_ids.py`:

```python
import unicodedata
from datetime import UTC, datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

from codelore.ids import canonical_encode, record_id

scalars = st.one_of(st.none(), st.booleans(), st.integers(), st.text())
values = st.recursive(
    scalars,
    lambda children: st.one_of(
        st.lists(children, max_size=4),
        st.dictionaries(st.text(min_size=1), children, max_size=4),
    ),
    max_leaves=10,
)


def test_key_order_independence():
    a = canonical_encode({"b": 1, "a": 2})
    b = canonical_encode({"a": 2, "b": 1})
    assert a == b


def test_nfc_normalization():
    composed = "café"
    decomposed = unicodedata.normalize("NFD", composed)
    assert canonical_encode(composed) == canonical_encode(decomposed)


def test_datetime_rfc3339_utc():
    dt = datetime(2024, 1, 1, 12, 0, tzinfo=UTC)
    assert canonical_encode(dt) == b'"2024-01-01T12:00:00Z"'


def test_floats_rejected():
    with pytest.raises(ValueError):
        canonical_encode(1.5)


def test_record_id_shape():
    rid = record_id("art", {"project_id": "p", "artifact_type": "commit",
                            "source_locator": "abc"})
    prefix, digest = rid.split(":")
    assert prefix == "art" and len(digest) == 16


@given(values)
def test_encode_is_deterministic(value):
    assert canonical_encode(value) == canonical_encode(value)


@given(st.dictionaries(st.text(min_size=1), scalars, min_size=1, max_size=5))
def test_record_id_stable_under_key_permutation(fields):
    reordered = dict(reversed(list(fields.items())))
    assert record_id("t", fields) == record_id("t", reordered)
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest tests/test_ids.py -q` — Expected: FAIL (ModuleNotFoundError: codelore.ids).

- [ ] **Step 4: Implement `src/codelore/ids.py`**

```python
"""Content-addressed identifiers per docs/architecture/11-id-and-serialization-spec.md."""

import hashlib
import unicodedata
from datetime import datetime, timezone


def _canonical(value: object) -> object:
    if value is None or isinstance(value, bool | int):
        return value
    if isinstance(value, float):
        raise ValueError("floats are not permitted in canonical encoding")
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError("datetimes must be timezone-aware")
        rendered = value.astimezone(timezone.utc).isoformat()
        return rendered.replace("+00:00", "Z")
    if isinstance(value, dict):
        return {
            _require_str_key(k): _canonical(v)
            for k, v in sorted(value.items())
        }
    if isinstance(value, list | tuple):
        return [_canonical(v) for v in value]
    raise ValueError(f"unsupported type for canonical encoding: {type(value)!r}")


def _require_str_key(key: object) -> str:
    if not isinstance(key, str):
        raise ValueError("canonical dict keys must be strings")
    return unicodedata.normalize("NFC", key)


def canonical_encode(value: object) -> bytes:
    import json

    return json.dumps(
        _canonical(value), ensure_ascii=False, separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def record_id(prefix: str, fields: dict[str, object]) -> str:
    digest = hashlib.sha256(canonical_encode(fields)).hexdigest()[:16]
    return f"{prefix}:{digest}"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_ids.py -q` — Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/codelore/ids.py tests/test_ids.py pyproject.toml uv.lock
git commit -m "feat: content-addressed ID scheme with canonical encoding"
```

---

### Task 6: Canonical pack serializer (`codelore.serialize`)

**Files:**
- Create: `src/codelore/serialize.py`
- Test: `tests/test_serialize.py`

**Interfaces:**
- Consumes: `canonical_encode` semantics from Task 5 (shared `_canonical` rules via `codelore.ids`).
- Produces: `canonical_json_bytes(record: BaseModel) -> bytes`; `write_record(path, record) -> None`; `write_jsonl(path, records, id_field) -> None` (sorted by `id_field`); constant `PACK_SCHEMA_VERSION = "1"`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_serialize.py`:

```python
from codelore.models import LinkMethod, LinkRecord, MembershipType, RelationType
from codelore.serialize import PACK_SCHEMA_VERSION, canonical_json_bytes, write_jsonl


def _link(n: int) -> LinkRecord:
    return LinkRecord(
        link_id=f"lnk:{n:016x}",
        window_id="win:1",
        relation_type=RelationType.NATIVE_TO_WINDOW,
        source_id="win:1",
        target_id=f"art:{n}",
        link_method=LinkMethod.STRUCTURAL,
        membership_type=MembershipType.NATIVE,
    )


def test_schema_version():
    assert PACK_SCHEMA_VERSION == "1"


def test_canonical_json_bytes_sorted_and_compact():
    raw = canonical_json_bytes(_link(1))
    assert raw.startswith(b"{")
    keys = [k.split(b'":')[0] for k in raw[1:].split(b',"')]
    assert keys == sorted(keys)
    assert b": " not in raw


def test_write_jsonl_sorted_by_id_lf_terminated(tmp_path):
    path = tmp_path / "links.jsonl"
    write_jsonl(path, [_link(2), _link(1)], id_field="link_id")
    data = path.read_bytes()
    lines = data.split(b"\n")
    assert data.endswith(b"\n") and b"\r" not in data
    assert b'"lnk:0000000000000001"' in lines[0]
    assert b'"lnk:0000000000000002"' in lines[1]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_serialize.py -q` — Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implement `src/codelore/serialize.py`**

```python
"""Canonical pack serialization per docs/architecture/11-id-and-serialization-spec.md."""

from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

from codelore.ids import canonical_encode

PACK_SCHEMA_VERSION = "1"


def canonical_json_bytes(record: BaseModel) -> bytes:
    return canonical_encode(record.model_dump(mode="python"))


def write_record(path: Path, record: BaseModel) -> None:
    path.write_bytes(canonical_json_bytes(record) + b"\n")


def write_jsonl(path: Path, records: Sequence[BaseModel], id_field: str) -> None:
    ordered = sorted(records, key=lambda r: getattr(r, id_field))
    body = b"".join(canonical_json_bytes(r) + b"\n" for r in ordered)
    path.write_bytes(body)
```

Note: `model_dump(mode="python")` keeps datetimes as datetime objects so `canonical_encode` renders them RFC3339-Z; enums dump to their `str` values via `StrEnum`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_serialize.py -q` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/codelore/serialize.py tests/test_serialize.py
git commit -m "feat: canonical JSON/JSONL pack serializer"
```

---

### Task 7: Deterministic fixture repository

**Files:**
- Create: `tests/conftest.py`

**Interfaces:**
- Produces: pytest fixture `fixture_repo(tmp_path_factory) -> Path` — a git repo with tags `v0.1.0` and `v0.2.0`; the window `v0.1.0..v0.2.0` contains exactly 5 all-ancestry commits (4 first-parent), 1 merge, and touches `src/app.py`, `docs/guide.md`, `tests/test_app.py`, `src/feature.py`.

- [ ] **Step 1: Write the fixture and a self-test**

Create `tests/conftest.py`:

```python
import subprocess
from pathlib import Path

import pytest

_ENV = {
    "GIT_AUTHOR_NAME": "Fixture",
    "GIT_AUTHOR_EMAIL": "fixture@example.com",
    "GIT_COMMITTER_NAME": "Fixture",
    "GIT_COMMITTER_EMAIL": "fixture@example.com",
    "GIT_AUTHOR_DATE": "2024-01-01T00:00:00+00:00",
    "GIT_COMMITTER_DATE": "2024-01-01T00:00:00+00:00",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_SYSTEM": "/dev/null",
}


def _git(repo: Path, *args: str, date: str | None = None) -> str:
    env = dict(_ENV)
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    out = subprocess.run(
        ["git", "-C", str(repo), *args],
        env=env, check=True, capture_output=True, text=True,
    )
    return out.stdout.strip()


def _commit(repo: Path, path: str, content: str, message: str, date: str) -> None:
    file = repo / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", message, date=date)


@pytest.fixture(scope="session")
def fixture_repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    repo = tmp_path_factory.mktemp("fixture-repo")
    _git(repo, "init", "-b", "main")
    _commit(repo, "README.md", "hello\n", "initial", "2024-01-01T00:00:00+00:00")
    _git(repo, "tag", "v0.1.0")
    _commit(repo, "src/app.py", "APP = 1\n", "add app", "2024-01-02T00:00:00+00:00")
    _commit(repo, "docs/guide.md", "guide\n", "add guide", "2024-01-03T00:00:00+00:00")
    _commit(repo, "tests/test_app.py", "def test_app():\n    assert True\n",
            "add app test", "2024-01-04T00:00:00+00:00")
    _git(repo, "checkout", "-b", "feature")
    _commit(repo, "src/feature.py", "FEATURE = 1\n", "add feature",
            "2024-01-05T00:00:00+00:00")
    _git(repo, "checkout", "main")
    _git(repo, "merge", "--no-ff", "-m", "merge feature", "feature",
         date="2024-01-06T00:00:00+00:00")
    _git(repo, "tag", "v0.2.0")
    return repo
```

Create the self-test in `tests/test_fixture_repo.py`:

```python
import subprocess
from pathlib import Path


def _count(repo: Path, *args: str) -> int:
    out = subprocess.run(["git", "-C", str(repo), "rev-list", "--count", *args],
                         check=True, capture_output=True, text=True)
    return int(out.stdout)


def test_fixture_window_shape(fixture_repo):
    assert _count(fixture_repo, "v0.2.0", "^v0.1.0") == 5
    assert _count(fixture_repo, "--first-parent", "v0.2.0", "^v0.1.0") == 4
    assert _count(fixture_repo, "--merges", "v0.2.0", "^v0.1.0") == 1
```

- [ ] **Step 2: Run the self-test**

Run: `uv run pytest tests/test_fixture_repo.py -q` — Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/conftest.py tests/test_fixture_repo.py
git commit -m "test: deterministic fixture repository with merge topology"
```

---

### Task 8: Git ingestion (`codelore.ingest.git`)

**Files:**
- Create: `src/codelore/ingest/git.py`
- Test: `tests/test_ingest_git.py`

**Interfaces:**
- Produces:
  - `resolve_ref(repo: Path, ref: str) -> str` (full SHA; raises `ValueError` on unknown ref)
  - `CommitInfo` (frozen dataclass): `sha: str, parents: tuple[str, ...], author_date: str, committer_date: str, message: str, first_parent: bool` (dates RFC3339 UTC `Z`)
  - `list_window_commits(repo: Path, start_sha: str, end_sha: str) -> tuple[CommitInfo, ...]` (all-ancestry, oldest first, `first_parent` annotated)
  - `FileChange` (frozen dataclass): `path: str, change_kind: str` (`added|modified|deleted|renamed`), `additions: int | None, deletions: int | None`
  - `commit_file_changes(repo: Path, sha: str) -> tuple[FileChange, ...]`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_ingest_git.py`:

```python
import pytest

from codelore.ingest.git import (
    commit_file_changes, list_window_commits, resolve_ref,
)


def test_resolve_ref_returns_full_sha(fixture_repo):
    sha = resolve_ref(fixture_repo, "v0.1.0")
    assert len(sha) == 40


def test_resolve_ref_rejects_unknown(fixture_repo):
    with pytest.raises(ValueError):
        resolve_ref(fixture_repo, "no-such-ref")


def test_window_commits_all_ancestry_with_first_parent_annotation(fixture_repo):
    start = resolve_ref(fixture_repo, "v0.1.0")
    end = resolve_ref(fixture_repo, "v0.2.0")
    commits = list_window_commits(fixture_repo, start, end)
    assert len(commits) == 5
    assert sum(c.first_parent for c in commits) == 4
    assert commits[0].message.startswith("add app")          # oldest first
    assert all(c.committer_date.endswith("Z") for c in commits)
    merge = [c for c in commits if len(c.parents) == 2]
    assert len(merge) == 1


def test_commit_file_changes(fixture_repo):
    start = resolve_ref(fixture_repo, "v0.1.0")
    end = resolve_ref(fixture_repo, "v0.2.0")
    commits = list_window_commits(fixture_repo, start, end)
    app = next(c for c in commits if c.message == "add app")
    changes = commit_file_changes(fixture_repo, app.sha)
    assert [c.path for c in changes] == ["src/app.py"]
    assert changes[0].change_kind == "added"
    assert changes[0].additions == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_ingest_git.py -q` — Expected: FAIL (ImportError).

- [ ] **Step 3: Implement `src/codelore/ingest/git.py`**

```python
"""Git-first acquisition. Plain subprocess per the tooling decision in
docs/architecture/11-id-and-serialization-spec.md."""

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

_KIND = {"A": "added", "M": "modified", "D": "deleted", "R": "renamed"}


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise ValueError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def _to_utc_z(iso: str) -> str:
    parsed = datetime.fromisoformat(iso)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def resolve_ref(repo: Path, ref: str) -> str:
    return _git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()


@dataclass(frozen=True)
class CommitInfo:
    sha: str
    parents: tuple[str, ...]
    author_date: str
    committer_date: str
    message: str
    first_parent: bool


def list_window_commits(
    repo: Path, start_sha: str, end_sha: str
) -> tuple[CommitInfo, ...]:
    shas = _git(repo, "rev-list", "--reverse", end_sha, f"^{start_sha}").split()
    first_parent = set(
        _git(repo, "rev-list", "--first-parent", end_sha, f"^{start_sha}").split()
    )
    commits = []
    for sha in shas:
        raw = _git(
            repo, "show", "-s",
            "--format=%H%x1f%P%x1f%aI%x1f%cI%x1f%s", sha,
        ).strip()
        _, parents, a_date, c_date, subject = raw.split("\x1f")
        commits.append(
            CommitInfo(
                sha=sha,
                parents=tuple(parents.split()) if parents else (),
                author_date=_to_utc_z(a_date),
                committer_date=_to_utc_z(c_date),
                message=subject,
                first_parent=sha in first_parent,
            )
        )
    return tuple(commits)


@dataclass(frozen=True)
class FileChange:
    path: str
    change_kind: str
    additions: int | None
    deletions: int | None


def commit_file_changes(repo: Path, sha: str) -> tuple[FileChange, ...]:
    status_raw = _git(
        repo, "show", "--format=", "--name-status", "--no-renames", "-m",
        "--first-parent", sha,
    )
    numstat_raw = _git(
        repo, "show", "--format=", "--numstat", "--no-renames", "-m",
        "--first-parent", sha,
    )
    counts: dict[str, tuple[int | None, int | None]] = {}
    for line in numstat_raw.splitlines():
        if not line.strip():
            continue
        added, deleted, path = line.split("\t")
        counts[path] = (
            None if added == "-" else int(added),
            None if deleted == "-" else int(deleted),
        )
    changes = []
    for line in status_raw.splitlines():
        if not line.strip():
            continue
        status, path = line.split("\t", 1)
        additions, deletions = counts.get(path, (None, None))
        changes.append(
            FileChange(
                path=path,
                change_kind=_KIND.get(status[0], "modified"),
                additions=additions,
                deletions=deletions,
            )
        )
    return tuple(sorted(changes, key=lambda c: c.path))
```

Also create `src/codelore/ingest/__init__.py` content unchanged (already exists).

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_ingest_git.py -q` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/codelore/ingest/git.py tests/test_ingest_git.py
git commit -m "feat: git-first acquisition with first-parent annotation"
```

---

### Task 9: Window builder and normalization

**Files:**
- Create: `src/codelore/windows/builder.py`, `src/codelore/artifacts/normalize.py`
- Test: `tests/test_normalize.py`

**Interfaces:**
- Consumes: `CommitInfo`, `FileChange` (Task 8); `record_id` (Task 5); models (Task 4).
- Produces:
  - `build_change_window(project_id: str, window_type: WindowType, start_sha: str, end_sha: str, label: str) -> ChangeWindow` (window_id content-addressed; no tag/release names accepted — SHAs only)
  - `NormalizedWindow` (frozen pydantic model): `artifacts: tuple[ArtifactRecord, ...], links: tuple[LinkRecord, ...]`
  - `normalize_window(project: Project, window: ChangeWindow, commits: tuple[CommitInfo, ...], changes_by_sha: dict[str, tuple[FileChange, ...]]) -> NormalizedWindow`
  - `classify_path(path: str) -> ArtifactType` (docs/`.md` -> DOC_CHANGE, tests -> TEST_CHANGE, else DIFF)

- [ ] **Step 1: Write the failing tests**

Create `tests/test_normalize.py`:

```python
from codelore.artifacts.normalize import classify_path, normalize_window
from codelore.ingest.git import commit_file_changes, list_window_commits, resolve_ref
from codelore.models import ArtifactType, Project, RelationType, WindowType
from codelore.windows.builder import build_change_window


def _normalized(fixture_repo):
    start = resolve_ref(fixture_repo, "v0.1.0")
    end = resolve_ref(fixture_repo, "v0.2.0")
    window = build_change_window("fixture", WindowType.RELEASE, start, end,
                                 "v0.1.0..v0.2.0")
    commits = list_window_commits(fixture_repo, start, end)
    changes = {c.sha: commit_file_changes(fixture_repo, c.sha) for c in commits}
    project = Project(project_id="fixture", name="fixture")
    return window, normalize_window(project, window, commits, changes)


def test_classify_path():
    assert classify_path("docs/guide.md") == ArtifactType.DOC_CHANGE
    assert classify_path("tests/test_app.py") == ArtifactType.TEST_CHANGE
    assert classify_path("src/app.py") == ArtifactType.DIFF


def test_window_id_is_content_addressed(fixture_repo):
    window, _ = _normalized(fixture_repo)
    assert window.window_id.startswith("win:")
    assert window.window_type == WindowType.RELEASE


def test_artifact_and_link_counts(fixture_repo):
    _, normalized = _normalized(fixture_repo)
    commits = [a for a in normalized.artifacts
               if a.artifact_type == ArtifactType.COMMIT]
    assert len(commits) == 5
    diff_like = [a for a in normalized.artifacts
                 if a.artifact_type in (ArtifactType.DIFF,
                                        ArtifactType.DOC_CHANGE,
                                        ArtifactType.TEST_CHANGE)]
    # 4 non-merge commits x 1 file each, plus the merge commit's first-parent
    # diff (src/feature.py arriving on main) = 5
    assert len(diff_like) == 5
    membership = [link for link in normalized.links
                  if link.relation_type == RelationType.NATIVE_TO_WINDOW]
    assert len(membership) == len(normalized.artifacts)
    parents = [link for link in normalized.links
               if link.relation_type == RelationType.PARENT_OF]
    assert len(parents) == 5  # in-window parent edges incl. both merge parents


def test_replay_produces_identical_ids(fixture_repo):
    _, first = _normalized(fixture_repo)
    _, second = _normalized(fixture_repo)
    assert [a.artifact_record_id for a in first.artifacts] == \
           [a.artifact_record_id for a in second.artifacts]
    assert [link.link_id for link in first.links] == \
           [link.link_id for link in second.links]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_normalize.py -q` — Expected: FAIL (ImportError).

- [ ] **Step 3: Implement `src/codelore/windows/builder.py`**

```python
"""Core window assembly. Operates on resolved SHAs only; release/tag
resolution happens at the CLI edge."""

from codelore.ids import record_id
from codelore.models import ChangeWindow, WindowType


def build_change_window(
    project_id: str,
    window_type: WindowType,
    start_sha: str,
    end_sha: str,
    label: str,
) -> ChangeWindow:
    window_id = record_id(
        "win",
        {
            "project_id": project_id,
            "window_type": str(window_type),
            "start_sha": start_sha,
            "end_sha": end_sha,
        },
    )
    return ChangeWindow(
        window_id=window_id,
        window_type=window_type,
        label=label,
        project_id=project_id,
        start_ref=start_sha,
        end_ref=end_sha,
    )
```

- [ ] **Step 4: Implement `src/codelore/artifacts/normalize.py`**

```python
"""Normalize stage: source objects -> ArtifactRecord + LinkRecord."""

from datetime import datetime

from pydantic import Field

from codelore.ids import record_id
from codelore.ingest.git import CommitInfo, FileChange
from codelore.models import (
    ArtifactRecord, ArtifactType, ChangeWindow, CodeLoreModel, LinkMethod,
    LinkRecord, LocatorType, MembershipType, Project, RelationType,
)

_NORMALIZER = "codelore-normalize/1"


class NormalizedWindow(CodeLoreModel):
    artifacts: tuple[ArtifactRecord, ...] = Field(default_factory=tuple)
    links: tuple[LinkRecord, ...] = Field(default_factory=tuple)


def classify_path(path: str) -> ArtifactType:
    if path.startswith("docs/") or path.endswith(".md"):
        return ArtifactType.DOC_CHANGE
    parts = path.split("/")
    if parts[0] in ("test", "tests") or parts[-1].startswith("test_"):
        return ArtifactType.TEST_CHANGE
    return ArtifactType.DIFF


def _artifact_id(project_id: str, artifact_type: ArtifactType, locator: str) -> str:
    return record_id(
        "art",
        {
            "project_id": project_id,
            "artifact_type": str(artifact_type),
            "source_locator": locator,
        },
    )


def _link(window_id: str, relation: RelationType, source: str, target: str,
          membership: MembershipType | None = None) -> LinkRecord:
    link_id = record_id(
        "lnk",
        {
            "window_id": window_id,
            "relation_type": str(relation),
            "source_id": source,
            "target_id": target,
        },
    )
    return LinkRecord(
        link_id=link_id,
        window_id=window_id,
        relation_type=relation,
        source_id=source,
        target_id=target,
        link_method=LinkMethod.STRUCTURAL,
        membership_type=membership,
    )


def normalize_window(
    project: Project,
    window: ChangeWindow,
    commits: tuple[CommitInfo, ...],
    changes_by_sha: dict[str, tuple[FileChange, ...]],
) -> NormalizedWindow:
    artifacts: list[ArtifactRecord] = []
    links: list[LinkRecord] = []
    commit_art_ids: dict[str, str] = {}

    for commit in commits:
        art_id = _artifact_id(project.project_id, ArtifactType.COMMIT, commit.sha)
        commit_art_ids[commit.sha] = art_id
        artifacts.append(
            ArtifactRecord(
                artifact_record_id=art_id,
                artifact_type=ArtifactType.COMMIT,
                locator_type=LocatorType.GIT_COMMIT,
                source_locator=commit.sha,
                window_ids=(window.window_id,),
                source_system="git",
                captured_at=datetime.fromisoformat(commit.committer_date),
                normalized_by=_NORMALIZER,
                metadata={
                    "message": commit.message,
                    "first_parent": commit.first_parent,
                    "author_date": commit.author_date,
                    "parent_count": len(commit.parents),
                },
            )
        )

    for commit in commits:
        commit_art = commit_art_ids[commit.sha]
        links.append(_link(window.window_id, RelationType.NATIVE_TO_WINDOW,
                           window.window_id, commit_art, MembershipType.NATIVE))
        for parent in commit.parents:
            if parent in commit_art_ids:
                links.append(_link(window.window_id, RelationType.PARENT_OF,
                                   commit_art_ids[parent], commit_art))
        for change in changes_by_sha.get(commit.sha, ()):
            locator = f"{commit.sha}:{change.path}"
            diff_type = classify_path(change.path)
            diff_id = _artifact_id(project.project_id, diff_type, locator)
            artifacts.append(
                ArtifactRecord(
                    artifact_record_id=diff_id,
                    artifact_type=diff_type,
                    locator_type=LocatorType.FILE_PATH,
                    source_locator=locator,
                    window_ids=(window.window_id,),
                    source_system="git",
                    captured_at=datetime.fromisoformat(commit.committer_date),
                    normalized_by=_NORMALIZER,
                    metadata={
                        "path": change.path,
                        "change_kind": change.change_kind,
                        "additions": change.additions,
                        "deletions": change.deletions,
                    },
                )
            )
            links.append(_link(window.window_id, RelationType.NATIVE_TO_WINDOW,
                               window.window_id, diff_id, MembershipType.NATIVE))
            links.append(_link(window.window_id, RelationType.INCLUDES_DIFF,
                               commit_art, diff_id))

    return NormalizedWindow(artifacts=tuple(artifacts), links=tuple(links))
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_normalize.py -q` — Expected: PASS. (If the parent-edge count differs, check the merge commit's two in-window parents; the fixture yields 5 in-window parent pairs: app->guide, guide->test, test->feature, test->merge, feature->merge.)

- [ ] **Step 6: Commit**

```bash
git add src/codelore/windows/builder.py src/codelore/artifacts/normalize.py tests/test_normalize.py
git commit -m "feat: window builder and normalize stage emitting artifacts and links"
```

---

### Task 10: Run manifest and pack assembly

**Files:**
- Create: `src/codelore/pipeline.py`
- Test: `tests/test_pipeline.py`

**Interfaces:**
- Consumes: everything above.
- Produces:
  - `StageRecord` (pydantic, not frozen-compared): `name: str, input_count: int, output_count: int, drops: tuple[str, ...] = ()`
  - `RunManifest`: `run_id: str, code_version: str, invocation: str, started_at: datetime, completed_at: datetime | None, pack_schema_version: str, window_policy: dict[str, str], stages: tuple[StageRecord, ...]`
  - `build_pack(repo: Path, start_sha: str, end_sha: str, project: Project, label: str, out_dir: Path, invocation: str) -> RunManifest` — runs acquire -> window -> normalize -> assemble, writes the canonical pack directory.
  - `STABLE_MANIFEST_FIELDS = ("pack_schema_version", "window_policy", "stages")` for determinism comparison.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_pipeline.py`:

```python
import json

from codelore.ingest.git import resolve_ref
from codelore.models import Project
from codelore.pipeline import build_pack


def _build(fixture_repo, tmp_path, name="pack"):
    project = Project(project_id="fixture", name="fixture")
    out = tmp_path / name
    manifest = build_pack(
        repo=fixture_repo,
        start_sha=resolve_ref(fixture_repo, "v0.1.0"),
        end_sha=resolve_ref(fixture_repo, "v0.2.0"),
        project=project,
        label="v0.1.0..v0.2.0",
        out_dir=out,
        invocation="test",
    )
    return out, manifest


def test_pack_layout(fixture_repo, tmp_path):
    out, _ = _build(fixture_repo, tmp_path)
    names = sorted(p.name for p in out.iterdir())
    assert names == ["artifacts.jsonl", "links.jsonl", "manifest.json",
                     "project.json", "window.json"]


def test_manifest_counts_account_for_all_records(fixture_repo, tmp_path):
    out, manifest = _build(fixture_repo, tmp_path)
    stages = {s.name: s for s in manifest.stages}
    artifacts = len((out / "artifacts.jsonl").read_bytes().splitlines())
    links = len((out / "links.jsonl").read_bytes().splitlines())
    assert stages["acquire"].output_count == 5           # commits
    assert stages["normalize"].output_count == artifacts + links
    assert all(s.drops == () for s in manifest.stages)   # nothing dropped
    assert manifest.pack_schema_version == "1"
    assert manifest.window_policy["traversal"] == "all_ancestry_first_parent_annotated"


def test_window_json_is_canonical(fixture_repo, tmp_path):
    out, _ = _build(fixture_repo, tmp_path)
    raw = (out / "window.json").read_bytes()
    parsed = json.loads(raw)
    assert parsed["window_type"] == "release"
    assert raw.endswith(b"\n")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_pipeline.py -q` — Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implement `src/codelore/pipeline.py`**

```python
"""Phase 2 pipeline: acquire -> window -> normalize -> assemble."""

import subprocess
import uuid
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from codelore import __version__
from codelore.artifacts.normalize import normalize_window
from codelore.ingest.git import commit_file_changes, list_window_commits
from codelore.models import Project, WindowType
from codelore.serialize import PACK_SCHEMA_VERSION, write_jsonl, write_record
from codelore.windows.builder import build_change_window

STABLE_MANIFEST_FIELDS = ("pack_schema_version", "window_policy", "stages")

_WINDOW_POLICY = {
    "reachability": "end ^start",
    "traversal": "all_ancestry_first_parent_annotated",
    "timestamp_authority": "committer_date_utc",
}


class StageRecord(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    input_count: int
    output_count: int
    drops: tuple[str, ...] = Field(default_factory=tuple)


class RunManifest(BaseModel):
    model_config = ConfigDict(frozen=True)
    run_id: str
    code_version: str
    invocation: str
    started_at: datetime
    completed_at: datetime | None
    pack_schema_version: str
    window_policy: dict[str, str]
    stages: tuple[StageRecord, ...]


def _code_version() -> str:
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
            cwd=Path(__file__).resolve().parent,
        ).stdout.strip()
        return f"{__version__}+{sha}"
    except (subprocess.CalledProcessError, OSError):
        return __version__


def build_pack(
    *,
    repo: Path,
    start_sha: str,
    end_sha: str,
    project: Project,
    label: str,
    out_dir: Path,
    invocation: str,
) -> RunManifest:
    started = datetime.now(UTC)
    stages: list[StageRecord] = []

    commits = list_window_commits(repo, start_sha, end_sha)
    stages.append(StageRecord(name="acquire", input_count=2,
                              output_count=len(commits)))

    window = build_change_window(
        project.project_id, WindowType.RELEASE, start_sha, end_sha, label
    )
    stages.append(StageRecord(name="window", input_count=len(commits),
                              output_count=1))

    changes = {c.sha: commit_file_changes(repo, c.sha) for c in commits}
    normalized = normalize_window(project, window, commits, changes)
    stages.append(
        StageRecord(
            name="normalize",
            input_count=len(commits) + sum(len(v) for v in changes.values()),
            output_count=len(normalized.artifacts) + len(normalized.links),
        )
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    write_record(out_dir / "project.json", project)
    write_record(out_dir / "window.json", window)
    write_jsonl(out_dir / "artifacts.jsonl", normalized.artifacts,
                id_field="artifact_record_id")
    write_jsonl(out_dir / "links.jsonl", normalized.links, id_field="link_id")
    stages.append(
        StageRecord(
            name="assemble",
            input_count=len(normalized.artifacts) + len(normalized.links),
            output_count=len(normalized.artifacts) + len(normalized.links),
        )
    )

    manifest = RunManifest(
        run_id=str(uuid.uuid4()),
        code_version=_code_version(),
        invocation=invocation,
        started_at=started,
        completed_at=datetime.now(UTC),
        pack_schema_version=PACK_SCHEMA_VERSION,
        window_policy=_WINDOW_POLICY,
        stages=tuple(stages),
    )
    write_record(out_dir / "manifest.json", manifest)
    return manifest
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_pipeline.py -q` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/codelore/pipeline.py tests/test_pipeline.py
git commit -m "feat: run manifest and canonical pack assembly"
```

---

### Task 11: CLI wiring

**Files:**
- Modify: `src/codelore/cli.py` (replace the `build_window` stub body)
- Modify: `.gitignore` (ignore local pack output)
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `resolve_ref`, `build_pack`, `Project`.
- Produces: working `codelore build-window --repo R --start-ref A --end-ref B --project-id P [--output DIR]`; tag/release resolution happens here and only here.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_cli.py`:

```python
from typer.testing import CliRunner

from codelore.cli import app


def test_build_window_end_to_end(fixture_repo, tmp_path):
    out = tmp_path / "pack"
    result = CliRunner().invoke(app, [
        "build-window",
        "--repo", str(fixture_repo),
        "--start-ref", "v0.1.0",
        "--end-ref", "v0.2.0",
        "--project-id", "fixture",
        "--output", str(out),
    ])
    assert result.exit_code == 0, result.output
    assert (out / "artifacts.jsonl").exists()
    assert "commits=5" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli.py -q` — Expected: FAIL (the stub prints scaffolding text; no pack is written).

- [ ] **Step 3: Replace the `build_window` command body in `src/codelore/cli.py`**

Add the `--project-id` option and replace the body:

```python
@app.command("build-window")
def build_window(
    repo: Annotated[
        Path,
        typer.Option("--repo", exists=True, file_okay=False, dir_okay=True,
                     readable=True, resolve_path=True,
                     help="Local repository to ingest."),
    ],
    start_ref: Annotated[str, typer.Option("--start-ref", help="Window start ref.")],
    end_ref: Annotated[str, typer.Option("--end-ref", help="Window end ref.")],
    project_id: Annotated[str, typer.Option("--project-id", help="Project slug.")],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Evidence-pack output directory."),
    ] = Path("evidence-pack"),
) -> None:
    """Build a release-window evidence pack (Phase 2: artifacts and links)."""
    from codelore.ingest.git import resolve_ref
    from codelore.models import Project
    from codelore.pipeline import build_pack

    start_sha = resolve_ref(repo, start_ref)   # release semantics end here
    end_sha = resolve_ref(repo, end_ref)
    project = Project(project_id=project_id, name=project_id)
    manifest = build_pack(
        repo=repo, start_sha=start_sha, end_sha=end_sha, project=project,
        label=f"{start_ref}..{end_ref}", out_dir=output,
        invocation=f"build-window {start_ref}..{end_ref}",
    )
    stages = {s.name: s for s in manifest.stages}
    console.print(
        f"pack={output} commits={stages['acquire'].output_count} "
        f"records={stages['assemble'].output_count}"
    )
```

Append to `.gitignore`:

```text
evidence-pack/
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest -q` — Expected: PASS (full suite). If a pre-existing test in `tests/test_cli.py` asserts the old scaffold output ("build-window is scaffolded..."), update that assertion to the new output contract (`pack=... commits=... records=...`) — the scaffold text is gone by design.

- [ ] **Step 5: Commit**

```bash
git add src/codelore/cli.py tests/test_cli.py .gitignore
git commit -m "feat: wire build-window CLI to the Phase 2 pipeline"
```

---

### Task 12: Determinism gate and CI

**Files:**
- Create: `tests/test_determinism.py`, `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `build_pack`, `STABLE_MANIFEST_FIELDS`.
- Produces: the Phase 2 exit-criterion check (byte-identical packs) and the CI pipeline.

- [ ] **Step 1: Write the determinism test**

Create `tests/test_determinism.py`:

```python
import json

from codelore.ingest.git import resolve_ref
from codelore.models import Project
from codelore.pipeline import STABLE_MANIFEST_FIELDS, build_pack


def test_double_build_is_byte_identical(fixture_repo, tmp_path):
    packs = []
    for name in ("one", "two"):
        out = tmp_path / name
        build_pack(
            repo=fixture_repo,
            start_sha=resolve_ref(fixture_repo, "v0.1.0"),
            end_sha=resolve_ref(fixture_repo, "v0.2.0"),
            project=Project(project_id="fixture", name="fixture"),
            label="v0.1.0..v0.2.0",
            out_dir=out,
            invocation="determinism-test",
        )
        packs.append(out)

    for filename in ("project.json", "window.json", "artifacts.jsonl",
                     "links.jsonl"):
        assert (packs[0] / filename).read_bytes() == \
               (packs[1] / filename).read_bytes(), filename

    manifests = [json.loads((p / "manifest.json").read_text()) for p in packs]
    for field in STABLE_MANIFEST_FIELDS:
        assert manifests[0][field] == manifests[1][field], field
```

- [ ] **Step 2: Run test to verify it passes**

Run: `uv run pytest tests/test_determinism.py -q` — Expected: PASS. If it fails, the diff of the two files names the leak; fix the serializer or ID inputs, never the test.

- [ ] **Step 3: Create `.github/workflows/ci.yml`**

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        pythonhashseed: ["0", "424242"]
    env:
      PYTHONHASHSEED: ${{ matrix.pythonhashseed }}
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --group dev
      - run: uv run ruff check .
      - run: uv run pytest -q
```

- [ ] **Step 4: Run the full suite locally under both seeds**

Run: `PYTHONHASHSEED=0 uv run pytest -q && PYTHONHASHSEED=424242 uv run pytest -q`
Expected: PASS twice.

- [ ] **Step 5: Commit**

```bash
git add tests/test_determinism.py .github/workflows/ci.yml
git commit -m "test: byte-identical double-build gate and CI under varied hash seeds"
```

---

### Task 13: Gastown integration and exit-criteria verification

**Files:**
- Modify: `docs/validation/08-gastown-corpus-audit.md` (Verification Record section)

**Interfaces:**
- Consumes: the audit memo counts (Task 1) and the CLI (Task 11).

- [ ] **Step 1: Build the real window**

```bash
uv run codelore build-window \
  --repo /home/kimberly/repos/gastown \
  --start-ref v1.1.0 --end-ref v1.2.0 \
  --project-id gastown \
  --output /tmp/gastown-pack
```

Expected: `commits=<N>` where N equals the audit memo's all-ancestry count.

- [ ] **Step 2: Verify counts against the audit**

```bash
wc -l /tmp/gastown-pack/artifacts.jsonl /tmp/gastown-pack/links.jsonl
```

Compare commit-artifact count and changed-file-artifact counts to the memo. Any mismatch is investigated before proceeding — the memo's counts were produced independently, so a mismatch means an ingester bug or a policy ambiguity, not a memo update.

- [ ] **Step 3: Rebuild and byte-compare (real-corpus determinism)**

```bash
uv run codelore build-window --repo /home/kimberly/repos/gastown \
  --start-ref v1.1.0 --end-ref v1.2.0 --project-id gastown \
  --output /tmp/gastown-pack-2
cmp /tmp/gastown-pack/artifacts.jsonl /tmp/gastown-pack-2/artifacts.jsonl && echo IDENTICAL
cmp /tmp/gastown-pack/links.jsonl /tmp/gastown-pack-2/links.jsonl && echo IDENTICAL
```

Expected: `IDENTICAL` twice.

- [ ] **Step 4: Record the verification and commit**

Check the box in the audit memo's Verification Record with the observed counts, then:

```bash
git add docs/validation/08-gastown-corpus-audit.md
git commit -m "docs: record Phase 2 exit verification against gastown window"
git push
```

---

## Phase 2 exit criteria coverage

- Corpus audit and golden set exist, hand-verified — Tasks 1–2.
- `build-window` counts match the audit — Task 13.
- Byte-identical packs on rebuild, CI-verified — Tasks 12–13.
- Fixture-repo ingestion tests pass — Tasks 7–11.
- Release logic only at the CLI edge — Task 9 builder takes SHAs only; Task 11 resolves refs.
