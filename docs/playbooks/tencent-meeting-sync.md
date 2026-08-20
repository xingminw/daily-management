# Playbook · 腾讯会议 → 飞书日历同步

**场景**：把腾讯会议里约的会同步成飞书日程（2026-08-20 首次跑通）。

## 前置检查

```bash
tmeet auth status        # AccessToken ~6h 过期，过期则 tmeet auth login（阻塞式，前台跑）
lark-cli auth status     # 日历写权限
```

## 流程

```bash
# 1. 拉取待开始的会议（只有时间条件，用 list 不用 search）
tmeet meeting list --compact

# 2. 去重：查飞书对应日期段是否已有同名日程
lark-cli calendar +search-event --start <日期> --end <日期+1>
# 注意：search-event 有索引延迟，去重后复核用 +agenda

# 3. 逐个写入飞书（写操作，先向用户列出将建的日程清单）
lark-cli calendar +create \
  --summary "腾讯会议：<主题>" \
  --start "<ISO8601>" --end "<ISO8601>" \
  --description "腾讯会议 <meeting_code>

入会链接: <join_url>

（由 daily-management 同步自腾讯会议）"

# 4. （推荐）把日程的视频会议入口替换成腾讯会议链接
# +create 会自动挂一个飞书 VC（vc.feishu.cn/j/...），且 vchat:null 删不掉。
# 正确解法：events patch 改成 third_party 类型，日历上的"视频会议"按钮直接跳腾讯会议：
lark-cli calendar events patch --as user \
  --calendar-id "<organizer_calendar_id>" --event-id "<event_id>" \
  --data '{"vchat": {"vc_type": "third_party", "meeting_url": "<join_url>", "description": "腾讯会议 <meeting_code>"}}'

# 5. 复核
lark-cli calendar +agenda --start "<当日00:00>" --end "<当日23:59>"
```

## 约定

- 描述里必须含会议号（meeting_code）和入会链接（join_url）；**严禁出现 meeting_id**（隐私字段）。
- 第 4 步执行后，日程的视频会议入口即腾讯会议；未执行时飞书自动附带的 VC 链接不是入会入口，认 description 里腾讯链接。
- 会议时间变更：tmeet 侧改完后，删除旧日程（需用户确认）再重建，或直接 `calendar +update`。
- 已结束会议的录制/纪要查询：先读 tmeet skill 的 references/tmeet-record.md（路由规则复杂）。
