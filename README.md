# Skill Quality Auditor

Audit any Agent Skill for security, structure, and user-facing quality with plain-English explanations.

## What It Checks

| Layer | Tool | What It Finds |
| :--- | :--- | :--- |
| Structural | manifestspec | Missing sections, bad frontmatter |
| Security | NVIDIA SkillSpector v2.12.0 | 71+ vulnerability patterns |
| Quality | Custom 6-dimension scorer | Clarity, workflow, verification, safety |

## Quick Start

    pip install -e .
    skill-auditor path/to/skill-folder

## Example Output

    STRUCTURAL: valid
    SECURITY: 0 findings (Risk: LOW)
    QUALITY: 84.3/100 (SAFE TO USE)
    OVERALL: SAFE TO USE

## JSON Output

    skill-auditor path/to/skill-folder --json

## Quality Dimensions

| Dimension | Weight |
| :--- | :--- |
| Description clarity | 15% |
| Workflow structure | 20% |
| Verification presence | 20% |
| Error handling | 15% |
| Compatibility | 10% |
| Safety guardrails | 20% |

## Verdicts

- SAFE TO USE: valid structure, no critical findings, quality 80 or higher
- USE WITH CAUTION: minor issues present
- DO NOT USE: critical security or structural problems

## Development

    pip install -e ".[dev]"
    pytest tests/ -v

## License

Apache-2.0 -- see LICENSE.

## Disclaimer

This tool performs best-effort static analysis. It cannot detect all security vulnerabilities or quality issues. A clean audit does not guarantee a skill is safe. Always review third-party skills before installing.
