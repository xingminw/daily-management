# 决策记录（decisions.md）

> 本文替代旧版 project-context.md（2026-08-19 前的评估框架文档）。
> 每条决策：结论 + 依据 + 日期。新决策追加在末尾。

## D1 · 钉钉不作为 AI 接入目标（2026-08-19）

**结论**：学校钉钉只用客户端手工操作，不追求 AI/Agent 接入。

**依据**：
- `dws auth login` 实测报错："您不在该组织的 CLI 授权人员范围内，请联系组织管理员将您加入授权名单"。
- WorkBuddy 钉钉 connector 检查其 cli.json：auth 字段即 `dws auth login -y`，同一套 OAuth，同一面墙。
- 官方 dingtalk-mcp 需要自建开发者 App 并由学校管理员审批装进组织——对新入职无话语权的用户不可行。
- 钉钉自定义机器人（Webhook）只能单向推消息/收消息，读不了日历/待办/邮件/通讯录，价值有限，暂不启用。

**影响**：学校考勤、审批、教务通知保持手工；这些本质是一次性人工判断，AI 不该代劳。

## D2 · 个人飞书 = AI 中枢（2026-08-19）

**结论**：日程、待办、云盘、文档、消息、笔记、（9月后）学校邮箱全部走个人飞书，经 lark-cli 操作。

**依据**：
- lark-cli 已认证（user + bot 双身份），21 个产品域。
- 列表级验证通过：日历（主日历可读写）、任务、云盘（既有工作流文件夹可见）。
- 与飞书 App 同账号同数据，AI 写入与手工操作天然同步。
- 唯一缺口：邮箱功能未开通（15180001）；base 域 scope 待补授权。

## D3 · 任务分层：工作项 ≠ 待办（2026-08-20）

**结论**：
| 层 | 载体 | 放什么 |
|---|---|---|
| 项目管理 | 日常工作项 Base（任务表） | 论文、项目、行政事项——要跨会话推进、进周报的 |
| 细碎小事 | 飞书待办（task app） | 半小时内一次性能干完的 |
| 笔记 | 素材笔记 Base | 想法、会议片段（独立主体，不并入工作项） |
| 日程 | 飞书日历 | 时间安排 |

**判断口诀**："这事会出现在周报里吗？会 → 工作项；不会 → 待办。"

**依据**：用户直觉 + daily-assistant 原设计兼容（其 workflow 的"工作项"本就面向论文/项目/行政级对象；本次把"短期任务级"明确剥离给飞书待办）。daytrace 的 insights 读的正是飞书任务层，两层各喂各的，无需改动。

## D4 · repo 定位：纯文档与配置，无代码（2026-08-19）

**结论**：repo 保存工作流规则、playbook、连接清单、决策记录、skill 源；不写适配器代码，不存凭据。工具层直接用现成 CLI（lark-cli / tmeet）。

**依据**：Codex 时期的 289 行评估文档 + 空代码骨架被证明是过度工程；真正的接入动作就是"CLI 认证 + 授权 scope"，不需要代码胶水。agent 可移植性由 AGENTS.md（跨 agent 标准入口）+ 纯 markdown 知识层保证。

## D5 · daily-assistant 并入本 repo；daytrace 只注册（2026-08-20）

**结论**：daily-assistant（纯文档规格 repo）以 git 历史嫁接方式合并进来，成为本 repo 的工作项管理工作流部分；daytrace 是跑在 Mac mini 的运行系统，只在 connections.yaml 注册 + playbooks 提供运维入口，不合并。

**依据**：两者同类（文档型）合并后单一 AGENTS.md 入口；daytrace 有自己的部署（launchd/SQLite/采集器），搬进文档 repo 会破坏其运行边界。

## D6 · SSD 由 exFAT 重灌为 APFS（2026-08-20）

**结论**：外接 SSD（1.8TB）格式化 APFS，纯 Mac 生态使用。

**依据**：实测小文件创建 exFAT 比 APFS 慢约 16 倍；exFAT 无 journaling 是"弹出后不识别"老毛病根源；exFAT 每文件 512KB~1MB 分配块（my-profile 129 个 552K 的文件占 153M）；`._*` AppleDouble 噪音。Windows 兼容已非真实需求。迁移前所有 repo 已推 GitHub + 双备份（Desktop/ssd 全量 + ~/SSD-backup-20260820）。

## D7 · 浙大邮箱接入：repo 内统一 wrapper，不走 connector（2026-08-21）

**结论**：浙大邮箱（@zju.edu.cn，Coremail 自建）通过本 repo `skills/zju-mail/` 的统一 wrapper（`zju_mail.py`，纯标准库，IMAP `imap.zju.edu.cn:993` / SMTP `smtp.zju.edu.cn:994`，SSL）接入；凭据只存 macOS Keychain（service `zju-mail`，account=邮箱地址）。

**依据**：
- 连接器市场无 Coremail/自建邮箱 connector（网易只管 163/126，腾讯系只管 QQ/腾讯企业邮）。
- 原计划首选"飞书邮箱挂外部账户"依赖腾讯托管假设，实测浙大是 Coremail 自建；且飞书个人版邮箱功能未开通（15180001），该路线暂缓（不废弃，开通后可再评估）。
- 浙大邮箱开标准 IMAP/SMTP，直连无障碍，邮件客户端同款协议。
- 用户明确要求代码集中进本 repo 成为一体 wrapper，不再散落别处；这是对 D4"不写适配器代码"的窄化修订：允许 skill 配套脚本进 repo，凭据仍永不进 repo。

**影响**：`skills/zju-mail/` 是唯一源，`scripts/sync_skills.sh` 同步到 codex/hermes/workbuddy 各 skill 目录（同步脚本改为拷贝整个 skill 目录）；发信须先向用户确认完整收件人/主题/正文（对齐 QQ 邮箱技能的两阶段确认规则）。

## D8 · wrapper 泛化为 personal-mail，QQ 邮箱双通道（2026-08-22）

**结论**：D7 的 zju wrapper 泛化为多邮箱统一 wrapper `skills/personal-mail/mail.py`（`-p zju|qq` 选邮箱，provider 配置内置，凭据按邮箱分存 Keychain：`zju-mail` / `qq-mail`）；`skills/zju-mail/` 退役。QQ 邮箱采用**双通道分工**：官方 connector（OAuth）管日常读/发/搜/附件/转发，wrapper 补 connector 没有的能力（draft 存草稿、mark 标签/星标/已读、任意文件夹访问、大附件发送——connector 限 3 附件共 3MB）。

**依据**：
- 用户要求 QQ 邮箱也能存草稿/打标签，而 QQ 官方 connector 工具集没有这些操作，文件夹也只暴露 inbox/sent/trash/spam 四个。
- QQ 邮箱支持标准 IMAP/SMTP（imap.qq.com:993 / smtp.qq.com:465 SSL），需网页端开启服务并用 16 位授权码（与浙大客户端专用密码同机制）。
- 复用同一个 wrapper 而非每个邮箱复制一份脚本，避免 500 行代码 ×N 份的维护负担；用户明确偏好"一体 wrapper，不要弄成别的"。

**影响**：QQ 授权码待用户网页端生成后存 Keychain service `qq-mail`，跑 `mail.py -p qq test` 收尾；zju 通道行为不变（回归通过）。浙大邮箱仍只有 wrapper 一条通道。
