"""Contract tests for compose-org, research-company, and zava-workspace-deploy skills.

Dependency-free: stdlib unittest only.
Validates that published skill prose matches the approved product contract.
"""

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPOSE_SKILL = ROOT / "skills" / "compose-org" / "SKILL.md"
COMPOSE_README = ROOT / "skills" / "compose-org" / "README.md"
COMPOSE_VERTICAL_CONTRACT = ROOT / "skills" / "compose-org" / "references" / "vertical-pack-contract.md"
COMPOSE_PROOF_CONTRACT = ROOT / "skills" / "compose-org" / "references" / "proof-contract.md"
RESEARCH_SKILL = ROOT / "skills" / "research-company" / "SKILL.md"
RESEARCH_README = ROOT / "skills" / "research-company" / "README.md"
RETAIL_PRIMER = ROOT / "skills" / "research-company" / "references" / "industry-primers" / "retail.md"


class TestComposeOrgPhaseHeadings(unittest.TestCase):
    """compose-org SKILL.md must contain all four exact phase headings."""

    def setUp(self):
        self.text = COMPOSE_SKILL.read_text()

    def test_phase_research(self):
        self.assertIn("## Phase Research", self.text)

    def test_phase_design(self):
        self.assertIn("## Phase Design", self.text)

    def test_phase_build(self):
        self.assertIn("## Phase Build", self.text)

    def test_phase_prove(self):
        self.assertIn("## Phase Prove", self.text)


class TestComposeOrgReferences(unittest.TestCase):
    """compose-org references research-company, proof doc, verticals dir, upstream."""

    def setUp(self):
        self.text = COMPOSE_SKILL.read_text()

    def test_invokes_research_company(self):
        self.assertIn("research-company", self.text)

    def test_references_vertical_proof(self):
        self.assertIn("docs/VERTICAL-PROOF.md", self.text)

    def test_references_verticals_slug(self):
        self.assertIn("verticals/", self.text)
        self.assertIn("<slug>", self.text)

    def test_references_upstream_remote(self):
        self.assertIn("upstream", self.text)

    def test_references_permanent_proof_command(self):
        # Must mention generating a permanent proof command
        self.assertRegex(self.text, r"(?i)permanent\s+proof\s+command")


class TestComposeOrgForbiddenPhrases(unittest.TestCase):
    """Old contract phrases must NOT appear in compose-org SKILL or README."""

    FORBIDDEN = [
        "literal find-and-replace",
        "stub=True",
        "25\u201335 domain stubs",
        "swap entity",
    ]

    def test_skill_no_forbidden(self):
        text = COMPOSE_SKILL.read_text()
        for phrase in self.FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_readme_no_forbidden(self):
        text = COMPOSE_README.read_text()
        for phrase in self.FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_skill_no_branded_fork_completion_claim(self):
        """Must not claim a branded fork IS completion."""
        text = COMPOSE_SKILL.read_text()
        # The old contract positioned 'branded fork' as the deliverable
        self.assertNotIn("branded fork is completion", text.lower())
        self.assertNotIn("the fork is the deliverable", text.lower())


class TestComposeOrgVerticalPackContract(unittest.TestCase):
    """references/vertical-pack-contract.md exists and lists surfaces."""

    def setUp(self):
        self.assertTrue(COMPOSE_VERTICAL_CONTRACT.exists(),
                        f"Missing {COMPOSE_VERTICAL_CONTRACT}")
        self.text = COMPOSE_VERTICAL_CONTRACT.read_text()

    def test_lists_pack_owned_surfaces(self):
        self.assertIn("verticals/", self.text)

    def test_no_global_replacement(self):
        # Must explicitly state no global registry replacement
        self.assertRegex(self.text, r"(?i)never.*(replac|overwrit).*global")


class TestComposeOrgProofContract(unittest.TestCase):
    """references/proof-contract.md mirrors VERTICAL-PROOF.md."""

    def setUp(self):
        self.assertTrue(COMPOSE_PROOF_CONTRACT.exists(),
                        f"Missing {COMPOSE_PROOF_CONTRACT}")
        self.text = COMPOSE_PROOF_CONTRACT.read_text()

    def test_references_vertical_proof_doc(self):
        self.assertIn("docs/VERTICAL-PROOF.md", self.text)

    def test_source_commit(self):
        self.assertRegex(self.text, r"(?i)(source.commit|commit.sha)")

    def test_evidence_manifest(self):
        self.assertRegex(self.text, r"(?i)evidence.manifest")

    def test_vertical_slug(self):
        self.assertIn("verticals/", self.text)


