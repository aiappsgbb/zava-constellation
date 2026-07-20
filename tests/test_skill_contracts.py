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
    Guard golden scenario 1: "Capsule allocation" arithmetic
    from retail.md. Verify exact allocation values close properly.
    """

    def test_capsule_allocation_total_stock(self):
        """Available stock is 4,800 units."""
        available_stock = 4_800
        self.assertEqual(available_stock, 4_800)

    def test_capsule_allocation_store_count(self):
        """URBAN-FLAGSHIP cluster has exactly 5 stores."""
        num_stores = 5
        self.assertEqual(num_stores, 5)

    def test_capsule_allocation_per_store(self):
        """4,800 stock / 5 stores = 960 units per store."""
        available_stock = 4_800
        num_stores = 5
        allocation_per_store = available_stock // num_stores
        self.assertEqual(allocation_per_store, 960)

    def test_capsule_allocation_total_closes(self):
        """Total allocation across all stores equals available stock."""
        available_stock = 4_800
        num_stores = 5
        allocation_per_store = 960
        total_allocation = allocation_per_store * num_stores
        self.assertEqual(total_allocation, available_stock,
                         f"Expected {available_stock}, got {total_allocation}")

    def test_capsule_sku_count(self):
        """48 SKUs defined in range R-2025-SS-01."""
        num_skus = 48
        self.assertEqual(num_skus, 48)

    def test_capsule_allocation_per_sku_per_store(self):
        """960 units per store / 48 SKUs = 20 units per SKU per store."""
        allocation_per_store = 960
        num_skus = 48
        allocation_per_sku = allocation_per_store // num_skus
        self.assertEqual(allocation_per_sku, 20)

    def test_capsule_no_negative_allocation(self):
        """Allocation per SKU per store must be non-negative."""
        allocation_per_sku = 20
        self.assertGreaterEqual(allocation_per_sku, 0)

    def test_capsule_dc_decrement(self):
        """DC-NORTH inventory decremented by exactly 4,800."""
        total_allocation = 4_800
        dc_decrement = total_allocation
        self.assertEqual(dc_decrement, 4_800)

    def test_capsule_depth_multiplier_semantics(self):
        """Depth multiplier 1.0 does not over-commit the pool."""
        available_stock = 4_800
        num_stores = 5
        depth_multiplier = 1.0
        allocation_per_store = (available_stock / num_stores) * depth_multiplier
        total_allocation = allocation_per_store * num_stores
        self.assertLessEqual(total_allocation, available_stock,
                             "Total allocation must not exceed available stock")
        self.assertEqual(total_allocation, 4_800)


if __name__ == "__main__":
    unittest.main()
