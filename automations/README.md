# Automations

This directory is the repo source of truth for Agent-run daily work-item automations.

Codex automation definitions may live outside the repo under `~/.codex/automations/`, but their behavior should be mirrored here before it is treated as stable.

## Planned Automation Specs

- `daily-review.md`: produce a daily work-item brief from the Feishu `任务` table.
- `stale-task-review.md`: find open work items that have not been updated recently and recommend next actions.

## Rules

- Feishu Base `日常任务工作台` remains the business state source.
- This repo stores reproducible operating instructions, scripts, fixtures, and skill rules.
- Ambiguous inputs should be skipped or marked as uncertain, not guessed.
