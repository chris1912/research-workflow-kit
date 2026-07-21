# Project Memory

Codex annotation: Created by Codex on 2026-07-15.
Grok annotation: Stage A+B upgrade decisions and verification recorded by Grok on 2026-07-20.
Grok annotation: Stage D methods-pack slimming recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E0+E1 packaging recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E0/E1 revision 1 (R1-R6) recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E0/E1 revision 2 (V2-1–V2-4) recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E2 method depth (RQ/deep/SR + semantic gates) recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E2 review revision 2 (R1–R5 adversarial tests) recorded by Grok on 2026-07-20.
Codex annotation: Essential Core E2 independently accepted by Codex on 2026-07-20.
Grok annotation: Essential Core E3-A citation integrity vertical slice recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E3-A revision 1 (citation-record state coherence) recorded by Grok on 2026-07-20.
Codex annotation: Essential Core E3-A independently accepted by Codex on 2026-07-20.
Codex annotation: Essential Core E3-B independently accepted by Codex on 2026-07-20.
Grok annotation: Essential Core E3-B paper modes/revision/rebuttal/disclosure recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E3-B revision-2 ledger add/move/annotate truth recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E3-C manuscript review vertical slice + adversarial audit recorded by Grok on 2026-07-20.
Codex annotation: Essential Core E3-C independently accepted by Codex on 2026-07-20.
Grok annotation: Essential Core E3-C revision 1 (R1 calibration 5–20 + R2 identity source tokens) recorded by Grok on 2026-07-20.
Grok annotation: Essential Core E3-D packaging/compatibility consistency recorded by Grok on 2026-07-21.
Codex annotation: Essential Core E3-D independently accepted by Codex on 2026-07-21.
Grok annotation: Essential Core E3-D review revision (R1 workflow-router + R2 manifest date) recorded by Grok on 2026-07-21.

## Project

- Name: `research-workflow-kit`
- Purpose: route evidence-aware research tasks through optional local backends,
  reusable skills, and deterministic writing checks.
- Release shape: first-party adapters and skills only; no virtual environments,
  nested Git repositories, secrets, or personal research runs.

## Decisions

- Public directories use neutral aliases while provenance documents retain the
  original source names and commits.
- Runtime backends are optional and configured through environment variables.
- The first-party layer uses the MIT license.
- The source workspace remains separate from the publish candidate.
- Stage A+B (2026-07-20): contract-first upgrade without new required backends.
  - Provider-neutral `secondary_*` fields; `secondary_provider` may be `null`,
    `grok`, or another provider. Secondary is optional acceleration only.
  - Primary route must complete when secondary capability is unavailable.
  - Blind independent discovery before merge; then normalize DOI/title/year,
    deduplicate, compare omissions, re-screen, and record route outcome.
  - `MERGED_CORE_PAPERS.md` is the sole downstream authority after convergence;
    `core_papers.md` remains a compatibility pre-merge/single-route template.
  - Priority 3–8 OA-first full-text protocol with acquisition log, deep-read
    reports, and manual-action queue; no paywall bypass language.
  - Markdown/structured artifacts remain authoritative; conclusion-bearing runs
    require UTF-8 HTML entry + 3–8 decision pages with local-link checks.
  - Systematic-review / integrity / peer-review stay on `research-methods` entry;
    heavy methods-pack body is not expanded or reduced in Stage A+B.
  - Stage C runtime helpers were not added; templates and docs are sufficient.
- Stage D (2026-07-20): methods-pack slimming to a thin first-party surface.
  - Deleted vendored `skills/research-methods/ars/**` and `codex/**` from the
    working tree (recoverable from Git history).
  - Kept stable public route `skills/research-methods` with rewritten
    `SKILL.md`, compact `manifest.json`, and four local templates.
  - Full Academic Research Skills suite is optional-external, not bundled, and
    not a required runtime dependency; license texts retained under
    `docs/licenses/` for provenance only.
  - No auto-install script, submodule, or silent download for the external suite.
- Essential Core E0+E1 (2026-07-20): replace thin router with `essential_core`.
  - Exact 65-file first-party pack under `skills/research-methods/` (contracts,
    protocols, teams, templates, runtime agents/scripts/hooks/tests, lineage).
  - E1 implements routing planner, hook wrapper, quality gates, dual agent
    surfaces; protocol depth for E2–E4 remains `parity: not_started`.
  - No restore of deleted `ars/**` or `codex/**`; no full ARS behavioral parity claim.
