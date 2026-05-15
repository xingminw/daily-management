# Agent Guide

## Role

This repo defines a Feishu-first daily work-item management workflow and keeps the Agent-facing rules needed to run it reproducibly.

The important boundary is:

```text
docs/ = current Feishu workflow and repo operating rules
automations/ = runnable Agent process specs for this workflow
skills/ = portable personal Feishu interface and daily work-item management behavior
scripts/ = executable tools for the current Feishu workflow
config/ = Feishu workspace configuration
```

## Source Of Truth

- Feishu is the source of truth for work-item state, notes, project links, and daily/weekly views.
- This repo is the source of truth for workflow rules, automation specs, scripts, configuration, and the local copy of the general daily-manager skill.
- `docs/` owns system/workflow documentation.
- `skills/` owns reusable personal Feishu interface, work-item capture, and work-item review behavior.

This repo's skills are personal global skills for this user's Feishu workspace. `skills/personal-feishu-interface` owns the user's broader Feishu placement rules: visible entries in `我的文档库`, backing storage in Drive, sticky notes, project notes, and cross-linking. `skills/daily-manager` owns the work-item Base and work-item-oriented progress sync. These skills may include concrete Feishu entrypoints and current field names so they can work from other projects without rediscovery. Keep lower-level CLI runbooks and repo maintenance rules in `docs/`, `automations/`, `scripts/`, or `config/`.

## Primary Objects

- Main tracker: `日常任务工作台` Base.
- Main work-item table: `任务` (historical table name; each row is a `工作项`).
- Recommended notes entry: `日常记录工作台`, visible from `我的文档库`.
- Notes are a separate subject in `日常记录工作台`; they can link to one or more work items.
- Config file: `config/lark_daily_workspace.json`.

## What The Agent Can Do

- Capture work items from the current conversation or project context.
- Capture daily notes, sticky notes, random ideas, meeting notes, and project notes into the appropriate visible Feishu entry when asked.
- Create or update Feishu work-item records through repo scripts.
- Link a work item to a project, file, document, email, meeting, or conversation summary.
- Maintain the work item's status, importance, timeline, tags, next action, external links, Feishu link, and Agent workspace.
- Summarize daily or weekly task state.
- Maintain repo docs, automation specs, scripts, config, and skill source when asked.

## What The Agent Should Not Do

- Do not make GitHub Issues the default daily work-item system.
- Do not create scattered work-item docs outside the configured Feishu workspace.
- Do not delete Feishu records, documents, or files without explicit confirmation.
- Do not overwrite long work-item notes or Feishu documents without reading the current content first.
- Do not over-model status. The default statuses are `待办`, `进行中`, `等待`, and `完成`.
- Do not silently invent deadlines, priority, or project links. Leave unknown fields blank or mark them as uncertain.

## Required References

For workflow or automation tasks, read:

- `README.md`
- `docs/feishu-workspace.md`
- `docs/workflow.md`
- `config/lark_daily_workspace.json`

For cross-project work-item capture, read:

- `skills/personal-feishu-interface/SKILL.md`
- `skills/daily-manager/SKILL.md`
