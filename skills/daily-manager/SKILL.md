---
name: daily-manager
description: Use when managing the user's cross-project daily work items through the daily-assistant Feishu-first workflow, including creating, updating, completing, and syncing project progress.
---

# Daily Manager

## Purpose

Use this skill when the user asks to record, track, update, complete, or review a work item that should live in the global daily work management system rather than only in the current project.

A work item is something the user has decided to advance. It may be a paper, project, administrative matter, code effort, review, or other ongoing object. The Feishu table is still named `任务` for compatibility, but the Agent-facing concept is `工作项`.

Common triggers:

- "记一下"
- "挂到 daily manager"
- "开个工作项"
- "开个任务"
- "这个之后提醒我"
- "把这个加到日常管理"
- "下次继续这个"
- "把当前进度同步到 daily manager"
- "把这个 repo 和已有任务对上"
- "记录一下这个项目现在做到哪了"

## Source Of Truth

The work-item state belongs in Feishu, not in the current repo.

Global Feishu location:

- Wiki entry: `https://www.feishu.cn/wiki/TwLCwijKki0Q9VkDiaMcP7GKnAg`
- Base name: `日常工作项`
- Base token: `F9p4bjm24axBY8sd8macJIySnYe`
- Table name: `任务` (historical table name; treat each row as a `工作项`)
- Table id: `tbldFwiuV4K0l2Lp`
- Views: `表格` and `看板`
- Raw attachment field: `原始附件` (attachment; QR codes, screenshots, receipts, and source materials)
- External link fields: `外部链接 1`, `外部链接 2`, `外部链接 3` (URL text, one clickable external URL per field)
- Feishu links field: `飞书链接` (Feishu-internal URL; default empty)
- User input field: `用户原话`
- Human notes field: `备注`
- Agent workspace field: `Agent 工作区` (Agent-authored import, scan, progress, reasoning, uncertainty, and continuation context)
- Local config: `/Users/xingminwang/Projects/daily-manager/config/lark_daily_workspace.json`

The daily-assistant repo stores:

- workflow docs
- scripts
- automation specs
- Feishu config
- this portable skill

When this skill is triggered from another repo, use the Feishu location above as the global work-item system. The current repo is only the source context.

For broader Feishu placement decisions such as whether something belongs in work items, sticky notes, project notes, visible workspace entries, or backing Drive storage, use the `personal-feishu-interface` skill first. This skill only owns work-item records and work-item-oriented progress sync.

When the user explicitly says "记一个笔记", "记个想法", "记录一下", "随手记一下", or describes a loose thought, use `personal-feishu-interface` and write to `日常笔记 / Notes` instead of this work-item table. When the user says "记一个代办", "加个任务", "加个工作项", "这个要做", or gives a clear follow-up/deadline, use this work-item workflow. If the wording is ambiguous, ask whether it is a note or a work item.

## Capture Rules

When creating or updating a work item, capture:

- work-item title
- current date and time
- current working directory
- git remote and branch, if available
- source project or document
- user-stated deadline or next follow-up time
- importance, if stated or clearly implied
- tags, if clear
- user input or close paraphrase
- Agent workspace context from parsing, migration, quick scan, progress sync, and continuation notes
- next action

Do not guess deadlines, priority, or tags. If uncertain, leave the field blank or mention uncertainty in `Agent 工作区`.

Do not use this skill for pure sticky notes, random ideas, meeting fragments, or loose observations unless the user clearly wants to turn them into a work item. Those belong to the notes workflow and may link back to one or more work items.

When the user describes a project or code workspace but is uncertain about the exact repo or folder, locate candidates before writing final links:

- Search the likely local workspace first, especially the current repo, `/Users/xingminwang/Projects`, and user-stated folders such as `Projects/overleaf`.
- If the user asks to check GitHub, search the user's GitHub repositories after the local search.
- If exactly one strong candidate matches, write external repo/project links to `外部链接 1/2/3` and record the remaining uncertainty in `Agent 工作区`.
- If multiple plausible candidates remain, ask the user before writing a final workspace or repository link.

## Field Boundaries

- `用户原话`: Store the user's original wording or a close paraphrase of the request. Do not put Agent interpretation here.
- `备注`: Human notes area. Leave blank by default unless the user explicitly gives a note meant to remain as a human note.
- `Agent 工作区`: Store all Agent-authored working context: objective parsing, import/migration records, quick-scan evidence, current judgment, progress sync notes, next-step decomposition, uncertainty, and handoff notes for future Agent work.

Before updating `Agent 工作区` on an existing row, read the current field value and append or merge a dated section. Do not overwrite existing Agent context unless the user explicitly asks for replacement.

## Operating Modes

### Manage Work Item

Use when the user describes a new or existing thing to advance, track, update, complete, or continue later.

Default behavior:

