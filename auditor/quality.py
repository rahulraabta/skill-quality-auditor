import re
from pathlib import Path


class QualityScorer:
    """Score a skill on six user-centric quality dimensions."""

    WEIGHTS = {
        "description_clarity": 0.15,
        "workflow_structure": 0.20,
        "verification_presence": 0.20,
        "error_handling": 0.15,
        "compatibility": 0.10,
        "safety_guardrails": 0.20,
    }

    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.content = (
            self.skill_md.read_text(encoding="utf-8")
            if self.skill_md.exists()
            else ""
        )

    def score(self) -> dict:
        dimensions = {
            "description_clarity": self._score_description(),
            "workflow_structure": self._score_workflow(),
            "verification_presence": self._score_verification(),
            "error_handling": self._score_error_handling(),
            "compatibility": self._score_compatibility(),
            "safety_guardrails": self._score_safety(),
        }

        total = sum(dimensions[k] * self.WEIGHTS[k] for k in dimensions)

        return {
            "total_score": round(total, 1),
            "dimensions": {k: round(v, 1) for k, v in dimensions.items()},
            "verdict": self._verdict(total),
        }

    def _score_description(self) -> float:
        """Score description clarity (0-100)."""
        match = re.search(
            r"description:\s*[>|]?\s*\n?(.*?)(?=\n\w|\n---|$)",
            self.content,
            re.DOTALL,
        )
        if not match:
            return 0.0
        desc = match.group(1).strip()
        if len(desc) < 20:
            return 20.0
        if len(desc) > 1024:
            return 40.0
        sentences = len(re.findall(r"[.!?]+", desc)) or 1
        words = len(desc.split())
        avg_words = words / sentences
        if avg_words < 15:
            return 100.0
        elif avg_words < 25:
            return 70.0
        return 40.0

    def _score_workflow(self) -> float:
        numbered = len(re.findall(r"^\s*\d+\.\s", self.content, re.MULTILINE))
        action_verbs = len(
            re.findall(
                r"\b(?:run|execute|check|validate|create|update|scan|analyze|"
                r"generate|write|read|install|configure|verify)\b",
                self.content,
                re.IGNORECASE,
            )
        )
        return float(min(100, numbered * 12 + action_verbs * 3))

    def _score_verification(self) -> float:
        patterns = [r"\btest\b", r"\bverify\b", r"\bvalidate\b", r"\bcheck\b",
                    r"\bassert\b", r"\bexpect\b", r"\bconfirm\b"]
        matches = sum(len(re.findall(p, self.content, re.IGNORECASE)) for p in patterns)
        return min(100.0, matches * 15.0)

    def _score_error_handling(self) -> float:
        patterns = [r"\berror\b", r"\bfail\b", r"\bexception\b", r"\bfallback\b",
                    r"\bif.*not.*found\b", r"\bhandle\b", r"\brecover\b"]
        matches = sum(len(re.findall(p, self.content, re.IGNORECASE)) for p in patterns)
        return min(100.0, matches * 12.0)

    def _score_compatibility(self) -> float:
        agents = ["claude", "codex", "cursor", "antigravity", "copilot",
                  "windsurf", "gemini"]
        found = sum(1 for a in agents if a.lower() in self.content.lower())
        return min(100.0, found * 25.0)

    def _score_safety(self) -> float:
        patterns = [r"\bcaution\b", r"\bwarning\b", r"\bdestructive\b",
                    r"\bdelete\b", r"\boverwrite\b", r"\bconfirm\b", r"\bbackup\b"]
        matches = sum(len(re.findall(p, self.content, re.IGNORECASE)) for p in patterns)
        return min(100.0, matches * 12.0)

    def _verdict(self, score: float) -> str:
        if score >= 80:
            return "SAFE TO USE"
        elif score >= 50:
            return "USE WITH CAUTION"
        return "DO NOT USE"


if __name__ == "__main__":
    import json
    import sys

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(QualityScorer(path).score(), indent=2))