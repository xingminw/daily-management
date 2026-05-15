# Agent Guide

## Role

This repo defines a Feishu-first daily task management workflow and keeps the Agent-facing rules needed to run it reproducibly.

The important boundary is:

```text
docs/ = current Feishu workflow and repo operating rules
automations/ = runnable Agent process specs for this workflow
skills/ = portable daily task management behavior
scripts/ = executable tools for the current Feishu workflow
config/ = Feishu workspace configuration
```

## Source Of Truth

- Feishu is the source of truth for task state, task notes, project links, and daily/weekly task views.
- This repo is the source of truth for workflow rules, automation specs, scripts, configuration, and the local copy of the general daily-manager skill.
- `docs/` owns system/workflow documentation.
- `skills/` owns reusable task-capture and task-review behavior.

This repo's `skills/daily-manager` skill is a personal global skill for this user's Feishu workspace. It may include the concrete Feishu entrypoint, Base token, table id, and current field names so the skill can work from other projects without rediscovery. Keep lower-level CLI runbooks and repo maintenance rules in `docs/`, `automations/`, `scripts/`, or `config/`.

## Primary Objects

- Main tracker: `日常任务工作台` Base.
- Main task table: `任务`.
- Optional note workspace: one Feishu document per task only when the task needs long notes.
- Config file: `config/lark_daily_workspace.json`.

## What The Agent Can Do

- Capture tasks from the current conversation or project context.
- Create or update Feishu task records through repo scripts.
- Link a task to a project, file, document, email, meeting, or conversation summary.
- Maintain the task's status, importance, timeline, tags, next action, external links, Feishu link, import record, and Agent workspace.
- Summarize daily or weekly task state.
- Maintain repo docs, automation specs, scripts, config, and skill source when asked.

## What The Agent Should Not Do

- Do not make GitHub Issues the default daily task system.
- Do not create scattered task docs outside the configured Feishu workspace.
- Do not delete Feishu records, documents, or files without explicit confirmation.
- Do not overwrite long task notes without reading the current content first.
- Do not over-model status. The default statuses are `待办`, `进行中`, `等待`, and `完成`.
- Do not silently invent deadlines, priority, or project links. Leave unknown fields blank or mark them as uncertain.

## Required References

For workflow or automation tasks, read:

- `README.md`
- `docs/feishu-workspace.md`
- `docs/workflow.md`
- `config/lark_daily_workspace.json`

For cross-project task capture, read:

- `skills/daily-manager/SKILL.md`
