# Daily Management

个人日常事务管理与外部工具连接中枢（原 daily-assistant 已于 2026-08-20 并入）。

**架构一句话**：个人飞书 = AI 中枢（经 lark-cli 操作），钉钉 = 仅客户端手工用，学校邮箱 9 月接入；本 repo 保存工作流规则、playbook、连接清单与决策记录——纯文档与配置，零代码，零凭据。

## 核心关系

```text
飞书 = 日常工作项 / 待办 / 素材笔记 / 日程 / 云档的主界面，唯一业务状态源
人 = 最终判断者，负责优先级、时间线和取舍
Agent = 捕获上下文、管理工作项与待办、记录 notes、同步日程、出每日摘要
repo = Agent 能力和运行规范的来源（任何 agent 读 AGENTS.md 即可接管）
```

## 任务分层（决策 D3）

| 层 | 载体 | 放什么 |
|---|---|---|
| 项目管理 | `日常工作项` Base | 跨会话推进、进周报的对象（论文/项目/行政事项） |
| 细碎小事 | 飞书待办（task） | 半小时内一次性能干完的事 |
| 笔记 | `素材笔记` Base | 想法、会议片段（独立主体） |
| 日程 | 飞书日历 | 时间安排（含腾讯会议同步） |

## 目录职责

- `AGENTS.md`：Agent 入口（任何 agent 框架自动读取）
- `docs/decisions.md`：决策记录——改架构前先读
- `docs/feishu-workspace.md` + `docs/workflow.md`：飞书组织结构与工作流
- `docs/playbooks/`：场景手册（日历/待办/邮箱/会议同步/每日摘要/诊断）
- `skills/`：跨项目 skill（daily-manager、personal-feishu-interface）
- `automations/`：定时/触发式流程规范
- `scripts/`：skill 同步等维护脚本
- `config/connections.yaml`：外部连接清单与健康检查
- `config/lark_daily_workspace.json`：真实 token 配置（gitignored）

## 新会话入口

1. `AGENTS.md`
2. `config/connections.yaml`（当前连了什么、什么状态）
3. 干具体活时按场景查 `docs/playbooks/`
4. 涉及工作项系统再读 `docs/workflow.md` + `skills/daily-manager/SKILL.md`