- Essential Core E0/E1 revision 1 (2026-07-20): R1–R6 honesty fixes.
  - Full 68 prefixed aliases in manifest + planner; structured
    `mode_registry_coverage`; tightened `content_depth` with mutation tests.
  - Passport/reviewer gates behavioral or honestly partial; reproducibility
    routes to `experiment/validate`; ambiguous mode defaults documented.
  - Publishable docs no longer claim Stage-D thin router/four templates;
    methods budget exact 65 / soft ceiling 100; repo existing candidates ~210,
    ceiling <220.
- Essential Core E0/E1 revision 2 (2026-07-20): V2-1–V2-4 final normal loop.
  - Ambiguous explicit modes (`full`/`quick`/`plan`/`lit-review`) disambiguate
    workflow by context while retaining the requested mode; bare tokens keep
    safe defaults.
  - Real append-only reset-ledger transition validator (non-mutating).
  - Deterministic reviewer-stage validator for A20 early visibility, premature
    synthesis, and missing minority disposition (multi-process still partial).
  - README wording: Essential Core methods pack / Essential Core 方法核心包.
- Essential Core E2 (2026-07-20): method depth without adding files.
  - `research_question.md`, `deep_research.md`, `systematic_review.md` executable
    depth (FINER/Socratic, eight modes, PRISMA/RoB2/ROBINS-I/GRADE/effect/
    hetero/sensitivity/anti-pooling).
  - Semantic gates parse labeled field bodies (not keyword-only); mutation tests
    cover hollow fields, missing signaling questions, GRADE domain, single
    sensitivity, <3 anti-pooling conditions, silent pooling.
  - `content_depth` no longer exempts the three E2 protocols; E3/E4 remain
    `parity: not_started`; `stats_fallacies_11` still not_started (E4).
  - Exact methods file count remains 65; no full ARS parity claim.
- Essential Core E2 review revision 2 (2026-07-20): adversarial negatives only.
  - Retained prior R1–R5 gate-runner hardening (file-specific PRISMA surfaces,
    local RoB/ROBINS domain cues, GRADE anti-fabrication polarity, anti-pooling
    mandate/prohibition polarity, hetero pre-spec + multiplicity discipline).
  - Added six in-memory adversarial tests in `test_quality_gates.py`; runtime
    suite 45 passed; templates 21; six E2 gates pass; `all` fails only
    `stats_fallacies_11` as E4 not_started.
  - Methods count remains 65; E3 not started; no full ARS parity claim.
- Codex E2 acceptance (2026-07-20): PASS.
  - Independently reviewed six R1-R5 adversarial negatives and their local/file-
    specific failure surfaces.
  - Re-ran 6 focused, 45 runtime, and 21 repository template tests; all passed.
  - `quality_gates all` failed only E4 `stats_fallacies_11` as `not_started`;
    six E2 method gates passed, with 3 partial and 6 not_started protocols.
  - Test-generated ignored `__pycache__` directories remain because deletion was
    rejected by environment policy; they are excluded from the 65-file budget.
- Essential Core E3-A (2026-07-20): citation integrity vertical slice only.
  - Deepened `citation_integrity.md` to `parity: partial` with identity,
    locator/extract, claim-source fidelity, temporal/version, retraction risk,
    contamination advisory, plagiarism boundaries, access states, Mode1/Mode2,
    verdicts, escalation, offline fallback, and human gates.
  - Deepened `evidence_verdict.md`, `quality_gates.md`,
    `citation_integrity_audit.md`, and `claim_verification_report.md` with
    mode-scoped/labeled non-hollow fields; designated surfaces validate
    independently (protocol cannot rescue hollow audit/report).
  - Private helpers `evaluate_citation_record(s)` plus protocol/template surface
    evaluators wired into existing `claim_verdict_vocab` and `content_depth`
    only; no new public gate IDs (frozen at 21).
  - VERIFIED promotion hard rule: locator or extract + coherent access/risk +
    `support_status=supported` + `assessment_source` in
    `{human_confirmed, verified_adapter}`; DOI/token/similarity may only
    downgrade/escalate/unverify.
  - Adversarial tests: DOI-only VERIFIED, contradicted support, retracted/
    corrected/version/access-blocked clean VERIFIED, unknown verdict, missing
    identity, hollow designated surfaces, keyword-complete hollows, public ID
    snapshot, coherent verified + honest inaccessible positives.
  - Verified: runtime tests 57 passed; templates 21 passed; six E2 gates pass;
    `claim_verdict_vocab` + `content_depth` pass; `all` fails only
    `stats_fallacies_11` as E4 not_started; methods file count 65.
  - `academic_paper.md` and `manuscript_review.md` remain `not_started` (E3-B+);
    no full ARS parity claim; E4/E5 not started.
