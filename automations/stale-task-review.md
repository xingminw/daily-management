# Stale Work-Item Review Automation

## Goal

Find open work items that have not changed recently and recommend whether to continue, rewrite, wait, or close them.

## Default Rule

A work item is stale when:

- `状态 != 完成`
- and it has no recent `下一步时间`
- and its `Agent 工作区` does not show a clear current blocker

## Output

For each stale work item, summarize:

- work-item title
- current status
- source project
- why it appears stale
- recommended next action

Do not close work items automatically.
