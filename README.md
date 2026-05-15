# Daily Assistant

这是一个 Feishu-first 的日常任务管理与 Agent 协作仓库。

它的重点不是把任务写成本地 Markdown，也不是把 GitHub Issues 当作主任务系统，而是保存一套可复现的 Agent 能力：飞书工作台结构、任务捕获规则、自动化流程、脚本、配置和全局 skill。

## 核心关系

```text
飞书 = 日常任务状态和任务笔记的主工作台
人 = 最终判断者，负责决定优先级、时间线和取舍
Agent = 捕获上下文、创建任务、更新状态、整理每日/每周回顾
repo = Agent 能力和运行规范的来源
```

飞书中的 `日常任务工作台` Base 是任务入口。每条任务可以记录最多三个可点击外部链接；飞书内部材料入口只在确实存在时写入 `飞书链接`。

## 目录职责

- `AGENTS.md`：Agent 进入这个仓库时的快速规则。
- `docs/`：当前 Feishu-first 日常管理系统的工作流说明。
- `skills/`：跨项目可用的日常任务管理 skill。
- `automations/`：Agent 定时或触发式流程规范。
- `scripts/`：落实飞书操作的工具脚本。
- `config/`：飞书工作区配置模板和字段映射。

## 当前阶段

第一阶段先固定飞书工作台结构和 Agent 行为边界：

1. 使用一个全局 Base 管理任务状态。
2. 使用精简状态：`待办`、`进行中`、`等待`、`完成`。
3. 每条任务保留来源、时间线、重要程度、标签、外部链接、必要的飞书内部链接和下一步动作。
4. 通过全局 skill 让其他项目中的 Agent 会话也能把任务写回这里。

## 新会话入口

新的 Agent 会话应该先读：

1. `AGENTS.md`
2. `docs/feishu-workspace.md`
3. `docs/workflow.md`
4. 需要跨项目捕获任务时再读 `skills/daily-manager/SKILL.md`