- Essential Core E3-A revision 1 (2026-07-20): citation-record state coherence.
  - Fixed confirmed false passes: VERIFIED with missing/unverified access_state,
    UNVERIFIABLE_ACCESS with access_state=verified, empty aggregate as clean.
  - Exact access vocab `{verified,unverified,unresolvable,access_blocked}`;
    VERIFIED requires access_state=verified, non-empty citation_id/claim_text,
    locator or extract, supported status, safe/resolved risks, approved
    assessment source.
  - access_blocked/unresolvable pairs only with UNVERIFIABLE_ACCESS (bidirectional);
    unknown access/verdict/support/risk vocabulary fails closed.
  - Retracted / expression_of_concern / predatory / version_mismatch cannot be
    clean VERIFIED; corrected requires explicit acknowledgment note.
  - Empty `evaluate_citation_records([])` fails with stable `empty_records`.
  - Coherence fixtures embedded in `claim_verdict_vocab`; adversarial + positive
    direct-helper tests; E3-A test functions use explicit `return None`.
  - Verified: runtime tests 59 passed; templates 21; public gates frozen at 21;
    six E2 gates pass; `claim_verdict_vocab` + `content_depth` pass; `all` fails
    only `stats_fallacies_11` as E4 not_started; methods file count 65.
  - No E3-B+/E4/E5; no full ARS parity claim; no new public gate IDs.
- Codex E3-A acceptance (2026-07-20): PASS.
  - Reproduced and confirmed closure of all four citation-state false passes.
  - Re-ran 14 focused, 59 runtime, and 21 template tests; syntax compile passed.
  - Public gate IDs remain 21, methods source count remains 65, and all gates
    fail only E4 `stats_fallacies_11` as `not_started`.
- Essential Core E3-B (2026-07-20): academic-paper modes + revision/rebuttal/disclosure.
  - Deepened `academic_paper.md` to `parity: partial` with 11 independently
    validated mode-scoped field sets (full/plan/outline_only/revision/
    revision_coach/abstract_only/lit_review/format_convert/citation_check/
    disclosure/rebuttal_audit).
  - Deepened `generator_evaluator.md`, `academic_paper_roles.md`,
    `academic-paper-team.md`, and designated templates `revision_roadmap.md`,
    `rebuttal_audit.md`, `disclosure_statement.md`, `argument_map.md`.
  - Private helpers: `evaluate_all_paper_modes_text`,
    `evaluate_revision_transition`, `evaluate_rebuttal_consistency`,
    revision/rebuttal/disclosure template evaluators + disclosure polarity.
  - Wired into existing `content_depth` and `generator_evaluator_separation`
    only; frozen 21 public gate IDs unchanged.
  - Adversarial tests: one-mode-hollow parametric (11), revision
    delete/strengthen/silent DOI/false ledger/sign-off/recovery, rebuttal
    omit/duplicate/absent change/empty rationale/prose, disclosure polarity,
    designated template isolation, coherent positives.
  - Verified: runtime tests 67 passed; templates 21 passed; six E2 gates pass;
    E3-A gates pass; `content_depth` + `generator_evaluator_separation` pass;
    `all` fails only `stats_fallacies_11` as E4 not_started; methods count 65.
  - `manuscript_review.md` remains `not_started` (E3-C); no full ARS parity;
    E4/E5 not started; no new public gate IDs.
