---
name: daily-manager
description: Use when capturing, updating, or reviewing the user's cross-project daily tasks through the daily-assistant Feishu-first workflow.
---

# Daily Manager

## Purpose

Use this skill when the user asks to record, track, update, or review a task that should live in the global daily task system rather than the current project.

Common triggers:

- "记一下"
- "挂到 daily manager"
- "开个任务"
- "这个之后提醒我"
- "把这个加到日常管理"
- "下次继续这个"

## Source Of Truth

The task state belongs in Feishu, not in the current repo.

Global Feishu location:

- Wiki entry: `https://www.feishu.cn/wiki/TwLCwijKki0Q9VkDiaMcP7GKnAg`
- Base name: `日常任务工作台`
- Base token: `F9p4bjm24axBY8sd8macJIySnYe`
- Table name: `任务`
- Table id: `tbldFwiuV4K0l2Lp`
- Views: `表格` and `看板`
- Card cover field: `封面` (attachment)
- External link fields: `外部链接 1`, `外部链接 2`, `外部链接 3` (URL text, one clickable external URL per field)
- Feishu links field: `飞书链接` (Feishu-internal URL; default empty)
- User input field: `用户原话`
- Import record field: `导入记录`
- Human notes field: `备注`
- Agent workspace field: `Agent 工作区`
- Local config: `/Users/xingminwang/Projects/daily-manager/config/lark_daily_workspace.json`

The daily-assistant repo stores:

- workflow docs
- scripts
- automation specs
- Feishu config
- this portable skill

When this skill is triggered from another repo, use the Feishu location above as the global task system. The current repo is only the source context.

## Capture Rules

When creating or updating a task, capture:

- task title
- current date and time
- current working directory
- git remote and branch, if available
- source project or document
- user-stated deadline or next follow-up time
- importance, if stated or clearly implied
- tags, if clear
- user input or close paraphrase
- import record from parsing, migration, or quick scan, when a scan is performed
- Agent workspace context for continuation
- next action

Do not guess deadlines, priority, or tags. If uncertain, leave the field blank or mention uncertainty in `Agent 工作区`.

When the user describes a project or code workspace but is uncertain about the exact repo or folder, locate candidates before writing final links:

- Search the likely local workspace first, especially the current repo, `/Users/xingminwang/Projects`, and user-stated folders such as `Projects/overleaf`.
- If the user asks to check GitHub, search the user's GitHub repositories after the local search.
- If exactly one strong candidate matches, write external repo/project links to `外部链接 1/2/3` and record the remaining uncertainty in `Agent 工作区`.
- If multiple plausible candidates remain, ask the user before writing a final workspace or repository link.

## Field Boundaries

- `用户原话`: Store the user's original wording or a close paraphrase of the request. Do not put Agent interpretation here.
- `导入记录`: Store only objective Agent import, parsing, migration, and quick-scan records. This field is Agent-authored but should read like evidence, not future planning.
- `备注`: Human notes area. Leave blank by default unless the user explicitly gives a note meant to remain as a human note.
- `Agent 工作区`: Store continuation context for future Agent work: current judgment, next-step decomposition, uncertainty, and task-specific working notes.

## Operating Modes

### Capture New Task

Use when the user describes a new thing to remember or track.

Default behavior:

1. Parse the user's description into the Feishu task fields.
2. Inspect lightweight project context when useful: `pwd`, git remote, branch, and obvious README/TODO files.
3. Ask only for fields that block a useful record.
4. Write the task to `日常任务工作台 / 任务`.
5. Put the user's wording in `用户原话`, objective parsing/quick-scan findings in `导入记录`, and continuation context in `Agent 工作区`.
6. Report what was recorded and which assumptions were made.

### Update Existing Task

Use when the user is continuing, revising, or adding context to an existing task.

Default behavior:

1. Search existing Feishu tasks by title, project source, repo URL, and tags.
2. Prefer updating an existing task over creating a duplicate.
3. Update `下一步动作`, `下一步时间`, `状态`, `导入记录`, `用户原话`, or `Agent 工作区` as appropriate. Use `备注` only for user-authored human notes.
4. If multiple likely matches exist, ask the user which one to update.

### Project Progress Snapshot

Use when the user asks to record current project progress, next steps, or where to continue later.

Default behavior:

1. Inspect current working directory.
2. Capture git remote, branch, status, and recent commit if available.
3. Read lightweight status files such as `README.md`, `TODO.md`, `todo.md`, or obvious project docs when present.
4. Summarize:
   - completed or current state
   - unresolved questions or blockers
   - next action
5. Update the matching Feishu task, or create one if no task exists.

Do not perform a deep codebase review unless the user explicitly asks for one.

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

Each external link field is a URL-style text field and should contain exactly one clickable URL. Put link roles such as `manuscript`, `code`, `data`, or `submission` in `导入记录` or `Agent 工作区`, not inside the URL field.

Do not write local filesystem paths into external link fields. If the task workspace is local, put the local path in `导入记录` or `Agent 工作区`, and use real external URLs in `外部链接 1/2/3` when they exist.

Use `飞书链接` only for Feishu-internal resources such as Feishu Drive folders, Feishu documents, wiki pages, Base record links, or other Feishu material entrances. Leave it empty by default. Do not auto-create a Feishu folder for every task. Do not put GitHub, Overleaf, submission-system, or web links in `飞书链接`.

Do not create a standalone task document for every small task. When long notes, drafts, materials, or multi-step continuation are needed, create or reuse a Feishu document from the location referenced by `飞书链接`.

Use `封面` only for card cover images. Feishu kanban card cover must be backed by an attachment field, so upload or generate a small image into `封面` when the user asks for task covers. Do not use `飞书链接` as a cover field.

When creating covers, prefer the built-in image generation model to make simple generated cartoon/illustration covers that match the task topic. Default to a 1:1 square image because Feishu mobile card previews crop wide images awkwardly. Avoid crude local placeholder graphics made only from flat colors and text unless the user explicitly wants a temporary placeholder. A cover task is not complete until the image is uploaded to the task's `封面` attachment field in Feishu.

## Effort Rules

`每周预计投入` is a number field measured in hours per week. Store only the numeric hour value. If the user says "每周一天", use `8` hours only when that conversion is reasonable, and record the conversion assumption in `导入记录`.

Attachment overwrite caveat: Feishu Base attachment fields cannot be overwritten through normal `record-upsert`; the upload shortcut may append instead of replacing. To replace a cover cleanly, either ask the user to clear the old attachment in the UI, use browser/UI automation with explicit permission, or create/switch to a fresh attachment field for the active `封面` field. Do not assume CLI permissions alone will make attachment overwrite possible.

## Safety

Ask before deleting task records or documents.

Read existing content before overwriting long notes.

Prefer updating an existing task over creating a duplicate when the user is clearly continuing the same work.
