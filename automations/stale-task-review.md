# Stale Task Review Automation

## Goal

Find open tasks that have not changed recently and recommend whether to continue, rewrite, wait, or close them.

## Default Rule

A task is stale when:

- `状态 != 完成`
- and it has no recent `下一步时间`
- and its `导入记录` / `Agent 工作区` do not show a clear current blocker

## Output

For each stale task, summarize:

- task title
- current status
- source project
- why it appears stale
- recommended next action

Do not close tasks automatically.
