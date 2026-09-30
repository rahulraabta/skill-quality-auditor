---
name: clean-skill
description: >
  A production-quality example skill that demonstrates best practices for
  Agent Skills. It includes verification steps, error handling, and safety
  guardrails so it can be used as a reference for testing the auditor.
---

# Clean Skill

## Description

This skill is a gold-standard reference for how a well-written Agent Skill
should be structured. It works across Claude Code, Codex, Cursor, and
Antigravity, and it demonstrates verification, error handling, and safety
guardrails in practice.

## Triggers

Use when you need a reference example of a properly structured Agent Skill.
Use during testing of the skill quality auditor. Use before building your
own skill to see the expected shape.

## How to Use It

1. Run the validation command to check the skill structure.
2. Execute the test suite to verify behavior.
3. Check the output for any errors and review the results.
4. Validate the results against expected values.

## Examples

Example 1: Run the validator on a well-structured skill:

```bash
python -m auditor.structural tests/fixtures/clean-skill



## Verification

Run the test suite with `pytest tests/` to verify everything works as
expected. The tests assert that each function returns the correct value.
Confirm the output matches the expected schema before proceeding.

## Error Handling

If the validation fails, check that all required sections are present. If
the test suite fails, review the error message and fix the exception. Handle
missing files gracefully and recover by re-running the command. If a step
fails, fall back to the manual verification procedure.

## Compatibility

This skill is tested with Claude Code, Codex, Cursor, and Antigravity.
It also works with GitHub Copilot and Windsurf.

## Safety

Warning: this skill performs read-only operations only. It does not
overwrite or delete any files. If you modify it to write files, back up
your work first and confirm each destructive operation before proceeding.