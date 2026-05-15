# Scripts

This directory will hold executable helpers for the current Feishu workflow.

Planned scripts:

- `lark_create_task.py`: create one task in `日常任务工作台`.
- `lark_update_task.py`: update status, timeline, next action, notes, external links, Feishu link, import record, or Agent workspace.
- `lark_find_tasks.py`: search tasks by title, tag, status, source, or due date.

Scripts should read `config/lark_daily_workspace.json`, which should be created locally from `config/lark_daily_workspace.example.json` after the real Feishu Base is created.