- Essential Core E3-B revision-1 (2026-07-20): closed behavioral false passes.
  - Revision ledger: closed op vocabulary + before/after truth for replace
    (target before, absent after, non-empty summary after), delete, add,
    move, annotate; invalid ops fail `invalid_ledger_op`.
  - Rebuttal set: non-empty unique reviewer points with text; exact
    reviewer/rebuttal point-set equality; required valid coverage and
    response_kind; `coverage=missing` always fails; orphan/duplicate/missing
    and payload-specific failures closed.
  - Added `evaluate_disclosure_record` (fail-closed): none_confirmed needs
    human_confirmation+signer; unknown_pending_human draft-only blocks final;
    auto_filled/self_confirmed forbidden; funded/interests/disclosed need
    details; data/code and policy states mandatory; no auto-fill.
  - Wired disclosure positives/negatives into `generator_evaluator_separation`
    fixtures; expanded direct helper tests.
  - Verified: runtime tests 68 passed; templates 21 passed; focused E3-B
    tests pass; public 21 IDs frozen; E3-A + E2 pass; `all` fails only
    `stats_fallacies_11` as E4 not_started; methods count 65;
    manuscript_review still not_started.
  - Evidence honesty: CLI may initialize auxiliary MCP processes; this run
    authorized and used no MCP tool invocation. Prior structured result
    classification for denied MCP tooling was `network_failure`.
- Essential Core E3-B revision-2 (2026-07-20): final ledger-truth residual fix.
  - Every change-ledger row requires non-empty unique `change_id`
    (`missing_change_id` / `duplicate_change_id`).
  - `add`: non-empty summary absent before and present after.
  - `move`: non-empty target present before and after; first deterministic
    position must differ; unchanged or absent target fails closed.
  - `annotate`: non-empty target present in before or after text.
  - Preserved replace/delete truth, protected/new-evidence/signoff, rebuttal
    and disclosure behavior, 11 paper modes, E3-A, and frozen public APIs.
  - Direct helper tests + `generator_evaluator_separation` public-gate
    fixtures for add/move/annotate positives and the three residual negatives.
  - Verified: runtime tests 68 passed; templates 21 passed; focused E3-B
    9 passed; public 21 IDs frozen; E3-A + E2 pass; `all` fails only
    `stats_fallacies_11` as E4 not_started; methods count 65;
    manuscript_review still not_started.
  - Final normal revision for this ledger-truth defect family; no MCP/web/
    subagents/commit/push.
- Essential Core E3-C (2026-07-20): manuscript-review vertical slice + adversarial audit.
  - Deepened `manuscript_review.md` to `parity: partial` with six independently
    validated mode-scoped field sets (full/re_review/quick/methodology_focus/
    guided/calibration).
  - Deepened `reviewer_independence.md`, `reviewer_panel_roles.md`,
    `paper-reviewer-panel.md`, and designated templates
    `manuscript_review_full.md` + `editorial_decision.md`.
  - Private helpers: `evaluate_reviewer_identity`, `evaluate_rereview_consistency`,
    `evaluate_calibration_gold`, `evaluate_all_reviewer_modes_text`,
    `evaluate_quick_mode_honesty`, `evaluate_guided_mode_honesty`,
    `evaluate_guided_dialogue`, manuscript-review/editorial template evaluators
    (first-occurrence isolation).
  - Wired into existing `reviewer_independence` and `content_depth` only;
    frozen 21 public gate IDs unchanged.
  - Fail-closed identity (named needs non-empty non-circular source + human
    confirm; anonymous/simulated must be explicitly labeled; display name alone
    invalid). Calibration requires human gold set in accepted range 5–20 with
    1:1 predictions; no metrics on invalid sets; no fabricated/persistent claims.
    Re-review covers each prior issue exactly once; partial needs residual gap;
    new issues cannot offset missing priors. Quick cannot claim full panel;
    guided requires question-response-checkpoint progression.
  - Adversarial tests: one-mode-hollow parametric (6) with later-field rescue
    attempts, A20 synthesis/visibility/minority, identity negatives, re-review
    residuals, calibration inadequate/orphan/metrics, quick/guided dumps,
    designated-template isolation while protocol complete, public-gate dual path.
  - Verified: runtime tests 79 passed; templates 21 passed; focused E3-C pass;
    public 21 IDs frozen; E2 + E3-A + E3-B pass; `all` fails only
    `stats_fallacies_11` as E4 not_started; methods count 65.
  - No multi-process isolation claim; no real editorial authority claim; no full
    ARS parity; E3-D/E4/E5 not started; no new public gate IDs; no commit/push.