class TestResearchCompanyContract(unittest.TestCase):
    """research-company SKILL.md updated contract assertions."""

    def setUp(self):
        self.text = RESEARCH_SKILL.read_text()

    def test_compose_org_invokes_it(self):
        self.assertIn("compose-org", self.text)

    def test_facts_uncertainties(self):
        self.assertIn("facts", self.text.lower())
        self.assertIn("uncertainties", self.text.lower())

    def test_source_refs(self):
        self.assertRegex(self.text, r"(?i)source")

    def test_no_synthetic_actors(self):
        """Explicitly states it does not generate synthetic actors/records."""
        lower = self.text.lower()
        self.assertTrue(
            "does not generate synthetic" in lower
            or "never generate synthetic" in lower
            or "never creates synthetic" in lower
            or "does not create synthetic" in lower,
            "research-company must explicitly disclaim synthetic record generation"
        )


class TestRetailPrimer(unittest.TestCase):
    """Retail primer must be substantive, not a stub."""

    def setUp(self):
        self.text = RETAIL_PRIMER.read_text()
        self.lower = self.text.lower()

    def test_no_todo_stub(self):
        self.assertNotIn("TODO", self.text)
        self.assertNotIn("Stub", self.text)
        self.assertNotIn("stub", self.lower.split("unproven")[0] if "unproven" in self.lower else self.lower)

    def test_has_actors(self):
        # Must define actor/entity set
        for actor in ("customer", "store", "supplier", "product"):
            with self.subTest(actor=actor):
                self.assertIn(actor, self.lower)

    def test_has_causal_scenarios(self):
        self.assertRegex(self.text, r"(?i)causal")

    def test_has_process_families(self):
        self.assertRegex(self.text, r"(?i)process.famil")

    def test_has_typed_commands(self):
        self.assertRegex(self.text, r"(?i)typed.command")

    def test_has_deterministic_golden_scenarios(self):
        self.assertRegex(self.text, r"(?i)deterministic")
        self.assertRegex(self.text, r"(?i)golden")

    def test_has_proof_status_honesty(self):
        # Must label as unproven until clean compose-org run
        self.assertRegex(self.text, r"(?i)unproven")

    def test_has_distributions(self):
        self.assertRegex(self.text, r"(?i)distribut")


