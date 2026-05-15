# Docs

这个目录描述当前 Feishu-first 日常任务管理系统怎么运行。

## 文档地图

- `feishu-workspace.md`：飞书 Base、字段、状态、视图和任务笔记区结构。
- `workflow.md`：任务捕获、写入、推进和回顾的端到端流程。

## 边界

`docs/` 解释当前系统工作流，面向人和 Agent。

`skills/` 提供跨项目可用的个人任务捕获与管理行为。当前 `daily-manager` skill 是用户个人全局 skill，可以保存具体飞书入口、Base token、表 ID 和字段名，以便其他项目会话直接写入同一个任务系统。底层 CLI runbook 和 repo 维护规则仍放在 `docs/`、`automations/`、`scripts/` 或 `config/`。
