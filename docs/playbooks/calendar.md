# Playbook · 日历

**场景**：查/建/改日程、查闲忙、会前准备。

## 前置检查

```bash
lark-cli auth status   # user identity 应为 ready
```

## 常用命令

```bash
# 今日日程
lark-cli calendar +agenda

# 指定日期（ISO 8601，注意时区）
lark-cli calendar +agenda --start "2026-08-22T00:00:00+08:00" --end "2026-08-22T23:59:59+08:00"

# 搜索日程（关键词 + 时间范围）
lark-cli calendar +search-event --query "面试" --start 2026-08-20 --end 2026-08-31

# 建日程（写操作：先向用户复述时间/标题/描述再执行）
lark-cli calendar +create \
  --summary "标题" \
  --start "2026-08-21T10:00:00+08:00" \
  --end "2026-08-21T11:00:00+08:00" \
  --description "备注，可放链接"

# 查闲忙（安排会议前用）
lark-cli calendar +freebusy --help
```

## 约定

- 腾讯会议的日程同步见 [tencent-meeting-sync.md](tencent-meeting-sync.md)。
- 建日程时飞书会自动挂一个飞书 VC 链接（vchat 字段）；若日程实际是外部会议，入会链接放 description 并注明以 description 为准。
- `search-event` 索引有延迟（新建后立刻搜可能搜不到），复核用 `+agenda` 按天查。
- 日历 ID：主日历 `feishu.cn_XDDZQjXHlFGXlSUtp07iIb@group.calendar.feishu.cn`（默认 primary，无需显式传）。