- Essential Core E3-C revision 1 (2026-07-20): close Codex review findings R1–R2.
  - R1: `MIN_CALIBRATION_GOLD_ITEMS=5`, `MAX_CALIBRATION_GOLD_ITEMS=20`;
    `inadequate_gold_set` for <5, `excessive_gold_set` for >20; five-row positive
    fixtures; protocol/role/runtime surfaces document accepted 5–20 range.
  - R2: short identity sentinels (`na`/`n_a`/`none`/`tbd`/`todo`) match only as
    exact normalized values or whole underscore tokens; phrase detection retained
    for invented/assumed/self-asserted/circular/fabricated/placeholder; legitimate
    sources Nature staff profile / National university roster / journal masthead
    accepted; `n/a` still forbidden.
  - Direct-helper + existing `reviewer_independence` public-gate coverage for
    2-row/21-row calibration negatives and three legitimate identity positives.
  - Verified: focused E3-C pass; runtime 79; templates 21; compile ok; 21 gate IDs;
    RI + content_depth pass; `all` fails only `stats_fallacies_11` not_started;
    methods 65; `git diff --check` clean for product edits.
  - Artifacts written only under
    `.codex/grok-runs/2026-07-20-ars-essential-core-e3c-revision-1/`; no E3-D/E4/E5;
    no public gate ID changes; no commit/push.


- Codex E3-C acceptance (2026-07-20): PASS.
  - Independently reproduced calibration boundaries: 2 rows fail, 5 pass, and
    21 fail, with no metrics emitted on invalid sets.
  - Independently confirmed legitimate Nature/National/journal identity sources
    pass while `n/a` and invented-prestige provenance fail closed.
  - Re-ran 13 focused, 79 runtime, and 21 template tests; syntax compile passed.
  - Public gates remain 21, methods source files remain 65, and `all` fails only
    E4 `stats_fallacies_11` as `not_started`.
  - Manuscript review remains `parity: partial`; no multi-process isolation,
    real editorial authority, E3-D/E4/E5, commit, or push claim.
- Essential Core E3-D (2026-07-21): packaging/compatibility consistency closeout.
  - Reconciled public packaging surfaces with accepted E2 + E3-A/B/C parity:
    six protocols `parity: partial` (research_question, deep_research,
    systematic_review, academic_paper, citation_integrity, manuscript_review);
    three E4 protocols remain `parity: not_started` (academic_pipeline,
    experiment, optional_runtime).
  - Updated COMPATIBILITY, LINEAGE_INDEX, manifest annotations/parity claim,
    SKILL routing status, NOTICE honesty note, and public orientation docs
    (README, ARCHITECTURE, WORKFLOW, NAME_MAP, DEPENDENCIES, START_HERE,
    ARCHITECTURE_ROADMAP, THIRD_PARTY_MANIFEST current-state wording).
  - MODE_REGISTRY mode/alias names and counts unchanged; packaging_mode
    remains `essential_core`; manifest schema/aliases/public route unchanged.
  - Added four focused packaging-consistency regression tests in
    `tests/test_templates.py` (protocol path parity, manifest/SKILL claims,
    COMPATIBILITY/LINEAGE, public-surface stale-claim scan).
  - Verified: templates 25 passed; runtime 79 passed; public gates 21;
    `all` fails only `stats_fallacies_11` as E4 not_started; methods count 65;
    JSON parse + Python syntax compile ok; verify_publish_tree clean after
    cache removal; `git diff --check` clean on allowed product paths.
  - No protocol body/runtime/code changes beyond packaging docs+tests;
    no full ARS parity claim; no multi-process/editorial-authority claim;
    no E4/E5; no commit/push.
  - Intentionally untouched stale out-of-scope surfaces (historical notes or
    non-owned paths): root `AGENTS.md` still says E3–E4 not_started (out of
    E3-D ownership); protocol E4 skeleton headers still say "E2-E4 pending"
    as reserved-body historical baseline; some runtime agent notes remain
    outside allowed product paths.
