---
schema_version: 2
freshness_tier: A
automation_tier: auto
upstream:
  type: github_repo
  repo: arturcrmbot/zava-control-plane
  ref: main
  pinned_sha: 63d9a845052e255a8567ad7b880587adbe7a996b
  pinned_commit_message: "docs(skills): align builder contracts"
  license: MIT
  notes: |
    compose-org consumes the code-first vertical build contract, automatic pack
    discovery, and proof contract from this exact control-plane revision.
packages: []
docs_to_revalidate:
  - https://github.com/arturcrmbot/zava-control-plane
  - https://github.com/arturcrmbot/zava-control-plane/blob/main/docs/superpowers/contracts/VERTICAL-BUILD-CONTRACT.md
  - https://github.com/arturcrmbot/zava-control-plane/blob/main/docs/VERTICAL-PROOF.md
known_issues: []
validation:
  requires:
    - github_only
  runnable: true
  script: |
    #!/usr/bin/env bash
    set -euo pipefail

    PINNED_SHA="63d9a845052e255a8567ad7b880587adbe7a996b"
    REPO_URL="https://github.com/arturcrmbot/zava-control-plane"
    WORK=".upstream-pin-smoke/compose-org"

    rm -rf "$WORK"
    mkdir -p "$WORK"
    trap 'rm -rf "$WORK"' EXIT
    git clone --quiet --depth 1 "$REPO_URL" "$WORK/repo"
    actual="$(git -C "$WORK/repo" rev-parse HEAD)"
    test "$actual" = "$PINNED_SHA"
    echo "pinned SHA verified: $PINNED_SHA"

    python3 - "$WORK/repo" <<'PY'
    import pathlib
    import sys

    root = pathlib.Path(sys.argv[1])
    required = (
        "docs/superpowers/contracts/VERTICAL-BUILD-CONTRACT.md",
        "docs/VERTICAL-PROOF.md",
        "api/shared/vertical_loader.py",
        "verticals/telco/manifest.py",
    )
    missing = [path for path in required if not (root / path).exists()]
    if missing:
        raise SystemExit(f"missing current substrate paths: {missing}")

    build = (root / required[0]).read_text(encoding="utf-8")
    proof = (root / required[1]).read_text(encoding="utf-8")
    loader = (root / required[2]).read_text(encoding="utf-8")

    assert "**Contract version:** `1.0.0`" in build
    assert "**Contract version:** `1.0.0`" in proof
    assert "discover_pack_modules" in loader
    assert "PACK_MODULES = discover_pack_modules()" in loader
    PY

    echo "builder contract version verified: 1.0.0"
    echo "proof contract version verified: 1.0.0"
    echo "automatic pack discovery verified"
  expected_output:
    - "pinned SHA verified"
    - "builder contract version verified: 1.0.0"
    - "proof contract version verified: 1.0.0"
    - "automatic pack discovery verified"
  failure_signatures: []
last_validated: 2026-07-28
validated_by: copilot
known_issues_count: 0
---

# Upstream pin - `compose-org`

This is the machine-readable validation contract for the control-plane
revision consumed by `compose-org`.

## Pin

The YAML frontmatter is the single source of truth for the commit SHA and
subject. It pins the published control-plane revision that introduced:

- `docs/superpowers/contracts/VERTICAL-BUILD-CONTRACT.md`;
- `docs/VERTICAL-PROOF.md` contract version `1.0.0`;
- automatic discovery in `api/shared/vertical_loader.py`;
- pack composition through `verticals/<slug>/manifest.py`.

## Validation

Run the `validation.script` from the repository root. It clones the published
revision and verifies the current build contract, proof contract, pack loader,
and representative Telco manifest.

## Refresh procedure

1. Read the new published `main` SHA and commit subject.
2. Update both pinned SHA occurrences in frontmatter.
3. Run the validation script.
4. Update `last_validated` and `validated_by`.
5. Bump the consuming skill version when behavior changes.

Never pin an unpushed local commit.
