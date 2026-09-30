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

1. Identify the path to the skill folder the user wants audited.
2. Run skill-auditor with the path to generate the report.
3. Review the STRUCTURAL, SECURITY, and QUALITY sections.
4. Present the overall verdict and any critical findings.

## Examples

Example 1: Audit a local skill folder.

    skill-auditor ./my-skill

Example 2: Get JSON output for CI.

    skill-auditor ./my-skill --json

## Verification

Run pytest tests/ -v to verify behavior against three test fixtures. All 8 tests must pass before publishing changes.

## Error Handling

If a skill folder does not contain SKILL.md, the structural auditor returns a MISSING_SKILL_MD error. If SkillSpector is not installed, the security auditor returns an install hint.
