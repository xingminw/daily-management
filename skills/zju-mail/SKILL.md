---
name: zju-mail
description: "浙大邮箱(@zju.edu.cn)操作技能。触发场景：看浙大邮箱、查浙大邮件、学校邮箱有没有新邮件、用浙大邮箱发邮件/回复邮件、下载浙大邮件附件、搜索浙大邮箱。通过 IMAP/SMTP wrapper（zju_mail.py）操作，凭据存 macOS Keychain。关键词：浙大邮箱、学校邮箱、zju.edu.cn、zju mail。"
---

# ZJU Mail Skill (zju-mail)

通过本 skill 目录下的 `zju_mail.py`（纯标准库 Python，零依赖）操作浙大邮箱。
浙大邮箱为 Coremail 自建系统：IMAP `imap.zju.edu.cn:993`，SMTP `smtp.zju.edu.cn:994`，均 SSL。

源文件在 daily-management repo：`/Volumes/My SSD/Codespace/daily-management/skills/zju-mail/`。
本 skill 是同步副本，`zju_mail.py` 与本 SKILL.md 同目录；改源后需在 repo 里跑 `scripts/sync_skills.sh`。

## ⚠️ 二次验证（2FA）必须用客户端专用密码

浙大邮箱默认开二次验证，**Web 登录密码（= VPN/上网账号密码）不能用于 IMAP/SMTP 客户端**。第一次接入前，必须先在网页端（https://mail.zju.edu.cn）登录 → 设置 → 客户端专用密码（"专用密码生成"）生成一条 16 位的客户端专用密码，**生成时只显示一次，必须立即保存**。这条专用密码才是 wrapper 要存进 Keychain 的 password。

参考文档：https://mail.zju.edu.cn/coremail/help/2fa.html

注意：
- 一条专用密码对应一个客户端名（"mymac" / "workbuddy" 等），可以建多条以便识别/单独撤销。
- 网页/邮箱密码改时不会自动轮换专用密码；专用密码独立管理、丢了重生成即可（旧的自动失效）。
- 跨设备复用：一条专用密码可以同时在多台机器用（设备名只是备注）；想撤销单条就删那一条。

## 凭据（不进 repo、不进对话记录）

macOS Keychain 单条目：service `zju-mail`，account = 邮箱地址，password = **客户端专用密码**（不是网页登录密码）。

一次性写入（Setup 用，日常不要执行）：

```bash
security add-generic-password -s zju-mail -a "<addr>@zju.edu.cn" -w "<客户端专用密码>"
```

密码变更后更新：

```bash
security delete-generic-password -s zju-mail
security add-generic-password -s zju-mail -a "<addr>@zju.edu.cn" -w "<新专用密码>"
```

脚本优先读环境变量 `ZJU_MAIL_ADDR` / `ZJU_MAIL_PASS`（仅测试用），否则读 Keychain。
两者都没有时报错退出（code 2），此时按上面命令补 Keychain，不要让用户把密码发到对话里。

## 调用方式

```bash
python3 <skill_dir>/zju_mail.py <command> [options]
```

所有输出为单个 JSON：`{"ok": true, "data": ...}` 或 `{"ok": false, "error": "..."}`。
解析 `data` 字段展示给用户；`ok:false` 时把 error 原样转述。

## 命令速查

| 命令 | 用途 | 示例 |
|---|---|---|
| `test` | 连接+登录自检 | `zju_mail.py test` |
| `folders` | 列文件夹 | `zju_mail.py folders` |
| `list` | 列最新邮件（uid/发件人/主题/时间/未读） | `-f INBOX -n 10 --unread --since 2026-08-01` |
| `read <uid>` | 读全文+附件名 | `-f INBOX` |
| `search <query>` | 关键词搜邮件 | `-n 20` |
| `attachments <uid>` | 列出/下载附件 | `-d /path/to/dir` 下载 |
| `send` | 发新邮件 | `--to a@x.com,b@x.com --cc c@x.com --subject S --body B --attach f.pdf` |
| `reply <uid>` | 回复（自动引用原文、In-Reply-To） | `--body "..." --all` 表示回复全部 |
| `draft` | 存草稿到服务器草稿箱（自动探测 Drafts/草稿箱文件夹），网页版/客户端可继续编辑 | `--subject S --body B`，`--to/--cc` 可选可后补 |
| `mark <uid>` | 打标签：标记已读/未读、加/去星标旗标、自定义关键字标签 | `--seen` `--unseen` `--flag` `--unflag` `--keyword 重要 Review` |

## 行为规则

1. **发信（send / reply）前必须向用户展示完整收件人、主题、正文并获确认**，与 QQ 邮箱技能的两阶段确认规则一致。收发件人地址必须原样保留，不得自动补全或改写。
2. 读信（list/read/search/attachments）只读操作，可直接执行；wrapper 用 `BODY.PEEK`，不会把邮件标记为已读。
3. `draft`（存草稿）和 `mark`（标签/旗标/已读状态）是轻量写操作：用户明确要求时直接执行即可，无需二次确认，但执行后报告结果（存到哪个文件夹、设了什么标签）。
4. 展示邮件用中文标签（发件人/收件人/主题/时间/正文/附件），时间格式 YYYY-MM-DD HH:MM:SS。
5. 邮件正文不添加任何自动签名或"由 AI 代发"类脚注。
6. 附件下载默认存到用户指定的目录；未指定时先问。
7. 大附件（>2GB）不可能出现（浙大单附件上限 2GB），但下载大附件前告知用户目标路径。
8. 未实现的操作：转发（forward）、移动/删除邮件。需要时先在源 repo 给 wrapper 加子命令，再跑同步，不要用别的工具绕。

## 故障排查

| 现象 | 处理 |
|---|---|
| exit 2（凭据缺失） | 按上面命令写 Keychain |
| exit 3（连不上服务器） | 检查网络/VPN；浙大邮箱校外直连一般可用，若被限制提示用户连学校 VPN（myvpn.zju.edu.cn） |
| exit 4（登录失败） | 密码错或被改；提醒用户去 mail.zju.edu.cn 重置后更新 Keychain |
| 搜中文无结果但邮件存在 | Coremail 的 UTF-8 SEARCH 支持不稳，脚本已自动降级 SUBJECT/TEXT；仍不行就用 `list --since` 翻列表 |

## 健康检查

```bash
python3 <skill_dir>/zju_mail.py test
```

connections.yaml 里 `school-email` 条目登记此连接；状态源是 repo 的 `config/connections.yaml`。
