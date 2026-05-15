# Docs

这个目录描述当前 Feishu-first 日常工作项管理系统怎么运行。

## 文档地图

- `feishu-workspace.md`：飞书 Base、字段、状态、视图、工作项和个人可见入口结构。
- `workflow.md`：工作项捕获、写入、推进、同步和回顾的端到端流程。

## 边界

`docs/` 解释当前系统工作流，面向人和 Agent。

`skills/` 提供跨项目可用的个人飞书接口、工作项捕获与管理行为。`personal-feishu-interface` 记录用户如何把飞书作为个人工作系统入口；`daily-manager` 记录工作项 Base 的具体写入规则。个人全局 skill 可以保存具体飞书入口、Base token、表 ID 和字段名，以便其他项目会话直接写入同一个系统。底层 CLI runbook 和 repo 维护规则仍放在 `docs/`、`automations/`、`scripts/` 或 `config/`。
