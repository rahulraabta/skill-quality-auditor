import shutil
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from auditor.structural import StructuralAuditor
from auditor.security import SecurityAuditor
from auditor.quality import QualityScorer


FIXTURES = Path(__file__).parent / "fixtures"


def test_clean_skill_is_structurally_valid():
    result = StructuralAuditor(FIXTURES / "clean-skill").validate()
    assert result["valid"] is True, f"Expected valid, got errors: {result['errors']}"
    assert result["errors"] == []


def test_clean_skill_has_no_security_findings():
    if not shutil.which("skillspector"):
        pytest.skip("skillspector not installed")
    result = SecurityAuditor(FIXTURES / "clean-skill").scan()
    assert result["total"] == 0, f"Expected 0 findings, got {result['total']}"


def test_clean_skill_scores_high_on_quality():
    result = QualityScorer(FIXTURES / "clean-skill").score()
    assert result["total_score"] >= 80, f"Expected >=80, got {result['total_score']}"
    assert result["verdict"] == "SAFE TO USE"


def test_malicious_skill_triggers_security_findings():
    if not shutil.which("skillspector"):
        pytest.skip("skillspector not installed")
    result = SecurityAuditor(FIXTURES / "malicious-skill").scan()
    assert result["total"] >= 5, f"Expected >=5 findings, got {result['total']}"
    assert result["recommendation"] == "DO_NOT_INSTALL"
    assert result["risk_severity"] == "CRITICAL"


def test_malicious_skill_scores_low_on_quality():
    result = QualityScorer(FIXTURES / "malicious-skill").score()
    assert result["total_score"] < 60, f"Expected <60, got {result['total_score']}"


def test_poor_quality_skill_scores_low():
    result = QualityScorer(FIXTURES / "poor-quality-skill").score()
    assert result["total_score"] < 70, f"Expected <70, got {result['total_score']}"
    assert result["verdict"] in ("DO NOT USE", "USE WITH CAUTION")


def test_missing_skill_md_returns_error(tmp_path):
    result = StructuralAuditor(tmp_path).validate()
    assert result["valid"] is False
    assert any(e["code"] == "MISSING_SKILL_MD" for e in result["errors"])


def test_nonexistent_path_for_quality_returns_zero(tmp_path):
    result = QualityScorer(tmp_path).score()
    assert result["total_score"] == 0.0
    assert result["verdict"] == "DO NOT USE"
