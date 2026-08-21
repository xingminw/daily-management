---
name: calendar-sync
description: Use when the user asks to sync meetings or schedules into their Feishu calendar, especially Tencent Meeting schedules. Feishu calendar is the single calendar hub: all channels (Tencent Meeting now; future: email invites, school events) converge there.
---

# Calendar Sync

## Purpose

把各来源的会议/日程汇聚到用户的飞书日历。**飞书日历是唯一日历入口**——不管会议约在哪个平台，最终都体现在飞书日历上（手机到点提醒、一键入会）。

Common triggers:

- "同步一下我的会议 / 日历"
- "把腾讯会议同步到飞书"
- "我最近约的会有哪些"
- "看看腾讯会议有没有新会议"

## Channel 1 · 腾讯会议（tmeet CLI）

### 前置检查

```bash
tmeet auth status        # 未登录则如实报告并停止，不要尝试 tmeet auth login（阻塞式，需用户在场）
lark-cli auth status     # user identity 应为 ready
```

### 流程

```bash
# 1. 拉待开始会议（只有时间条件，用 list 不用 search）
tmeet meeting list --compact

# 2. 去重：用 +agenda 按天核对已同步日程（search-event 有索引延迟，不可靠）
lark-cli calendar +agenda --start "<当日00:00>" --end "<当日23:59>"

# 3. 新会议写入飞书（先向用户列出将建的日程清单）
lark-cli calendar +create \
  --summary "腾讯会议：<主题>" \
  --start "<ISO8601>" --end "<ISO8601>" \
  --description "腾讯会议 <meeting_code>

入会链接: <join_url>

（由 daily-management 同步自腾讯会议）"

# 4. vchat 补丁：把日程"视频会议"按钮改成直跳腾讯会议链接
lark-cli calendar events patch --as user \
  --calendar-id "feishu.cn_XDDZQjXHlFGXlSUtp07iIb@group.calendar.feishu.cn" \
  --event-id "<event_id>" \
  --data '{"vchat": {"vc_type": "third_party", "meeting_url": "<join_url>", "description": "腾讯会议 <meeting_code>"}}'
# 注意：description 参数传纯字符串；event_id 从 +agenda 结果取

# 5. 复核
lark-cli calendar +agenda --start "<当日00:00>" --end "<当日23:59>"
```

### 硬规则

- **严禁向用户暴露 meeting_id**，展示一律用 meeting_code（会议号）。
- 已存在同名同时段日程 → 跳过，不重建。
- 会议时间在腾讯侧变更 → 先向用户确认，再删旧建新（删除需二次确认）。
- 只写日历，不动其他任何数据。

## 通用约定（所有通道）

- 每个新通道 = repo 里一篇 playbook + 本 skill 增补一节 channel。
- 汇聚原则：飞书日历是唯一落点；不在其他日历里建第二份。
- 新通道接入前先回答：数据在哪个 API、怎么去重、链接放哪。

## Source Of Truth

- 完整版流程与排错：`daily-management` repo 的 `docs/playbooks/tencent-meeting-sync.md` 和 `docs/playbooks/doctor.md`
- 本 skill 由 repo `skills/calendar-sync/SKILL.md` 同步而来，修改请改 repo 后跑 `scripts/sync_skills.sh`