class TestRetailCapsuleAllocationArithmetic(unittest.TestCase):
    """
    Document-sensitive test: Extract Capsule allocation scenario
    from RETAIL_PRIMER and verify allocation arithmetic.
    Validates: per_store*stores == stock and per_sku*skus == per_store.
    """

    def setUp(self):
        import re
        self.text = RETAIL_PRIMER.read_text()

    def test_capsule_allocation_primer_math(self):
        """Extract and verify Capsule allocation scenario numbers from primer."""
        import re

        # Extract scenario block from golden scenario 1
        scenario_block = re.search(
            r"###\s+Golden scenario 1:.*?(?=###|$)",
            self.text,
            re.DOTALL | re.IGNORECASE
        )
        self.assertIsNotNone(scenario_block, "Golden scenario 1 not found in primer")
        scenario_text = scenario_block.group(0)

        # Extract available stock (handles commas)
        stock_match = re.search(r"(\d{1,3}(?:,\d{3})*)\s+units", scenario_text)
        self.assertIsNotNone(stock_match, "Available stock not found in scenario")
        available_stock = int(stock_match.group(1).replace(',', ''))

        # Extract store count (from "5 stores")
        store_match = re.search(r"(\d+)\s+stores", scenario_text)
        self.assertIsNotNone(store_match, "Store count not found in scenario")
        num_stores = int(store_match.group(1))

        # Extract SKU count (from "48 SKUs")
        sku_match = re.search(r"(\d+)\s+SKUs", scenario_text)
        self.assertIsNotNone(sku_match, "SKU count not found in scenario")
        num_skus = int(sku_match.group(1))

        # Extract per-store allocation (from "960 units per store")
        per_store_match = re.search(r"(\d{1,3}(?:,\d{3})*)\s+units\s+per\s+store", scenario_text)
        self.assertIsNotNone(per_store_match, "Per-store allocation not found in scenario")
        per_store = int(per_store_match.group(1).replace(',', ''))

        # Extract per-SKU-per-store allocation (from "20 units per SKU per store")
        per_sku_match = re.search(r"(\d+)\s+units\s+per\s+SKU\s+per\s+store", scenario_text)
        self.assertIsNotNone(per_sku_match, "Per-SKU-per-store allocation not found in scenario")
        per_sku = int(per_sku_match.group(1))

        # Verify arithmetic: per_store * stores == stock
        self.assertEqual(
            per_store * num_stores,
            available_stock,
            f"per_store ({per_store}) * stores ({num_stores}) = {per_store * num_stores}, "
            f"expected stock {available_stock}"
        )

        # Verify arithmetic: per_sku * skus == per_store
        self.assertEqual(
            per_sku * num_skus,
            per_store,
            f"per_sku ({per_sku}) * skus ({num_skus}) = {per_sku * num_skus}, "
            f"expected per_store {per_store}"
        )

        # Verify non-negative allocation
        self.assertGreaterEqual(per_sku, 0, "Per-SKU allocation must be non-negative")

        # Verify DC decrement claim (check for "decremented by 4,800" or "decremented by" language)
        dc_decrement_match = re.search(
            r"(?:decremented|decrement)\s+by\s+(\d{1,3}(?:,\d{3})*)\s+(?:total|units)?",
            scenario_text,
            re.IGNORECASE
        )
        if dc_decrement_match:
            dc_decrement = int(dc_decrement_match.group(1).replace(',', ''))
            self.assertEqual(
                dc_decrement,
                available_stock,
                f"DC decrement {dc_decrement} must equal available stock {available_stock}"
            )

        # Verify "no over-allocation" or "no negative allocation" language
        self.assertTrue(
            "no" in scenario_text.lower() and ("over-allocation" in scenario_text.lower() or "negative" in scenario_text.lower()),
            "Scenario should mention 'no over-allocation' or 'no negative allocation'"
        )


DEPLOY_SKILL = ROOT / "skills" / "zava-workspace-deploy" / "SKILL.md"


class TestDeploySkillVersion(unittest.TestCase):
    """Deploy skill must declare version 4.0.0."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_version_4(self):
        self.assertIn('version: "4.0.0"', self.text)


class TestDeploySkillModeGate(unittest.TestCase):
    """Must require explicit private-live or public-replay choice before Azure mutation."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_private_live_mode(self):
        self.assertIn("private-live", self.text)

    def test_public_replay_mode(self):
        self.assertIn("public-replay", self.text)

    def test_mode_choice_before_mutation(self):
        """Skill text must state mode choice is required before Azure mutation."""
        lower = self.text.lower()
        self.assertTrue(
            "before" in lower and ("azd" in lower or "mutation" in lower or "deploy" in lower),
            "Must require mode choice BEFORE any Azure mutation"
        )
        # Mode gate must be explicit
        self.assertRegex(self.text, r"(?i)choose|select|pick.*mode")


