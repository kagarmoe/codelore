# CodeLore Setup Runbook

## Purpose

This runbook is the starting point for setting up CodeLore development on the
current machine.

It covers:

- awareness of current host hardware and toolchain
- GPU and CUDA verification
- Python environment setup
- initial repo scaffold expectations
- graph database setup
- Headroom installation and repo awareness
- source repos that should be treated as first-class development corpora
- the boundary between sandbox-safe work and host-level work

This document is intentionally practical. It is for getting a new agent or
human operator into a working development state with the least ambiguity.

## Development posture

CodeLore should be developed with a **GPU-aware, host-first stance**.

That does not mean every task needs the GPU. It means:

- the machine has meaningful local acceleration available
- local model, embedding, and batch extraction workflows should be designed to
  take advantage of it
- GPU-dependent checks should be verified from the host shell, not inferred from
  sandboxed agent output

## Current host snapshot

These values reflect the current machine at the time this runbook was written.

### OS and core hardware

- OS: Ubuntu 24.04 on Linux `6.17.0-35-generic`
- CPU: AMD Ryzen 7 7700X, 8 cores / 16 threads
- RAM: 61 GiB total
- Disk: ~1.1 TiB free on `/`

### GPU and CUDA

Authoritative host-shell GPU report provided by Kimberly:

- GPU: NVIDIA GeForce RTX 3090
- VRAM: 24 GiB
- Driver version: `580.159.03`
- Reported CUDA version from `nvidia-smi`: `13.0`

Agent-observed CUDA compiler state from the execution environment:

- `nvcc` present
- `nvcc --version` reported CUDA toolkit `12.0`

This means the environment should be treated as:

- host GPU available and healthy
- at least one CUDA toolkit installed locally
- possible version skew between host driver reporting and toolkit versioning
- sandboxed `nvidia-smi` checks are not authoritative

### Python and core tooling

Current host/tooling state already observed:

- Python: `3.13.13`
- `uv`: `0.11.26`
- Docker: `29.4.1`
- Docker Compose: `v5.1.0`
- Git: `2.43.0`
- Node: `v24.14.1`
- GitHub CLI: `2.45.0`
- Graphify: `0.9.5`

## Source repos that matter

CodeLore development should stay aware of these repos:

- `/home/kimberly/repos/codelore`
- `/home/kimberly/repos/gt-wiki`
- `/home/kimberly/repos/gastown`
- `/home/kimberly/repos/llama.cpp`

Roles:

- `codelore`: product and implementation repo
- `gt-wiki`: extraction lineage and process prototype
- `gastown`: first favorable implementation/evaluation corpus
- `llama.cpp`: post-MVP hostile validation corpus

## First environment checks

Run these from a **normal host shell**, not from a sandboxed agent environment,
when verifying machine capability.

### GPU checks

```bash
nvidia-smi
nvcc --version
```

If PyTorch or another CUDA framework is installed later, also verify from the
project environment:

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-gpu')"
```

### Core tool checks

```bash
python3 --version
uv --version
docker --version
docker compose version
git --version
gh --version
graphify --version
```

## Sandbox boundary

Sandboxed agent command output is acceptable for:

- reading and editing repo files
- normal Python scaffolding
- non-GPU CLI work
- graph/model/doc planning
- most git operations

Sandboxed agent command output is **not authoritative** for:

- GPU visibility
- CUDA driver health
- host-device access
- inference performance
- local GPU benchmarking
- any workflow that needs real device access

For GPU-dependent tasks, use host-level commands or unsandboxed execution.

## Python environment setup

CodeLore should use `uv` from the beginning.

Recommended initial pattern:

```bash
cd /home/kimberly/repos/codelore
uv python pin 3.13
uv venv
source .venv/bin/activate
```

Recommended initial dependency posture:

- keep the base environment lean
- add libraries only when they are needed for a concrete phase
- separate core runtime, dev tooling, and optional GPU/model dependencies

Likely early dependency buckets:

### Core

- `pydantic`
- `typer` or `click`
- `rich`
- `orjson`
- `networkx` only if needed for local graph experiments
- Neo4j client library if Neo4j is selected immediately

### Dev and quality

- `pytest`
- `ruff`
- `mypy` if useful

### Later GPU/model stack

Choose based on actual inference plan, but likely candidates are:

- `torch` with CUDA support
- embedding/model libraries as needed
- local inference adapters only after the first ingestion/evidence pipeline is
  clear

Important rule:

Do not install a heavyweight model stack before the first scaffold and schema
work are stable enough to justify it.

## Recommended repo scaffold

The authoritative development plan is
`docs/plans/00b-development-plan-evidence-first.md`; the original
`docs/plans/00-development-plan.md` is historical. The current package layout
is:

- `src/codelore/ingest`
- `src/codelore/windows`
- `src/codelore/artifacts`
- `src/codelore/evidence`
- `src/codelore/claims`
- `src/codelore/graph`
- `src/codelore/query`
- `src/codelore/export`

Recommended near-term root files:

- `pyproject.toml`
- `.python-version` if desired
- `.gitignore`
- `src/codelore/__init__.py`
- `src/codelore/cli.py`
- `tests/`

Recommended CLI direction:

- `codelore build-window`
- `codelore ask`
- `codelore export-evidence-pack`

## Graph database setup

The project direction is service-backed graph storage from day one.

Recommended initial choice:

- Neo4j via Docker Compose

Why:

- easy local startup
- clear property-graph model
- good fit for the current schema direction
- keeps the graph concrete early

Recommended initial setup shape:

```bash
cd /home/kimberly/repos/codelore
mkdir -p infra/neo4j
```

Then add a `compose.yaml` or `docker-compose.yml` with a local Neo4j service.

Suggested initial requirements:

- deterministic container name
- explicit ports
- local volume for persistence
- credentials stored in local env config, not hard-coded in docs forever

Recommended first verification:

```bash
docker compose up -d
```

Then verify the service is reachable before wiring Python code to it.

## Headroom setup

Headroom should be installed as a development aid for codebase understanding
and repo-aware context.

Source:

- `https://github.com/headroomlabs-ai/headroom`

