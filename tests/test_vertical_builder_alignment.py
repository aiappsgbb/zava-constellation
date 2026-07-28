from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class TestVerticalBuilderAlignment(unittest.TestCase):
    def test_active_skills_share_current_substrate_contract(self):
        compose = (ROOT / "skills" / "compose-org" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        vertical = (
            ROOT
            / "skills"
            / "compose-org"
            / "references"
            / "vertical-pack-contract.md"
        ).read_text(encoding="utf-8")
        proof = (
            ROOT / "skills" / "compose-org" / "references" / "proof-contract.md"
        ).read_text(encoding="utf-8")
        research = (ROOT / "skills" / "research-company" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        airline = (
            ROOT
            / "skills"
            / "research-company"
            / "references"
            / "industry-primers"
            / "airline.md"
        ).read_text(encoding="utf-8")
        upstream = (
            ROOT / "skills" / "compose-org" / "references" / "upstream-pin.md"
        ).read_text(encoding="utf-8")

        assert "VERTICAL-BUILD-CONTRACT.md" in compose
        assert "read-only active-pack adapters" in compose
        assert "Global registries are extended additively" not in compose

        assert "automatically discovered" in vertical
        assert "read-only active-pack adapters" in vertical
        assert "domains are *registered* there" not in vertical
        assert "the pack adds entries" not in vertical
        for term in (
            "run_agent_session",
            "workflow identity",
            "HITL recovery context",
            "typed command",
            "projection",
        ):
            assert term in vertical

        assert "Contract version: `1.0.0`" in proof
        assert "when the workflow declares one" in proof
        assert "user-visible parity" in proof
        assert "Build ready" in proof
        assert "Demo ready" in proof

        assert "stop and write one first" not in research
        assert "return the gap to `compose-org`" in research

        assert "AGENTS.md" not in airline
        assert "## TODO" not in airline
        assert "Stub" not in airline
        assert "Unproven seed" in airline

        assert "api/shared/vertical_loader.py" in upstream
        assert "verticals/telco/manifest.py" in upstream
        assert "api/server/data_fabric/client_brand_gen.py" not in upstream


if __name__ == "__main__":
    unittest.main()
