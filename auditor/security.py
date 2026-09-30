import json
import subprocess
from pathlib import Path


class SecurityAuditor:
    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path)

    def scan(self) -> dict:
        """Run SkillSpector in static-only mode (no LLM, no API key)."""
        try:
            result = subprocess.run(
                [
                    "skillspector", "scan", str(self.skill_path),
                    "--no-llm",
                    "--format", "json",
                ],
                capture_output=True,
                text=True,
                timeout=180,
            )
        except FileNotFoundError:
            return {
                "error": "SkillSpector not installed. Run: uv tool install git+https://github.com/NVIDIA/skillspector.git",
                "findings": [],
                "total": 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "error": "SkillSpector scan timed out",
                "findings": [],
                "total": 0,
            }

        # Extract JSON object from stdout (SkillSpector prints a text header first)
        stdout = result.stdout or ""
        json_start = stdout.find("{")
        if json_start == -1:
            return {
                "error": f"No JSON in output. stderr: {result.stderr[:200]}",
                "findings": [],
                "total": 0,
            }

        try:
            data = json.loads(stdout[json_start:])
        except json.JSONDecodeError as e:
            return {
                "error": f"Could not parse JSON: {e}",
                "raw_output": stdout[:500],
                "findings": [],
                "total": 0,
            }

        return self._normalize_findings(data)

    def _normalize_findings(self, raw: dict) -> dict:
        """Normalize SkillSpector output into a consistent format."""
        findings = []

        # SkillSpector v2.x native format: top-level "issues" array
        for issue in raw.get("issues", []):
            loc = issue.get("location") or {}
            location = loc.get("file", "unknown")
            start_line = loc.get("start_line")
            if start_line:
                location = f"{location}:{start_line}"

            findings.append({
                "rule_id": issue.get("id", "unknown"),
                "category": issue.get("category", "unknown"),
                "severity": (issue.get("severity") or "unknown").lower(),
                "message": issue.get("pattern") or issue.get("finding", ""),
                "detail": issue.get("explanation", ""),
                "remediation": issue.get("remediation", ""),
                "location": location,
                "confidence": issue.get("confidence", 0.0),
            })

        risk = raw.get("risk_assessment", {})

        return {
            "findings": findings,
            "total": len(findings),
            "risk_score": risk.get("score"),
            "risk_severity": risk.get("severity"),
            "recommendation": risk.get("recommendation"),
        }


if __name__ == "__main__":
    import sys

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(SecurityAuditor(path).scan(), indent=2))