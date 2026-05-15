# Automations

This directory is the repo source of truth for Agent-run daily task automations.

Codex automation definitions may live outside the repo under `~/.codex/automations/`, but their behavior should be mirrored here before it is treated as stable.

## Planned Automation Specs

- `daily-review.md`: produce a daily task brief from the Feishu task table.
- `stale-task-review.md`: find open tasks that have not been updated recently and recommend next actions.

## Rules

- Feishu Base `日常任务工作台` remains the business state source.
- This repo stores reproducible operating instructions, scripts, fixtures, and skill rules.
- Ambiguous inputs should be skipped or marked as uncertain, not guessed.