- Essential Core E3-D review revision (2026-07-21): close R1/R2 only.
  - R1: `skills/workflow-router/SKILL.md` research-methods route now states E2
    RQ/deep/SR and E3 paper/integrity/review operational `parity: partial`,
    E4 pipeline/experiment/optional_runtime `parity: not_started`, with full
    ARS honesty boundary preserved.
  - R1 regression: `E3D_PUBLIC_PACKAGING_SURFACES` now includes
    `skills/workflow-router/SKILL.md` and `skills/research-methods/NOTICE.md`.
  - R2: `manifest.json` `generated_date` advanced to `2026-07-21` to match
    adapter `1.0.0-e3` and E3-D annotation; schema/aliases/route/mode unchanged.
  - R2 regression: focused assertion that adapter_version, generated_date, and
    annotation date stay coherent for the E3-D artifact.
  - No E4/E5, protocol/runtime, root AGENTS, commit, or push.


- Codex E3-D acceptance (2026-07-21): PASS.
  - Public methods packaging, compatibility, lineage, manifest, router, README,
    Markdown/HTML orientation, dependency, and third-party surfaces now state
    six E2/E3 protocols partial and three E4 protocols not_started.
  - Independent checks: 4 focused, 25 template, and 79 runtime tests passed;
    three key gates passed; 21 public IDs and 65 methods files remained stable.
  - `quality_gates all` failed only E4 `stats_fallacies_11` as `not_started`;
    publish-tree and scoped diff checks passed.
  - Review revision closed the stale workflow-router claim and manifest date
    mismatch; no E4/E5, commit, push, or publication work was performed.


## Current route

1. Research question and guide decomposition.
2. Search strategy and optional dual-route preflight.
3. Primary literature discovery (+ optional blind secondary).
4. Merge to `MERGED_CORE_PAPERS.md`; priority OA-first full text as needed.
5. Document parsing, evidence QA, and literature mapping.
6. Research synthesis and long-form drafting.
7. Academic editing, prose linting, HTML delivery for conclusions, packaging.

## Risks

- External providers may require credentials or network access.
- The optional external Academic Research Skills suite retains a non-commercial
  upstream license (CC BY-NC-4.0 as stated in retained notices); the local thin
  router/templates are first-party MIT surface.
- No copied content from the unlicensed prompt reference library is included.
- Users who need the full historical methods suite must install it outside this
  repository under upstream terms; absence of that suite is normal.

## Verification

Codex annotation: Verified by Codex on 2026-07-15.

- `python -m pytest`: 6 tests passed.
- `python -m compileall -q src tests scripts`: passed; generated caches were removed.
- Formatter smoke test: passed with a temporary Word output and no tracked binary.
- JSON/JSONL templates: parsed successfully.
- HTML desktop/mobile browser check: both pages loaded without console errors and all relative links resolved.
- Publish-tree scan: no nested Git metadata, junctions, secrets, absolute machine paths, binaries, or generated caches.

Grok annotation: Stage A+B checks run by Grok on 2026-07-20.

- `python -m pytest tests/test_templates.py`: **12 passed**.
- `python -m pytest`: **17 passed** (5 adapter + 12 template tests).
- `python scripts/verify_publish_tree.py`: **clean** after generated caches removed;
  scanner now skips local `.codex` agent-run evidence (gitignored, not publishable).
- JSON/JSONL/CSV parsing for proposal templates: covered by `tests/test_templates.py`.
- Structural HTML UTF-8 / required-section / relative-link checks: covered by
  `tests/test_templates.py` for public docs HTML and proposal HTML shells.
- `python -m compileall -q src tests scripts`: **passed**; generated caches removed after.
- No dependency install and no external service contact during Stage A+B.

Grok annotation: Stage D checks run by Grok on 2026-07-20.

- Deleted working-tree `skills/research-methods/ars` and `codex` after absolute
  path child validation; did not use `git rm` or stage deletions.
- Focused template/manifest absence/link/file-count tests added in
  `tests/test_templates.py`.
- Verification order: focused pytest, full pytest, `git diff --check`,
  compileall with bytecode outside the repo, `verify_publish_tree.py`, and
  publish-candidate file count below 200.
- No dependency install, no external service contact, no commit/push.

## GitHub Publication

Codex annotation: Published by Codex on 2026-07-15.

- repository: `https://github.com/chris1912/research-workflow-kit`
- visibility: public
- default branch: `main`
- latest local commit on remote-tracking `origin/main`: `659783f`
- GitHub Actions quality workflow: present as `.github/workflows/quality.yml`

Grok annotation: Pre-publish prepare and audit recorded by Grok on 2026-07-20.

