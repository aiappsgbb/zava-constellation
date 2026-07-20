"""Contract tests for compose-org and research-company skills.

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


if __name__ == "__main__":
    unittest.main()
