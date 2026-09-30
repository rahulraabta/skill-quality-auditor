from pathlib import Path
from manifestspec import ManifestSpec, ValidationResult


class StructuralAuditor:
    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"

    def validate(self) -> dict:
        if not self.skill_md.exists():
            return {
                "valid": False,
                "errors": [{"code": "MISSING_SKILL_MD", "message": "SKILL.md not found"}],
                "warnings": [],
            }

        result: ValidationResult = ManifestSpec.from_skill_file(str(self.skill_md))

        return {
            "valid": result.is_valid,
            "errors": [{"code": e.code, "message": e.message} for e in result.errors],
            "warnings": [{"code": w.code, "message": w.message} for w in result.warnings],
        }


if __name__ == "__main__":
    import sys
    import json

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(StructuralAuditor(path).validate(), indent=2))