- Prepared bilingual community/docs surfaces for a future GitHub update; no
  stage, commit, or push was performed in this stage.
- `CITATION.cff` release-candidate version set to `0.2.0` dated `2026-07-20`.
- Working-tree publish candidates (existing paths from
  `git ls-files --cached --others --exclude-standard`): **152** (below 200).
- Intentional methods-pack deletions remain **1,061** paths under
  `skills/research-methods/ars/**` (1045) and `skills/research-methods/codex/**`
  (16); not staged.
- Local checks in this stage: focused pytest 20 passed; full pytest 25 passed;
  `git diff --check` clean; compileall with bytecode outside the repository
  passed; `scripts/verify_publish_tree.py` clean after cache removal.
- Deterministic secret scanners (`ggshield`, Gitleaks, TruffleHog) were not
  installed; working-tree and full-history secret scans marked WARN with
  count-only local fallback only.
- External `markdownlint` / `markdownlint-cli2` / `lychee` unavailable; marked
  WARN; local template HTML/link tests and path checks used as fallback.
- No `.github/secret_scanning.yml` path exclusions present. Recommend enabling
  GitHub Secret Protection and push protection on the remote repository.
- Audit artifacts remain under ignored local agent-run directories and are
  outside the publication set.

Codex annotation: Final local acceptance completed by Codex on 2026-07-20.

- Accepted the Stage A+B workflow-contract upgrade and Stage D methods-pack
  slimming after independent diff, scope, and test review.
- Confirmed **152** existing publish candidates and **1,061** intentional,
  unstaged deletions confined to `skills/research-methods/ars/**` and
  `skills/research-methods/codex/**`.
- Re-ran 20 focused tests and 25 full tests; compileall, YAML/CFF parsing,
  `git diff --check`, and `scripts/verify_publish_tree.py` passed.
- Final GitHub pre-publication audit status is **WARN** with no blockers because
  professional secret scanners, markdownlint/lychee, and visual browser review
  were unavailable or not run.
- No files were staged, committed, pushed, fetched, tagged, or published.

## 2026-07-21 Project-specific teaching entry

- Added `SCIENTIFIC_WORKFLOW_START_HERE.html` at the repository root as the
  lightweight project's own entry manual, distinct from the full lab manual.
- Kept `docs/START_HERE.html` as the detailed visual route guide and updated
  `README.md` and `AGENTS.md` to route users through the new project entry first.
- The new entry preserves the public kit's evidence boundary, optional
  secondary route, merged-core authority, priority full-text contract, HTML
  delivery gate, and Essential Core parity limits.

## 2026-07-21 Public entry manual rebuild (Grok Stage)

- Rebuilt `SCIENTIFIC_WORKFLOW_START_HERE.html` as a Chinese-first lightweight
  teaching entry with purpose/audience, public-vs-full-lab difference, skill
  overview, evidence states, Essential Core limits, setup/verification, and
  clear routes to `docs/START_HERE.html` and `README.md`.
- Rebuilt `docs/START_HERE.html` as the detailed project-specific teaching
  manual: ten-phase route, all seven first-party skills (when/input/output + CN
  examples), artifact path table, required vs optional gates, evidence/safety
  rules, Essential Core parity honesty, ≥15 copyable prompts, setup/security/
  licensing, and repository-relative documentation links.
- README Start-here wording aligned: “Detailed teaching manual / 详细教学手册”.
- Conceptual reference only from the sibling full-lab manual; no private paths,
  credentials, or full-runtime assumptions. Allowed-path edit only; no source,
  skills, tests, or remote-state changes in this stage.

## 2026-07-22 Project-level lite skill router

- Added `skills/scientific-workflow-lab-lite/SKILL.md` as this lightweight
  kit's project-level callable router. It is deliberately named separately
  from the full-lab `scientific-workflow-lab` skill and does not modify it.
- Added `skills/scientific-workflow-lab-lite/agents/openai.yaml` so hosts that
  support project-local skill metadata can discover or implicitly invoke
  `$scientific-workflow-lab-lite`.
- Updated the root entry, detailed teaching manual, README, architecture
  roadmap, architecture notes, and AGENTS guidance to distinguish this lite
  router from the full-lab skill and the seven specialist skills; documented
  the fallback when a host cannot load repository skills.

## Update rule

Update this file when the public tree, route order, provenance policy, or
external dependency contract changes.
