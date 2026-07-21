"""Tests for public example artifacts and proposal-research contract templates.

Grok annotation: Expanded by Grok on 2026-07-20 for Stage A+B contract surface.
Grok annotation: Added focused publish-scanner skip regression on 2026-07-20.
Grok annotation: Stage D research-methods thin-pack tests added by Grok on 2026-07-20.
Grok annotation: Stage D revision-loop-1 factual regression tests by Grok on 2026-07-20.
Grok annotation: Essential Core E0+E1 packaging assertions updated by Grok on 2026-07-20.
Grok annotation: E3-D packaging-consistency regression tests added by Grok on 2026-07-21.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_TEMPLATES = ROOT / "skills" / "proposal-research" / "templates"
PROPOSAL_EVALS = ROOT / "skills" / "proposal-research" / "evals" / "evals.json"
METHODS_ROOT = ROOT / "skills" / "research-methods"
METHODS_TEMPLATES = METHODS_ROOT / "core" / "templates"
METHODS_MANIFEST = METHODS_ROOT / "manifest.json"
PUBLIC_HTML = [
    ROOT / "docs" / "START_HERE.html",
    ROOT / "docs" / "ARCHITECTURE_ROADMAP.html",
    PROPOSAL_TEMPLATES / "core_papers_page.html",
    PROPOSAL_TEMPLATES / "priority_papers_page.html",
]
PRIVATE_MARKERS = ("D:\\AIAgent\\", "C:\\Users\\", "D:/AIAgent/", "C:/Users/")
REQUIRED_TEMPLATE_NAMES = {
    "literature_route_status.json",
    "MERGED_CORE_PAPERS.md",
    "core_papers.md",
    "priority_papers.md",
    "fulltext_acquisition.csv",
    "FULLTEXT_MANUAL_ACTION_REQUIRED.md",
    "deep_read_report.md",
    "html_delivery_checklist.md",
    "core_papers_page.html",
    "priority_papers_page.html",
    "search_strategy.md",
    "candidate_literature_pool.csv",
    "evidence_cards.jsonl",
}
METHODS_TEMPLATE_SECTIONS = {
    "prisma_protocol.md": (
        "Research question",
        "Protocol scope",
        "Search plan",
        "Human gates",
        "Evidence states",
    ),
    "citation_integrity_audit.md": (
        "Citation inventory",
        "Claim-to-source audit",
        "Integrity red flags",
        "Human gates",
        "Uncertainty",
    ),
    "manuscript_review_full.md": (
        "Structure map",
        "Claim support",
        "Simulated peer-review",
        "Human gates",
        "Evidence badge",
    ),
    "reproducibility_checklist.md": (
        "Study and experiment intent",
        "Analysis and statistical-interpretation",
        "Reproducibility artifacts",
        "Human gates",
        "Evidence states",
    ),
}
METHODS_MANIFEST_TEMPLATE_PATHS = {
    "core/templates/prisma_protocol.md",
    "core/templates/manuscript_review_full.md",
    "core/templates/citation_integrity_audit.md",
    "core/templates/reproducibility_checklist.md",
}
# Normative E3 closeout parity: derived from explicit protocol paths only.
E3D_PARTIAL_PROTOCOL_RELS = (
    "core/protocols/research_question.md",
    "core/protocols/deep_research.md",
    "core/protocols/systematic_review.md",
    "core/protocols/academic_paper.md",
    "core/protocols/citation_integrity.md",
    "core/protocols/manuscript_review.md",
)
E3D_NOT_STARTED_PROTOCOL_RELS = (
    "core/protocols/academic_pipeline.md",
    "core/protocols/experiment.md",
    "core/protocols/optional_runtime.md",
)
E3D_PUBLIC_PACKAGING_SURFACES = (
    METHODS_ROOT / "SKILL.md",
    METHODS_ROOT / "COMPATIBILITY.md",
    METHODS_ROOT / "LINEAGE_INDEX.md",
    METHODS_ROOT / "NOTICE.md",
    METHODS_MANIFEST,
    ROOT / "skills" / "workflow-router" / "SKILL.md",
    ROOT / "README.md",
    ROOT / "docs" / "ARCHITECTURE.md",
    ROOT / "docs" / "WORKFLOW.md",
    ROOT / "docs" / "NAME_MAP.md",
    ROOT / "docs" / "DEPENDENCIES.md",
    ROOT / "docs" / "START_HERE.html",
    ROOT / "docs" / "ARCHITECTURE_ROADMAP.html",
    ROOT / "docs" / "THIRD_PARTY_MANIFEST.json",
)
STALE_BLANKET_E2_E4_PATTERNS = (
    re.compile(r"E2\s*[–-]\s*E4\s+protocol\s+depth\s+remains\s+`?parity:\s*not_started`?", re.I),
    re.compile(r"E2\s*[–-]\s*E4\s+协议深度仍[为标]", re.I),
    re.compile(r"E2\s*[–-]\s*E4\s+协议深度为\s*`?parity:\s*not_started`?", re.I),
    re.compile(r"protocol bodies reserved for E2\s*[–-]\s*E4\s+remain\s+`?parity:\s*not_started`?", re.I),
    re.compile(r"protocol bodies for E2-E4 marked parity not_started", re.I),
    re.compile(r"E2\s*[–-]\s*E4\s+协议深度尚未开始", re.I),
    re.compile(r"E2–E4 protocol depth not_started", re.I),
    re.compile(r"E2-E4 protocol depth not_started", re.I),
    re.compile(r"E3\s*[–-]\s*E4 protocol bodies remain\s+`?parity:\s*not_started`?", re.I),
    re.compile(r"E3-E5 are all unclaimed|E3-E5 not claimed|E3-E4 protocols remain not_started", re.I),
)
STALE_E3_PENDING_PATTERNS = (
    re.compile(r"Manuscript review\s*/\s*integrity\s*/\s*paper modes depth\s*\|\s*not_started\s*\|\s*E3", re.I),
    re.compile(r"E3 depth pending", re.I),
    re.compile(r"manuscript review/integrity/paper modes are E3 pending", re.I),
    re.compile(r"E3 pending", re.I),
)
DOC_SURFACE_FOR_LINK_AUDIT = [
    ROOT / "README.md",
    ROOT / "PROJECT_MEMORY.md",
    ROOT / "docs" / "START_HERE.html",
    ROOT / "docs" / "WORKFLOW.md",
    ROOT / "docs" / "ARCHITECTURE.md",
    ROOT / "docs" / "ARCHITECTURE_ROADMAP.html",
    ROOT / "docs" / "DEPENDENCIES.md",
    ROOT / "docs" / "NAME_MAP.md",
    ROOT / "docs" / "THIRD_PARTY_MANIFEST.json",
    ROOT / "docs" / "THIRD_PARTY_NOTICES.md",
    ROOT / "skills" / "workflow-router" / "SKILL.md",
    ROOT / "skills" / "proposal-research" / "SKILL.md",
    PROPOSAL_EVALS,
    METHODS_ROOT / "SKILL.md",
    METHODS_MANIFEST,
]


def _read_text(path: Path) -> str:
    """Read a UTF-8 text file and fail clearly when the path is missing."""
    if not path.is_file():
        raise FileNotFoundError(f"missing required template or doc: {path}")
    return path.read_text(encoding="utf-8")


def test_example_evidence_card_is_valid_jsonl() -> None:
    path = ROOT / "examples" / "minimal" / "evidence_card.jsonl"
    records = [
        json.loads(line)
        for line in _read_text(path).splitlines()
        if line.strip()
    ]
    assert len(records) == 1
    assert records[0]["epistemic_status"] == "placeholder"
    return None


def test_required_proposal_templates_exist() -> None:
    present = {path.name for path in PROPOSAL_TEMPLATES.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_TEMPLATE_NAMES - present)
    assert missing == [], f"missing proposal templates: {missing}"
    return None


def test_literature_route_status_json_schema_keys() -> None:
    path = PROPOSAL_TEMPLATES / "literature_route_status.json"
    data = json.loads(_read_text(path))
    required_keys = {
        "primary_route",
        "secondary_provider",
        "secondary_skill_available",
        "secondary_cli_available",
        "secondary_discovery_ok",
        "secondary_model",
        "selected_mode",
        "fallback_reason",
        "artifacts",
    }
    missing = sorted(required_keys - set(data))
    assert missing == [], f"literature_route_status missing keys: {missing}"
    assert data["selected_mode"] in {
        "primary_only",
        "primary_secondary_parallel",
        "primary_only_after_secondary_failure",
    }
    assert "secondary_" in " ".join(data.keys()) or "secondary_provider" in data
    return None


def test_proposal_jsonl_and_csv_templates_parse() -> None:
    jsonl_path = PROPOSAL_TEMPLATES / "evidence_cards.jsonl"
    for line_no, line in enumerate(_read_text(jsonl_path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSONL at {jsonl_path}:{line_no}") from exc

    for csv_name in ("candidate_literature_pool.csv", "fulltext_acquisition.csv"):
        csv_path = PROPOSAL_TEMPLATES / csv_name
        with csv_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            raise AssertionError(f"CSV template has no header row: {csv_path}")
        assert all(cell.strip() for cell in rows[0]), f"empty header in {csv_path}"
    return None


def test_merged_core_authority_language() -> None:
    merged = _read_text(PROPOSAL_TEMPLATES / "MERGED_CORE_PAPERS.md")
    core = _read_text(PROPOSAL_TEMPLATES / "core_papers.md")
    assert "sole downstream authority" in merged.lower() or "唯一权威" in merged
    assert "MERGED_CORE_PAPERS.md" in core
    assert "authority" in core.lower() or "权威" in core
    return None


def test_priority_fulltext_templates_forbid_paywall_bypass() -> None:
    texts = [
        _read_text(PROPOSAL_TEMPLATES / "priority_papers.md"),
        _read_text(PROPOSAL_TEMPLATES / "FULLTEXT_MANUAL_ACTION_REQUIRED.md"),
        _read_text(PROPOSAL_TEMPLATES / "priority_papers_page.html"),
        _read_text(PROPOSAL_TEMPLATES / "html_delivery_checklist.md"),
    ]
    joined = "\n".join(texts).lower()
    assert "paywall bypass" in joined or "付费墙绕过" in joined
    assert "oa" in joined or "open access" in joined or "开放获取" in joined
    return None


def test_proposal_evals_cover_new_contracts() -> None:
    data = json.loads(_read_text(PROPOSAL_EVALS))
    assert data["skill_name"] == "proposal-research"
    names = {item["name"] for item in data["evals"]}
    expected = {
        "guide_only_deep_research_startup",
        "guide_with_keywords_broad_search_plan",
        "existing_direction_with_background",
        "secondary_provider_missing_primary_only_fallback",
        "priority_fulltext_oa_first_and_manual_queue",
        "html_delivery_gate_for_conclusions",
        "research_methods_routing_for_integrity",
    }
    missing = sorted(expected - names)
    assert missing == [], f"missing eval cases: {missing}"
    return None


@pytest.mark.parametrize("html_path", PUBLIC_HTML, ids=lambda p: p.name)
def test_public_html_utf8_sections_and_local_links(html_path: Path) -> None:
    """Check UTF-8 integrity, required sections, and relative href targets."""
    raw = html_path.read_bytes()
    text = raw.decode("utf-8")
    assert "\ufffd" not in text, f"replacement character present in {html_path}"
    assert re.search(r'charset\s*=\s*"?utf-8"?', text, flags=re.I), (
        f"missing UTF-8 charset declaration in {html_path}"
    )

    required_snippets = {
        "START_HERE.html": ["evidence-boundary", "dual-route", "MERGED_CORE_PAPERS", "HTML"],
        "ARCHITECTURE_ROADMAP.html": ["MERGED_CORE_PAPERS", "START_HERE.html", "双路由"],
        "core_papers_page.html": [
            "evidence-boundary",
            "merged-core-table",
            "Provenance",
            "@media print",
        ],
        "priority_papers_page.html": [
            "evidence-boundary",
            "priority-table",
            "oa_first",
            "@media print",
        ],
    }
    for snippet in required_snippets[html_path.name]:
        assert snippet in text, f"{html_path.name} missing required snippet: {snippet}"

    hrefs = re.findall(r'href="([^"]+)"', text)
    for href in hrefs:
        if href.startswith(("#", "mailto:", "http://", "https://")):
            continue
        if "://" in href:
            raise AssertionError(f"non-local absolute URL in {html_path.name}: {href}")
        target = (html_path.parent / href).resolve()
        assert target.exists(), f"broken relative link in {html_path.name}: {href}"
    return None


def test_no_private_path_markers_in_first_party_upgrade_surface() -> None:
    paths = list(PROPOSAL_TEMPLATES.glob("*"))
    paths.extend(list(METHODS_TEMPLATES.glob("*")))
    paths.extend(
        [
            ROOT / "docs" / "START_HERE.html",
            ROOT / "docs" / "WORKFLOW.md",
            ROOT / "docs" / "ARCHITECTURE.md",
            ROOT / "docs" / "ARCHITECTURE_ROADMAP.html",
            ROOT / "docs" / "DEPENDENCIES.md",
            ROOT / "docs" / "NAME_MAP.md",
            ROOT / "docs" / "THIRD_PARTY_MANIFEST.json",
            ROOT / "docs" / "THIRD_PARTY_NOTICES.md",
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "PROJECT_MEMORY.md",
            ROOT / "skills" / "proposal-research" / "SKILL.md",
            ROOT / "skills" / "workflow-router" / "SKILL.md",
            METHODS_ROOT / "SKILL.md",
            METHODS_MANIFEST,
            PROPOSAL_EVALS,
        ]
    )
    findings: list[str] = []
    for path in paths:
        if not path.is_file():
            continue
        text = _read_text(path)
        for marker in PRIVATE_MARKERS:
            if marker in text:
                findings.append(f"{path.relative_to(ROOT)} contains {marker}")
    assert findings == [], "private path markers found:\n" + "\n".join(findings)
    return None


def test_research_methods_templates_exist_with_required_sections() -> None:
    """Prove Essential Core successor templates exist with required sections."""
    if not METHODS_TEMPLATES.is_dir():
        raise AssertionError(f"missing methods templates directory: {METHODS_TEMPLATES}")
    present = {path.name for path in METHODS_TEMPLATES.iterdir() if path.is_file()}
    missing = sorted(set(METHODS_TEMPLATE_SECTIONS) - present)
    assert missing == [], f"missing research-methods templates: {missing}"
    for name, sections in METHODS_TEMPLATE_SECTIONS.items():
        text = _read_text(METHODS_TEMPLATES / name)
        for section in sections:
            assert section in text, f"{name} missing required section: {section}"
    return None


def test_research_methods_ars_and_codex_absent() -> None:
    """Vendored ars/ and codex/ bodies must not remain in the working tree."""
    assert not (METHODS_ROOT / "ars").exists(), "skills/research-methods/ars must be absent"
    assert not (METHODS_ROOT / "codex").exists(), "skills/research-methods/codex must be absent"
    return None


def test_research_methods_manifest_marks_external_suite_not_bundled() -> None:
    """Manifest must parse and declare essential_core offline, suite not bundled."""
    data = json.loads(_read_text(METHODS_MANIFEST))
    assert data.get("packaging_mode") == "essential_core"
    external = data.get("external_suite")
    if not isinstance(external, dict):
        raise AssertionError("manifest.external_suite must be an object")
    assert external.get("bundled") is False
    assert external.get("required_runtime") is False
    assert external.get("status") == "optional-external"
    local = data.get("local_surface")
    if not isinstance(local, dict):
        raise AssertionError("manifest.local_surface must be an object")
    assert local.get("works_offline_without_external_suite") is True
    templates = local.get("templates")
    if not isinstance(templates, list):
        raise AssertionError("manifest.local_surface.templates must be a list")
    assert set(templates) == METHODS_MANIFEST_TEMPLATE_PATHS
    return None


def test_no_documentation_links_into_removed_methods_subtrees() -> None:
    """Publishable docs must not hyperlink into deleted ars/ or codex/ bodies."""
    link_patterns = (
        re.compile(
            r"\[[^\]]*\]\(\s*(?:\./|\.\./)*(?:skills/research-methods/)?(?:ars|codex)(?:/[^)\s]*)?\s*\)"
        ),
        re.compile(
            r'href="(?:\./|\.\./)*(?:skills/research-methods/)?(?:ars|codex)(?:/[^"]*)?"'
        ),
    )
    findings: list[str] = []
    for path in DOC_SURFACE_FOR_LINK_AUDIT:
        if not path.is_file():
            raise FileNotFoundError(f"missing documentation surface file: {path}")
        text = _read_text(path)
        for pattern in link_patterns:
            match = pattern.search(text)
            if match is not None:
                findings.append(
                    f"{path.relative_to(ROOT).as_posix()}: {match.group(0)}"
                )
    assert findings == [], "stale links into removed methods subtrees:\n" + "\n".join(
        findings
    )
    return None


def test_publish_candidate_file_count_below_220() -> None:
    """Existing paths from git index plus untracked publishables stay under 220.

    Baseline after Essential Core is about 210 existing candidates. The repo-wide
    ceiling is narrow (<220) so unreviewed growth is not hidden. Methods pack
    budget is enforced separately (exact 65 this stage; soft ceiling 100).
    """
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {result.stderr.strip()}")
    listed = [
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    candidate_count = sum(1 for path in listed if (ROOT / path).exists())
    assert candidate_count < 220, (
        f"publish candidate file count {candidate_count} is not below 220"
    )
    return None


def test_methods_pack_file_budget_exact_65() -> None:
    """Essential Core methods pack is exactly 65 files this stage, never above 100."""
    files = [
        path
        for path in METHODS_ROOT.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and not path.name.endswith(".pyc")
    ]
    count = len(files)
    assert count == 65, (
        f"methods pack file count {count} != 65 at this stage; "
        "additions above 65 need written justification in the run note"
    )
    assert count <= 100, f"methods pack soft ceiling 100 exceeded: {count}"
    return None


def test_methods_license_paths_exist_on_disk() -> None:
    """Every local license path referenced on the methods provenance surface must exist."""
    surface_paths = [
        METHODS_ROOT / "SKILL.md",
        METHODS_MANIFEST,
        ROOT / "docs" / "DEPENDENCIES.md",
        ROOT / "docs" / "THIRD_PARTY_MANIFEST.json",
        ROOT / "docs" / "THIRD_PARTY_NOTICES.md",
    ]
    path_pattern = re.compile(
        r"(?:docs/licenses/|licenses/)[A-Za-z0-9._/-]*academic-research-skills[A-Za-z0-9._/-]*"
    )
    referenced: set[str] = set()
    for path in surface_paths:
        text = _read_text(path)
        for match in path_pattern.findall(text):
            normalized = match.replace("\\", "/")
            if normalized.startswith("licenses/"):
                normalized = f"docs/{normalized}"
            referenced.add(normalized.strip("`\"' "))
    assert referenced, "expected at least one academic-research-skills license reference"
    missing = sorted(
        path for path in referenced if not (ROOT / path).is_file()
    )
    assert missing == [], f"referenced license paths missing on disk: {missing}"
    return None


def test_agents_md_describes_essential_core_methods() -> None:
    """Root AGENTS.md must not describe research-methods as a heavy bundled pack."""
    text = _read_text(ROOT / "AGENTS.md").lower()
    assert "skills/research-methods" in text or "research-methods" in text
    heavy_phrases = (
        "heavy pack",
        "unmodified heavy",
        "without expanding or reducing that heavy pack",
    )
    for phrase in heavy_phrases:
        assert phrase not in text, f"AGENTS.md still uses heavy-pack wording: {phrase}"
    assert (
        "essential_core" in text
        or "essential core" in text
        or "optional external" in text
        or "not_started" in text
    )
    return None


def _load_verify_publish_tree() -> ModuleType:
    """Load scripts/verify_publish_tree.py without requiring package install."""
    script_path = ROOT / "scripts" / "verify_publish_tree.py"
    spec = importlib.util.spec_from_file_location("verify_publish_tree", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load publish scanner: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_verify_publish_tree_scans_unignored_codex_content(tmp_path: Path) -> None:
    """Unignored `.codex/<other>/` must not be silently skipped by the scanner."""
    module = _load_verify_publish_tree()
    other_dir = tmp_path / ".codex" / "other"
    other_dir.mkdir(parents=True)
    other_sample = other_dir / "sample.txt"
    other_sample.write_text("unignored codex content", encoding="utf-8")

    grok_dir = tmp_path / ".codex" / "grok-runs" / "run-1"
    grok_dir.mkdir(parents=True)
    (grok_dir / "sample.txt").write_text("gitignored agent evidence", encoding="utf-8")

    scanned = {path.relative_to(tmp_path).as_posix() for path in module.iter_files(tmp_path)}
    assert ".codex/other/sample.txt" in scanned
    assert ".codex/grok-runs/run-1/sample.txt" not in scanned
    return None


def _protocol_parity_label(text: str) -> str:
    """Extract the first **parity: <label>** marker from a protocol body."""
    match = re.search(r"\*\*parity:\s*(partial|not_started)\*\*", text, flags=re.I)
    if match is None:
        raise AssertionError("protocol missing **parity: partial|not_started** marker")
    return match.group(1).lower()


def test_e3d_protocol_parity_six_partial_three_not_started() -> None:
    """Derive six partial / three not_started parity labels from explicit paths."""
    assert len(E3D_PARTIAL_PROTOCOL_RELS) == 6
    assert len(E3D_NOT_STARTED_PROTOCOL_RELS) == 3
    for rel in E3D_PARTIAL_PROTOCOL_RELS:
        path = METHODS_ROOT / rel
        label = _protocol_parity_label(_read_text(path))
        assert label == "partial", f"{rel} expected parity partial, got {label}"
    for rel in E3D_NOT_STARTED_PROTOCOL_RELS:
        path = METHODS_ROOT / rel
        label = _protocol_parity_label(_read_text(path))
        assert label == "not_started", f"{rel} expected parity not_started, got {label}"
    return None


def test_e3d_manifest_and_skill_claim_partial_not_full_ars() -> None:
    """Manifest and SKILL must claim E2/E3 partial depth without full ARS or E4 done."""
    data = json.loads(_read_text(METHODS_MANIFEST))
    assert data.get("packaging_mode") == "essential_core"
    assert data.get("adapter_version") == "1.0.0-e3"
    assert data.get("generated_date") == "2026-07-21"
    annotation = str(data.get("annotation", ""))
    assert "2026-07-21" in annotation
    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        raise AssertionError("manifest.provenance must be an object")
    parity_claim = str(provenance.get("parity_claim", ""))
    assert "partial" in parity_claim.lower()
    assert "full ars" in parity_claim.lower() or "not claimed" in parity_claim.lower()
    assert "e4" in parity_claim.lower() or "e4-e5" in parity_claim.lower()
    joined_notes = "\n".join(str(item) for item in data.get("runtime_notes", []))
    package_text = "\n".join([parity_claim, joined_notes, annotation]).lower()
    assert "not_started" in package_text
    assert "e3-e5 are all unclaimed" not in package_text
    assert "e3-e4 protocols remain not_started" not in package_text
    assert "e2-e4" not in package_text or "partial" in package_text

    skill = _read_text(METHODS_ROOT / "SKILL.md")
    skill_l = skill.lower()
    assert "parity: partial" in skill_l
    assert "e4" in skill_l and "not_started" in skill_l
    assert "full ars" in skill_l
    assert "e3–e4 protocol bodies remain" not in skill_l
    assert "e3-e4 protocol bodies remain" not in skill_l
    return None


def test_e3d_compatibility_and_lineage_match_protocol_state() -> None:
    """COMPATIBILITY and LINEAGE_INDEX must not mark accepted E2/E3 bodies not_started."""
    compat = _read_text(METHODS_ROOT / "COMPATIBILITY.md")
    assert "Manuscript review / integrity / paper modes depth | partial" in compat.replace(
        "|", " | "
    ) or re.search(
        r"Manuscript review\s*/\s*integrity\s*/\s*paper modes depth\s*\|\s*partial",
        compat,
        flags=re.I,
    )
    assert re.search(
        r"Pipeline \+ experiment \+ optional_runtime depth\s*\|\s*not_started",
        compat,
        flags=re.I,
    )
    assert "E3 depth pending" not in compat
    assert not re.search(
        r"Manuscript review\s*/\s*integrity\s*/\s*paper modes depth\s*\|\s*not_started",
        compat,
        flags=re.I,
    )

    lineage = _read_text(METHODS_ROOT / "LINEAGE_INDEX.md")
    for rel in E3D_PARTIAL_PROTOCOL_RELS:
        row_match = None
        for line in lineage.splitlines():
            if rel in line and line.strip().startswith("|"):
                row_match = line
                break
        assert row_match is not None, f"LINEAGE_INDEX missing row for {rel}"
        assert "body not_started" not in row_match, (
            f"LINEAGE_INDEX still marks accepted protocol body not_started: {rel}"
        )
        assert "parity: partial" in row_match or "partial" in row_match
    for rel in E3D_NOT_STARTED_PROTOCOL_RELS:
        row_match = None
        for line in lineage.splitlines():
            if rel in line and line.strip().startswith("|"):
                row_match = line
                break
        assert row_match is not None, f"LINEAGE_INDEX missing row for {rel}"
        assert "not_started" in row_match, f"E4 lineage row must remain not_started: {rel}"
    return None


def test_e3d_public_surfaces_reject_stale_blanket_claims() -> None:
    """Allowed packaging/public docs must not regress to blanket E2-E4/E3-pending claims."""
    findings: list[str] = []
    for path in E3D_PUBLIC_PACKAGING_SURFACES:
        text = _read_text(path)
        rel = path.relative_to(ROOT).as_posix()
        for pattern in STALE_BLANKET_E2_E4_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                findings.append(f"{rel}: blanket E2-E4 claim: {match.group(0)}")
        for pattern in STALE_E3_PENDING_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                findings.append(f"{rel}: E3-pending claim: {match.group(0)}")
        lower = text.lower()
        if "full ars behavioral parity" in lower and "not" not in lower:
            # Require an explicit denial somewhere nearby for safety.
            if "not claimed" not in lower and "not full ars" not in lower:
                findings.append(f"{rel}: possible full ARS parity claim without denial")
    assert findings == [], "stale packaging claims found:\n" + "\n".join(findings)

    # Positive current-state anchors on key public pages.
    readme = _read_text(ROOT / "README.md").lower()
    assert "parity: partial" in readme
    assert "not_started" in readme
    start_here = _read_text(ROOT / "docs" / "START_HERE.html").lower()
    assert "parity: partial" in start_here
    assert "not_started" in start_here
    roadmap = _read_text(ROOT / "docs" / "ARCHITECTURE_ROADMAP.html").lower()
    assert "parity: partial" in roadmap
    assert "not_started" in roadmap
    return None

