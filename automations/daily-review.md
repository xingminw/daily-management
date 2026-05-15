# Daily Review Automation

## Goal

Generate a concise daily task brief from `日常任务工作台`.

## Inputs

- Open tasks where `状态 != 完成`.
- Tasks with `下一步时间` today or earlier.
- Tasks with `重要程度` equal to `P0` or `P1`.
- Tasks in `等待` status that may need follow-up.

## Output

The brief should include:

1. 今日推进
2. 重要但未安排
3. 等待跟进
4. 建议关闭或改写的任务

Do not mutate task records unless the user explicitly asks.