class TestDeploySkillProofManifest(unittest.TestCase):
    """Deploy skill must require a proof manifest with specific checks."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_proof_manifest_path(self):
        self.assertIn("proof/manifest.json", self.text)

    def test_source_commit_check(self):
        """Must verify git rev-parse HEAD equals manifest source_commit."""
        self.assertIn("source_commit", self.text)
        self.assertIn("git rev-parse HEAD", self.text)

    def test_vertical_match(self):
        """Must verify manifest vertical matches requested vertical."""
        self.assertIn("vertical", self.text.lower())
        self.assertRegex(self.text, r"(?i)manifest.*vertical|vertical.*manifest")

    def test_fingerprint_check(self):
        """Must verify fingerprint matches."""
        self.assertIn("fingerprint", self.text)

    def test_live_pass(self):
        """Must require live result PASS."""
        self.assertRegex(self.text, r"(?i)live.*PASS|live_result.*PASS")

    def test_replay_pass(self):
        """Must require replay result PASS."""
        self.assertRegex(self.text, r"(?i)replay.*PASS|replay_result.*PASS")

    def test_browser_errors_empty(self):
        """Must require browserErrors empty."""
        self.assertIn("browserErrors", self.text)
        self.assertRegex(self.text, r"(?i)browserErrors.*empty|\[\]")

    def test_fail_closed(self):
        """Proof must fail closed."""
        self.assertRegex(self.text, r"(?i)fail.closed|abort|exit 1")


class TestDeploySkillPrivateLiveMode(unittest.TestCase):
    """private-live mode: auth, Durable Functions, actor world, writable state, HITL."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_zava_mode_live(self):
        self.assertIn("ZAVA_MODE=live", self.text)

    def test_zava_vertical_env(self):
        self.assertIn("ZAVA_VERTICAL", self.text)

    def test_durable_functions_enabled(self):
        self.assertRegex(self.text, r"(?i)durable\s+functions.*enabled|functions\s+host")

    def test_actor_world_enabled(self):
        self.assertRegex(self.text, r"(?i)actor.world.*enabled|writable.*state")

    def test_authentication_required(self):
        self.assertRegex(self.text, r"(?i)auth.*required|authentication.*before.*ingress")

    def test_postdeploy_health_smoke(self):
        self.assertRegex(self.text, r"(?i)health")

    def test_postdeploy_workflow_smoke(self):
        self.assertRegex(self.text, r"(?i)workflow.*smoke|smoke.*workflow")

    def test_postdeploy_hitl_smoke(self):
        self.assertRegex(self.text, r"(?i)hitl|human.in.the.loop")

    def test_postdeploy_world_mutation_smoke(self):
        self.assertRegex(self.text, r"(?i)world.*mutation|mutation.*smoke")


class TestDeploySkillPublicReplayMode(unittest.TestCase):
    """public-replay mode: baked tape, read-only, no Functions, no actor world."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_zava_mode_replay(self):
        self.assertIn("ZAVA_MODE=replay", self.text)

    def test_baked_tape(self):
        self.assertRegex(self.text, r"(?i)baked\s+tape|tape.*path")

    def test_read_only_middleware(self):
        self.assertRegex(self.text, r"(?i)read.only.*middleware|middleware.*read.only")

    def test_functions_skipped(self):
        self.assertRegex(self.text, r"(?i)skip.*functions|functions.*disabled|no.*functions")

    def test_actor_world_disabled(self):
        self.assertRegex(self.text, r"(?i)actor.world.*disabled|world.*disabled")

    def test_postdeploy_replay_meta_smoke(self):
        self.assertRegex(self.text, r"(?i)replay.*meta|meta.*smoke")

    def test_postdeploy_read_only_rejection(self):
        self.assertRegex(self.text, r"(?i)read.only.*reject|write.*reject|405|403")

    def test_postdeploy_surfaces_smoke(self):
        self.assertRegex(self.text, r"(?i)surface.*smoke|smoke.*surface")


class TestDeploySkillNoStaleCounts(unittest.TestCase):
    """Must not quote stale fixed counts from old versions."""

    STALE_COUNTS = [
        "462 files",
        "38 domains",
        "48 routes",
        "46 tools",
        "62 graphs",
        "19 agents",
    ]

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_no_stale_counts(self):
        for count in self.STALE_COUNTS:
            with self.subTest(count=count):
                self.assertNotIn(count, self.text)


class TestDeploySkillAzdAcaPattern(unittest.TestCase):
    """Must use actual azd/ACA pattern from the repo."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_azd_up(self):
        self.assertIn("azd up", self.text)

    def test_container_apps(self):
        self.assertRegex(self.text, r"(?i)container\s*app")

    def test_bicep(self):
        self.assertIn("Bicep", self.text)


