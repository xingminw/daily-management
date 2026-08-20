# Playbook · 待办（细碎小事层）

**场景**：半小时内一次性能干完的小事——回邮件、交表、查数据、传文件。
**边界**：会出现在周报里的、要跨会话推进的，去日常工作项 Base（见 [../workflow.md](../workflow.md)），不进待办。

## 前置检查

```bash
lark-cli auth status   # task 域 scope 应已授予
```

## 常用命令

```bash
# 任务清单列表
lark-cli task tasklists list

# 查任务（shortcut 优先，--help 看参数）
lark-cli task +list --help

# 建任务（写操作）
lark-cli task +create --help

# 完成任务
lark-cli task +complete --help
```

## 分层规则（决策 D3）

| 判断 | 去处 |
|---|---|
| 会出现在周报里？跨会话推进？有项目来源？ | 日常工作项 Base（任务表） |
| 半小时一次性干完？不值得建项目？ | 飞书待办 |
| 只是想法/片段/记录，不是要推进的事？ | 素材笔记 Base |

工作项与待办可以互指：工作项的 `Agent 工作区` 里可写"碎事见待办 xxx"，但不强制。
