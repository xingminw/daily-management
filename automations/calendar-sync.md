# Automation · calendar-sync（会议日程汇聚到飞书日历）

> 2026-08-21 创建。运行实例已注册为 WorkBuddy 定时任务（每日 08:30）。
> 本文件是 repo 侧的规范记录：改这里 + 改 WorkBuddy 任务，两边保持一致。

## 汇聚原则

**飞书日历是唯一日历入口。** 所有来源的会议/日程最终都写进飞书主日历：

```
腾讯会议（tmeet）──┐
                   ├──►  飞书日历（唯一落点）
未来：邮件邀请 ─────┤
未来：学校日程搬运 ─┘
```

## 运行定义

| 项 | 值 |
|---|---|
| 触发 | 每日 08:30（WorkBuddy automation）+ 用户随口一提（on-demand，见 skills/calendar-sync） |
| 工作目录 | daily-management repo |
| 执行内容 | 按 `docs/playbooks/tencent-meeting-sync.md` 跑一遍腾讯会议→飞书同步 |
| 通知 | 有新会议同步/有异常时在会话中汇报；无新会议则简单说"无新增" |

## 通道清单

| 通道 | 状态 | 数据源 | playbook |
|---|---|---|---|
| 腾讯会议 | ✅ 运行中 | `tmeet meeting list` | docs/playbooks/tencent-meeting-sync.md |
| 邮件邀请 | ⏸ 待邮箱开通（9 月） | 飞书邮箱 API | 待写 |
| 学校钉钉日程 | ⏸ 手动搬运（钉钉 API 被组织墙挡） | 无 API，人工 | 不做 |

## 增加新通道的步骤

1. 在 `docs/playbooks/` 写该通道的 playbook（数据在哪个 API、怎么去重、链接放哪）
2. 在 `skills/calendar-sync/SKILL.md` 增补一节 channel
3. 本文件通道清单加一行
4. 跑 `scripts/sync_skills.sh` 同步技能
5. 若需要提高同步频率，改 WorkBuddy 任务的 schedule

## 已知边界

- tmeet AccessToken 约 6h 过期；automation 跑时若发现未登录，如实报告并停止（不尝试登录，用户在场才能授权）
- search-event 有索引延迟，去重一律用 `+agenda` 按天查
- 当天临时约的会不等定时任务，用户说一声就手动触发