class TestDeploySkillTenantIsolation(unittest.TestCase):
    """Tenant isolation must link to aiappsgbb/awesome-gbb skill."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_references_awesome_gbb(self):
        self.assertIn("aiappsgbb/awesome-gbb", self.text)

    def test_revalidate_before_azd(self):
        """Must revalidate tenant immediately before azd up."""
        self.assertRegex(
            self.text,
            r"(?i)(revalidat|verify|check).*tenant.*before.*azd|"
            r"tenant.*(immediately|just)\s+before"
        )


class TestDeploySkillManifestCapabilities(unittest.TestCase):
    """Must introspect capabilities from manifest instead of fixed counts."""

    def setUp(self):
        self.text = DEPLOY_SKILL.read_text()

    def test_manifest_introspection(self):
        self.assertRegex(self.text, r"(?i)manifest.*capabilit|introspect|discover.*from.*manifest")

    def test_no_roadmap_section(self):
        """Must not contain stale roadmap section."""
        self.assertNotIn("### v11 roadmap", self.text)
        self.assertNotIn("### v10 roadmap", self.text)

    def test_frontmatter_description_practical_limit(self):
        """Frontmatter description must be under 500 chars (plugin practical limit)."""
        import re
        match = re.search(r"^---\n(.*?)^---", self.text, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, "Missing frontmatter")
        fm = match.group(1)
        desc_match = re.search(r"description:\s*>\n(.*?)(?=^\w|\Z)",
                               fm, re.MULTILINE | re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
        else:
            desc_match = re.search(r"description:\s*(.+)", fm)
            self.assertIsNotNone(desc_match, "Missing description")
            desc = desc_match.group(1).strip()
        self.assertLess(len(desc), 500,
                        f"Description too long ({len(desc)} chars)")


###############################################################################
# Task-8 public story contracts
###############################################################################

README_PATH = ROOT / "README.md"
ZAVA_MD_PATH = ROOT / "ZAVA.md"
PLUGIN_JSON_PATH = ROOT / "plugin.json"
DOCS_INDEX_PATH = ROOT / "docs" / "index.html"
EXPERIENCE_PATH = ROOT / "zava-experience.html"

PUBLIC_FILES = [README_PATH, ZAVA_MD_PATH, DOCS_INDEX_PATH, EXPERIENCE_PATH]


class TestPublicStoryPresence(unittest.TestCase):
    """Public files must mention compose-org, phases, deploy, and modes."""

    REQUIRED_TERMS = [
        "compose-org",
        "Research",
        "Design",
        "Build",
        "Prove",
        "zava-workspace-deploy",
        "private-live",
        "public-replay",
    ]

    def test_readme_contains_required_terms(self):
        text = README_PATH.read_text()
        for term in self.REQUIRED_TERMS:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_zava_md_contains_required_terms(self):
        text = ZAVA_MD_PATH.read_text()
        for term in self.REQUIRED_TERMS:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_docs_index_contains_required_terms(self):
        text = DOCS_INDEX_PATH.read_text()
        for term in self.REQUIRED_TERMS:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_experience_contains_required_terms(self):
        text = EXPERIENCE_PATH.read_text()
        for term in self.REQUIRED_TERMS:
            with self.subTest(term=term):
                self.assertIn(term, text)


class TestPublicStoryForbiddenPhrases(unittest.TestCase):
    """Public files must NOT advertise old contract language."""

    FORBIDDEN = [
        "research-company \u2192 compose-org",
        "research-company -> compose-org",
        "three-step",
        "three-skill",
        "three skills",
        "Three skills",
        "Three Copilot skills",
        "branded fork",
        "literal rebrand",
        "domain stubs",
        "swap entity kinds",
        "170 API routes",
        "170 routes",
        "37 domains",
        "37-domain",
        "12 operational",
        "25 strategic",
    ]

    def test_readme_no_forbidden(self):
        text = README_PATH.read_text()
        for phrase in self.FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_zava_md_no_forbidden(self):
        text = ZAVA_MD_PATH.read_text()
        for phrase in self.FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_docs_index_no_forbidden(self):
        text = DOCS_INDEX_PATH.read_text()
        for phrase in self.FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_experience_no_forbidden(self):
        text = EXPERIENCE_PATH.read_text()
        for phrase in self.FORBIDDEN:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


class TestPluginJsonTask8(unittest.TestCase):
    """plugin.json must be version 2.0.0 with updated description."""

    def setUp(self):
        import json
        self.data = json.loads(PLUGIN_JSON_PATH.read_text())

    def test_version_2(self):
        self.assertEqual(self.data["version"], "2.0.0")

    def test_description_mentions_compose_org(self):
        self.assertIn("compose-org", self.data["description"])

    def test_description_mentions_vertical(self):
        self.assertIn("vertical", self.data["description"].lower())

    def test_description_mentions_actor_world(self):
        desc = self.data["description"].lower()
        self.assertTrue(
            "actor world" in desc or "synthetic actor" in desc or "actor" in desc,
            "plugin description must mention actor world concept"
        )

    def test_description_no_three_skills(self):
        self.assertNotIn("three", self.data["description"].lower())

    def test_keywords_has_vertical(self):
        kw = [k.lower() for k in self.data.get("keywords", [])]
        self.assertTrue(any("vertical" in k for k in kw))


class TestHtmlFilesIdentical(unittest.TestCase):
    """docs/index.html and zava-experience.html must be byte-identical."""

    def test_byte_identical(self):
        a = DOCS_INDEX_PATH.read_bytes()
        b = EXPERIENCE_PATH.read_bytes()
        self.assertEqual(a, b, "docs/index.html and zava-experience.html must be byte-identical")


###############################################################################
# Cross-repo proof manifest path / schema alignment
###############################################################################

REQUIRED_PROOF_SCHEMA_KEYS = [
    "source_commit",
    "vertical",
    "fingerprint",
    "live_result",
    "replay_result",
    "browserErrors",
    "live_summary",
    "replay_summary",
]


class TestProofManifestPathAlignment(unittest.TestCase):
    """compose-org and deploy must agree on the canonical proof/manifest.json path."""

    def setUp(self):
        self.compose = COMPOSE_SKILL.read_text()
        self.deploy = DEPLOY_SKILL.read_text()

    def test_compose_skill_references_root_manifest(self):
        """Phase Prove must name the canonical proof/manifest.json at repo root."""
        self.assertIn("proof/manifest.json", self.compose)

    def test_compose_skill_no_verticals_proof_bundle(self):
        """Evidence bundle must not be placed under verticals/<slug>/proof/."""
        self.assertNotIn("verticals/<slug>/proof/", self.compose)

    def test_compose_and_deploy_same_manifest_path(self):
        """Both skills must reference the same canonical proof/manifest.json path."""
        self.assertIn("proof/manifest.json", self.compose)
        self.assertIn("proof/manifest.json", self.deploy)


class TestProofContractCanonicalPath(unittest.TestCase):
    """proof-contract.md must reference root proof/manifest.json, not a vertical-scoped path."""

    def setUp(self):
        self.text = COMPOSE_PROOF_CONTRACT.read_text()

    def test_root_manifest_path(self):
        """Evidence manifest must be at proof/manifest.json (repo root)."""
        self.assertIn("proof/manifest.json", self.text)

    def test_no_verticals_proof_path(self):
        """Must not place the evidence bundle under verticals/<slug>/proof/."""
        self.assertNotIn("verticals/<slug>/proof/", self.text)

    def test_no_wrong_manifest_filename(self):
        """Must not use the old standalone proof-manifest.json filename."""
        self.assertNotIn("proof-manifest.json", self.text)


class TestProofContractSchemaKeys(unittest.TestCase):
    """proof-contract.md schema must contain all keys required by the deploy skill."""

    def setUp(self):
        self.text = COMPOSE_PROOF_CONTRACT.read_text()

    def test_has_fingerprint(self):
        self.assertIn("fingerprint", self.text)

    def test_has_live_result(self):
        self.assertIn("live_result", self.text)

    def test_has_replay_result(self):
        self.assertIn("replay_result", self.text)

    def test_has_browser_errors(self):
        self.assertIn("browserErrors", self.text)

    def test_has_live_summary(self):
        self.assertIn("live_summary", self.text)

    def test_has_replay_summary(self):
        self.assertIn("replay_summary", self.text)


class TestProofContractNoDurableObject(unittest.TestCase):
    """proof-contract.md must reference Azure Durable Functions, not 'Durable Object'."""

    def setUp(self):
        self.text = COMPOSE_PROOF_CONTRACT.read_text()

    def test_no_durable_object(self):
        """Must not describe the orchestration step as a 'Durable Object'."""
        self.assertNotIn("Durable Object", self.text)

    def test_uses_azure_durable_functions(self):
        """Must explicitly reference Azure Durable Functions."""
        self.assertIn("Azure Durable Functions", self.text)


if __name__ == "__main__":
    unittest.main()
