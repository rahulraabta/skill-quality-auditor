import argparse
import json
import sys
from pathlib import Path

from .structural import StructuralAuditor
from .security import SecurityAuditor
from .quality import QualityScorer


def run_audit(path):
    return {
        "skill_path": str(path),
        "structural": StructuralAuditor(path).validate(),
        "security": SecurityAuditor(path).scan(),
        "quality": QualityScorer(path).score(),
    }


def print_human_report(report):
    print("=" * 60)
    print("  Skill Quality Audit: " + report["skill_path"])
    print("=" * 60)
    s = report["structural"]
    print("")
    print("STRUCTURAL: " + ("Valid" if s.get("valid") else "Invalid"))
    for e in s.get("errors", []):
        print("  ERROR [" + e["code"] + "] " + e["message"])
    for w in s.get("warnings", []):
        print("  WARN  [" + w["code"] + "] " + w["message"])
    sec = report["security"]
    total = sec.get("total", 0)
    print("")
    print("SECURITY: " + str(total) + " finding(s)")
    if sec.get("recommendation"):
        print("  Recommendation: " + sec["recommendation"])
    for f in sec.get("findings", []):
        print("  [" + f["severity"].upper() + "] " + f["rule_id"] + " " + f["message"])
    q = report["quality"]
    print("")
    print("QUALITY: " + str(q["total_score"]) + "/100 - " + q["verdict"])
    for dim, score in q["dimensions"].items():
        print("  " + dim + ": " + str(score))
    print("")
    print("=" * 60)
    structural_ok = s.get("valid", False)
    security_ok = total == 0 or sec.get("recommendation") != "DO_NOT_INSTALL"
    quality_ok = q["total_score"] >= 80
    if structural_ok and security_ok and quality_ok:
        print("  OVERALL: SAFE TO USE")
    elif structural_ok and not security_ok:
        print("  OVERALL: DO NOT USE (security issues)")
    else:
        print("  OVERALL: USE WITH CAUTION")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Audit an Agent Skill.")
    parser.add_argument("path", type=Path, help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--html", type=Path, help="Write HTML report to this file")
    args = parser.parse_args()

    if not args.path.exists():
        print("Error: path does not exist", file=sys.stderr)
        sys.exit(1)

    report = run_audit(args.path)

    if args.json:
        print(json.dumps(report, indent=2))
    elif args.html:
        from .reporter import render_html_report
        out = render_html_report(report, args.html)
        print("HTML report written to: " + str(out))
    else:
        print_human_report(report)


if __name__ == "__main__":
    main()