The Headroom README positions it as a coding-memory/context layer with repo
awareness and MCP integration.

### Installation intent

Install Headroom into the host environment in a way that makes it available for
CodeLore development sessions.

Since external tool installation details may evolve, verify the current install
steps against the Headroom repo README at install time.

### CodeLore-specific intent for Headroom

Headroom should be made aware of these repos:

- `~/repos/codelore`
- `~/repos/gastown`
- `~/repos/gt-wiki`
- `~/repos/llama.cpp`

Use those repos for:

- product repo context (`codelore`)
- extraction lineage (`gt-wiki`)
- favorable corpus (`gastown`)
- hostile validation corpus (`llama.cpp`)

### Practical setup goal

After installation, the environment should support:

- Headroom wrapping or indexing the `codelore` repo itself
- Headroom awareness of the other three repos as related context sources
- persistent local context that helps future agent sessions resume faster

Because Headroom’s exact commands may change, the runbook requirement is:

1. verify current README instructions
2. install Headroom using the recommended method
3. configure it against the four relevant repos above
4. verify that it can see those repos cleanly

### Verification checklist for Headroom

After installation/configuration, verify at least:

- Headroom runs from the host shell
- it recognizes `codelore`
- it can be pointed at `gastown`, `gt-wiki`, and `llama.cpp`
- its local state is persistent across sessions

If Headroom supports repo indexing, wrapping, or MCP registration, document the
exact commands actually used in a follow-up update to this runbook.

## Graphify setup and use

Graphify is already installed and available, but it is optional developer
tooling for agent codebase navigation. It is not part of CodeLore's product
architecture, runtime graph, or data model.

Recommended usage in CodeLore:

- use it only when scoped graph retrieval would help answer a codebase question
- do not treat Graphify output as CodeLore product data
- do not require `graphify update .` after every implementation change

Optional update command:

```bash
graphify update .
```

If `graphify-out/graph.json` exists in `codelore`, future codebase questions
may use Graphify retrieval before wide manual browsing.

CodeLore's product graph should be modeled and persisted through the explicit
graph backend, currently planned as Neo4j.

## GPU-first opportunities for CodeLore

Not every stage needs GPU support, but the following should be designed with GPU
availability in mind:

- local embedding generation
- batch extraction over repo artifacts
- local model inference for summarization or evidence extraction
- reranking or semantic clustering
- experimentation against `llama.cpp`

Recommended rule:

- keep the core ingestion and schema path CPU-safe
- make GPU acceleration an explicit enhancement path for the semantic layers
- validate GPU-dependent workflows from the host shell

## Immediate setup sequence

Recommended order for a fresh development session:

1. Verify host GPU state with `nvidia-smi`.
2. Verify CUDA toolchain visibility with `nvcc --version`.
3. Activate or create the `uv` Python environment.
4. Scaffold the Python project in `/home/kimberly/repos/codelore`.
5. Add lint/test tooling.
6. Stand up Neo4j with Docker Compose.
7. Install and configure Headroom.
8. Optionally verify Graphify availability for agent navigation.
9. Begin Phase 1 implementation work.

## Known environment caveats

- Sandboxed agent execution may fail to see the GPU even when the host can.
- Host driver/CUDA reporting and local toolkit versioning may not match exactly.
- GPU-dependent work should be treated as host-validated work.
- Tooling setup instructions for Headroom may change upstream; verify at install time.

## Suggested follow-up docs

After the first actual scaffold/setup pass, add these if useful:

- `docs/runbooks/01-python-scaffold.md`
- `docs/runbooks/02-neo4j-local-dev.md`
- `docs/runbooks/03-headroom-setup.md`
- `docs/runbooks/04-gpu-model-stack.md`

## Definition of done for setup

The setup phase is in good shape when:

- the host GPU is verified from a normal shell
- the Python environment is created and reproducible
- the CodeLore package scaffold exists
- the graph database can start locally
- Headroom is installed and aware of the four relevant repos
- optional agent-navigation tooling is documented clearly
- a new agent can resume from this runbook without guessing
