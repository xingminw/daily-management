---
name: personal-feishu-interface
description: Use when deciding where to create, find, or link the user's personal Feishu work artifacts, including visible workspace entries, daily notes, project notes, task links, and backing Drive storage.
---

# Personal Feishu Interface

## Purpose

Use this skill when the user asks how to organize, create, find, or link personal work artifacts in Feishu.

This is the user's higher-level Feishu interface skill. It decides where an artifact should live and how it should connect to tasks, notes, projects, and files.

Common triggers:

- "放到飞书里"
- "这个应该在哪个工作区"
- "记个 random idea"
- "放到今天的 notes"
- "做个 sticky note"
- "这个和哪个项目关联"
- "给我整理一下飞书入口"
- "以后在不同项目里也能链接到这里"

## Operating Model

Feishu is the user's main personal work surface.

Use two layers:

- Visible entry layer: things the user should directly open from `我的文档库`.
- Backing storage layer: Feishu Drive folders for assets, attachments, generated files, raw materials, exports, and project files.

Do not make Drive folders the primary daily entry unless the user explicitly asks. The user-facing things should be visible as workspaces, docs, Bases, or index pages in `我的文档库`. Do not put visible workspace entrances or Drive shortcuts to those entrances inside backing storage folders.

## Current Known Entries

- `日常工作项`: visible Base entry for work items: projects, papers, administrative matters, code efforts, reviews, status, timeline, importance, next action, tags, external links, and Feishu links. The current table is named `任务`, but each row should be treated as a `工作项`.
  - Wiki entry: `https://www.feishu.cn/wiki/TwLCwijKki0Q9VkDiaMcP7GKnAg`
  - Base token: `F9p4bjm24axBY8sd8macJIySnYe`
  - URL: `https://my.feishu.cn/base/F9p4bjm24axBY8sd8macJIySnYe`
  - Main table: `任务` (`tbldFwiuV4K0l2Lp`)
- `日常笔记`: visible Base entry for sticky notes, daily notes, random ideas, meeting notes, and non-actionable work fragments.
  - Wiki entry: `https://my.feishu.cn/wiki/FQgUwvMx5iNAj0ktY8Vcvsb4nwf`
  - Wiki node token: `FQgUwvMx5iNAj0ktY8Vcvsb4nwf`
  - Base token: `FGyobSwcpaxVWjspWRRcs2xGnac`
  - Base URL: `https://my.feishu.cn/base/FGyobSwcpaxVWjspWRRcs2xGnac`
  - Main table: `Notes` (`tblvDv4i88wCOaAn`)
- Backing Drive folder: `日常管理材料` (`https://my.feishu.cn/drive/folder/Y8DkfIkNLlMfuhdIn31c6Mm4n2e`)
  - Work-item materials: `工作项材料` (`https://my.feishu.cn/drive/folder/Y1tefkAYXl8ZSXdYbJFc0HiDn7f`)
  - Notes materials: `笔记材料` (`https://my.feishu.cn/drive/folder/XZDKfLFr1lYkXFdjjdkcYTGZndc`)

The daily work-item system details live in `daily-manager`. Use that skill when the artifact is a work item, work-item update, project progress sync, or daily/weekly work-item review.

## Placement Rules

Choose the artifact type by intent:

- Work item or follow-up: write to `日常工作项`.
- Random idea, scratch note, meeting note, observation, reading note, or loose thought: write to `日常笔记`.
- Long project context, drafts, references, or multi-round notes for one project: create or update a project note/index and link it from relevant tasks.
- Files, images, exports, raw assets, and generated artifacts: store in Feishu Drive backing folders and link from the visible entry when useful.
- Workspace entrances or shortcuts: keep out of Drive backing folders; use `我的文档库` or the native Feishu document/wiki surface as the entrance.

Do not promote every note into a work item. Promote only when the user clearly asks or when there is already a clear object to advance with a next action, deadline, owner, or follow-up need.

## Adding New Areas

When adding a new repeated personal workflow in Feishu, follow the same light two-layer pattern unless the user explicitly asks otherwise:

- Create the user-facing entry in `我的文档库` or the native Feishu document/wiki surface.
- Keep backing files in a Drive materials folder: attachments, screenshots, audio/video, exports, and raw source files.
- Do not put the visible entry itself, or shortcuts to it, inside the backing Drive folder.
- Name the visible entry for the thing the user opens; name Drive folders for the materials they store.
- Keep the first version small: one visible entry and one backing materials area is usually enough.

## Notes Layer

Default notes organization should stay simple. The first version is a Base table, one note per record, not one document per day:

```text
日常笔记
  Notes
    全部记录
    今天
    Inbox
    按工作项
```

Fields:

```text
标题
日期
类型
标签
正文 / 用户原话
关联工作项
飞书链接
外部链接 1
外部链接 2
外部链接 3
原始附件
Agent 工作区
```

Note type options:

```text
idea
meeting
progress
reference
decision
question
personal
```

Use date grouping as a view or naming convention when useful, not as a required folder hierarchy.

Notes are first-class records, not subfields of work items. If a note becomes important to an existing work item, link the note to the work item. Add only a concise pointer or summary in the work item's `Agent 工作区`, or use `飞书链接` only when there is a stable Feishu note/index to link. Do not put many one-off note links directly into work-item fields.

Because notes and work items currently live in separate Bases, `关联工作项` is a text field in the first version. Store work-item titles and, when available, record links. Do not assume cross-Base record-link fields are available.

## Project Linking

Use a stable project note or project index as the Feishu-internal link target when a project needs internal material organization.

Recommended link direction:

- Work-item row `飞书链接` -> stable Feishu project note/index, not a random daily note.
- Project note/index -> relevant notes, meeting notes, files, and external project links.
- Note -> links to zero, one, or many work items when relevant.

For external systems such as GitHub, Overleaf, submission systems, and public webpages, use the work-item system's external link fields or clearly labeled links inside notes. Do not put external URLs into Feishu-internal link fields.

## Agent Behavior

When capturing a note:

1. Determine whether it is a work item, note, project note, or file/material.
2. If it is a loose thought, observation, meeting fragment, progress fragment, or random idea, default to notes.
3. If it relates to existing work items, link the note to those work items when possible; otherwise keep it standalone.
4. Do not convert a note into a work item unless the user explicitly asks or the user's intent is already clear.
5. Preserve the user's wording. Keep Agent interpretation separate and concise.

When organizing entries:

1. Keep visible workspaces few and stable.
2. Prefer one visible entry per repeated user workflow.
3. Use backing Drive folders for storage, not navigation.
4. Avoid scattered standalone docs without an index or visible entry.
5. Do not create Drive shortcuts for `日常工作项` or `日常笔记` inside backing folders.

## Safety

Ask before deleting or moving Feishu documents, folders, or Base records.

Read existing long notes before overwriting them.

If unsure whether something is a work item or note, capture it as a note first and mark possible next actions separately.
