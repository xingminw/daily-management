# Daily Review Automation

## Goal

Generate a concise daily work-item brief from `日常工作项`.

## Inputs

- Open work items where `状态 != 完成`.
- Work items with `下一步时间` today or earlier.
- Work items with `重要程度` equal to `P0` or `P1`.
- Work items in `等待` status that may need follow-up.

## Output

The brief should include:

1. 今日推进
2. 重要但未安排
3. 等待跟进
4. 建议关闭或改写的工作项

Do not mutate work-item records unless the user explicitly asks.
