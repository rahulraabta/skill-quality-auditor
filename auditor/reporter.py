from pathlib import Path
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .explainer import explain_finding


TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def compute_summary(report: dict) -> dict:
    sec = report.get("security", {})
    qual = report.get("quality", {})

    findings = sec.get("findings", [])
    high_findings = [f for f in findings if f.get("severity") == "high"]

    if high_findings:
        top = high_findings[0]
        top_fix = f"Fix the high-severity issue: {top['message']} ({top['location']})"
        summary = f"This skill has {len(high_findings)} high-severity security problem(s). Do not install until they are fixed."
    elif findings:
        top = findings[0]
        top_fix = f"Review the {top['severity']}-severity issue: {top['message']} ({top['location']})"
        summary = f"This skill has {len(findings)} security finding(s) of medium or low severity."
    elif qual.get("total_score", 0) < 80:
        top_fix = "Improve documentation: add verification steps, error handling, and safety guardrails."
        summary = f"No security issues, but quality score is {qual['total_score']}/100."
    else:
        top_fix = "No action needed."
        summary = "This skill passed all checks."

    return {"summary": summary, "top_fix": top_fix, "high_count": len(high_findings), "total_findings": len(findings)}


def render_html_report(report: dict, output_path: Path) -> Path:
    """Render a dict report to a standalone HTML file."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report.html.j2")

    for f in report.get("security", {}).get("findings", []):
        f["explanation"] = explain_finding(f.get("rule_id", ""))

    summary = compute_summary(report)

    html = template.render(
        summary=summary,
        report=report,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    output_path = Path(output_path)
    output_path.write_text(html, encoding="utf-8")
    return output_path
