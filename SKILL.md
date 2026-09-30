---
name: skill-quality-auditor
description: >
  Audits any Agent Skill for security risks and quality issues, then explains
  findings in plain language. Works with Claude Code, Codex, Cursor, Antigravity.
---

# Skill Quality Auditor

## Description

A best-effort static analysis tool that scores Agent Skills on structure, security, and user-facing quality. It wraps NVIDIA SkillSpector for security, uses manifestspec for structure, and adds a custom six-dimension quality scorer.

## Triggers

Use when the user asks to audit a skill, check if a skill is safe, verify skill quality, or evaluate trustworthiness of a third-party skill.
Use before installing any skill from an untrusted source.
Use during CI to gate skill PRs on security and quality checks.

## How to Use It

1. Identify the path to the skill folder the user wants to audit.
2. Run the validate command to check structural integrity.
3. Execute the security scan to detect vulnerabilities.
4. Analyze the quality score across all six dimensions.
5. Review the findings and verify each one manually.
6. Generate the HTML report for a visual dashboard.
7. Create a summary with the top fix recommendation.
8. Confirm the final verdict before acting on it.

## Examples

Example 1: Audit a local skill folder.

    skill-auditor ./my-skill

Example 2: Generate HTML output.

    skill-auditor ./my-skill --html report.html

Example 3: Get JSON output for CI integration.

    skill-auditor ./my-skill --json

## Verification

Run pytest tests/ -v to verify behavior against three fixtures: clean, poor-quality, and malicious. Each test asserts a specific dimension and expects an exact score. Validate that the clean fixture passes and confirm the malicious fixture is flagged. Check that the output schema matches. All 8 tests must pass before publishing.

## Error Handling

If a skill folder does not contain SKILL.md, the structural auditor returns a MISSING_SKILL_MD error. If SkillSpector is not installed, the security auditor returns an install hint and continues. If any module throws an exception, the CLI prints the error to stderr and exits with a non-zero code. If a path does not exist, the tool fails fast with a clear message. If a scan times out, it aborts safely and emits a warning. Recover from any error by fixing the input and re-running. If a subprocess fails to launch, handle the FileNotFoundError and report a clear message. Check for fallback behavior when optional tools are missing.

## Safety

Warning: this tool performs best-effort static analysis and cannot detect all issues. A clean audit does not guarantee safety. Never install a skill without reviewing it manually. This tool is read-only and never executes target code. It does not delete, overwrite, or modify any files. Always backup your work before running automated tools. Confirm each finding manually before acting. Destructive operations are out of scope.