1. Parse the user's description into the Feishu work-item fields.
2. Inspect lightweight project context when useful: `pwd`, git remote, branch, and obvious README/TODO files.
3. Ask only for fields that block a useful record.
4. Create or update the row in `日常工作项 / 任务`.
5. Put the user's wording in `用户原话` and all Agent-authored parsing/quick-scan/continuation context in `Agent 工作区`.
6. Report what was recorded and which assumptions were made.

When the user is continuing, revising, completing, or adding context to an existing work item:

1. Search existing Feishu rows by title, project source, repo URL, and tags.
2. Prefer updating an existing row over creating a duplicate.
3. Update `下一步动作`, `下一步时间`, `状态`, `用户原话`, or `Agent 工作区` as appropriate. Use `备注` only for user-authored human notes.
4. If multiple likely matches exist, ask the user which one to update.

### Match Project And Sync Progress

Use when the user asks to match the current work to an existing work item, record current project progress, update where a project stands, or save where to continue later from a different repo or conversation.

Default behavior:

1. Inspect current working directory.
2. Capture git remote URLs, branch, status, recent commit, and current directory path if available.
3. Read lightweight status files such as `README.md`, `TODO.md`, `todo.md`, AGENTS instructions, or obvious project docs when present.
4. Search Feishu work items for candidates by:
   - exact or normalized match between git remote URLs and `外部链接 1/2/3`
   - project/source/title match against `项目来源` and work-item title
   - mentions in `Agent 工作区`
   - compatible tags
5. Decide:
   - If exactly one strong candidate matches, update that work item.
   - If several plausible candidates remain, ask the user which one to use.
   - If none match, ask whether to create a new work item or leave the snapshot local to the conversation.
6. Read the existing `Agent 工作区`, then append or merge a dated progress section:
   - completed or current state
   - unresolved questions or blockers
   - next action
   - evidence inspected, such as cwd, branch, recent commit, or key files
   - continuation instructions for the next Agent
7. Update `下一步动作` and, only when clear, `状态`. Add newly discovered external URLs to empty `外部链接 1/2/3` slots when the match is strong.

Do not infer new deadlines, importance, or human notes from a project scan. Do not perform a deep codebase review unless the user explicitly asks for one.

## Notes Boundary

Sticky notes are separate first-class records, not subfields of work items.

- Use the notes workflow for random ideas, meeting fragments, observations, scratch thoughts, and non-actionable context.
- A note may link to zero, one, or many work items.
- A work item may accumulate many linked notes over time.
- Do not automatically turn a note into a work item. Do so only when the user explicitly asks or clearly gives an actionable object to advance.
- When a note provides useful progress context for an existing work item, add only a concise pointer or summary to `Agent 工作区`; keep the note itself in the notes system.

## Status Rules

Use only these default statuses:

- `待办`
- `进行中`
- `等待`
- `完成`

Use `Agent 工作区` for cancellation, pause, deferral, or uncertainty unless the workflow docs have been updated to add a new status. Keep `备注` as a human-authored notes field.

## Link And Folder Rules

Use `外部链接 1`, `外部链接 2`, and `外部链接 3` for Feishu-external entrances:

- GitHub repositories
- Overleaf projects and git remotes
- submission systems
- web pages
- other non-Feishu project URLs

Each external link field is a URL-style text field and should contain exactly one clickable URL. Put link roles such as `manuscript`, `code`, `data`, or `submission` in `Agent 工作区`, not inside the URL field.

Do not write local filesystem paths into external link fields. If the task workspace is local, put the local path in `Agent 工作区`, and use real external URLs in `外部链接 1/2/3` when they exist.

Use `飞书链接` only for Feishu-internal resources such as Feishu Drive folders, Feishu documents, wiki pages, Base record links, or other Feishu material entrances. Leave it empty by default. Do not auto-create a Feishu folder for every task. Do not put GitHub, Overleaf, submission-system, or web links in `飞书链接`.

Do not create a standalone document for every small work item. When long notes, drafts, materials, or multi-step continuation are needed, create or reuse a Feishu document from the location referenced by `飞书链接`.

Use `原始附件` for source materials such as QR codes, receipts, screenshots, forms, audio/video, and other files the user provides as evidence or operational material.

## Effort Rules

`每周预计投入` is a number field measured in hours per week. Store only the numeric hour value. If the user says "每周一天", use `8` hours only when that conversion is reasonable, and record the conversion assumption in `Agent 工作区`.

Attachment overwrite caveat: Feishu Base attachment fields cannot be overwritten through normal `record-upsert`; the upload shortcut may append instead of replacing. Do not assume CLI permissions alone will make attachment overwrite possible.

## Safety

Ask before deleting work-item records or documents.

Read existing content before overwriting long notes.

Prefer updating an existing work item over creating a duplicate when the user is clearly continuing the same work.
