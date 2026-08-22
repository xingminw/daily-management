---
name: personal-mail
description: "个人邮箱统一 IMAP/SMTP wrapper（mail.py，-p zju/qq 选邮箱）。触发场景：看浙大邮箱/QQ邮箱、存草稿到草稿箱、给邮件打标签/加星标/标已读、搜索邮件、下载附件、发邮件、回复邮件。支持 connector 覆盖不到的能力：草稿（draft）、标签（mark）、任意文件夹。关键词：浙大邮箱、QQ邮箱、学校邮箱、草稿、标签、星标、zju.edu.cn、qq.com。"
---

# Personal Mail Skill (personal-mail)

统一 wrapper：本 skill 目录下的 `mail.py`（纯标准库 Python，零依赖），`-p` 选邮箱。

| provider | 邮箱 | IMAP | SMTP | Keychain service |
|---|---|---|---|---|
| `zju` | 浙大邮箱 @zju.edu.cn（Coremail 自建） | imap.zju.edu.cn:993 | smtp.zju.edu.cn:994 | `zju-mail` |
| `qq` | QQ 邮箱（需网页端开 IMAP/SMTP + 授权码） | imap.qq.com:993 | smtp.qq.com:465 | `qq-mail` |

源文件在 daily-management repo：`/Volumes/My SSD/Codespace/daily-management/skills/personal-mail/`。
本 skill 是同步副本，`mail.py` 与本 SKILL.md 同目录；改源后需在 repo 里跑 `scripts/sync_skills.sh`。

## 与官方 connector 的分工

QQ 邮箱已有官方 connector（OAuth，读信/发信/搜索/附件/转发）——**日常读发优先用 connector**。
wrapper 补 connector 没有的能力：**draft（存草稿）、mark（标签/星标/已读）、任意文件夹访问、大附件发送**（connector 限 3 个附件共 3MB，wrapper 走 SMTP 无此限）。
浙大邮箱无 connector，wrapper 是唯一通道。

## 凭据（不进 repo、不进对话记录）

每个 provider 一条 macOS Keychain：service 见上表，account = 邮箱地址，password = **客户端专用密码/授权码**（不是网页登录密码）。

- zju：网页端（mail.zju.edu.cn）→ 设置 → 客户端专用密码。二次验证默认开启，网页密码（= VPN 密码）连不了 IMAP/SMTP。参考 https://mail.zju.edu.cn/coremail/help/2fa.html
- qq：网页版（mail.qq.com）→ 设置 → 账户 → 开启 IMAP/SMTP 服务 → 生成授权码（16 位字母）。

一次性写入（Setup 用，日常不要执行）：

```bash
security add-generic-password -s zju-mail -a "<addr>@zju.edu.cn" -w "<客户端专用密码>"
security add-generic-password -s qq-mail  -a "<addr>@qq.com"     -w "<授权码>"
```

密码变更后更新（先 delete 再 add，命令同上）。脚本优先读环境变量 `MAIL_ADDR` / `MAIL_PASS`（仅测试用），否则读 Keychain。两者都没有时报错退出（code 2），此时按上面命令补 Keychain，不要让用户把密码发到对话里。

## 调用方式

```bash
python3 <skill_dir>/mail.py -p <zju|qq> <command> [options]
```

所有输出为单个 JSON：`{"ok": true, "data": ...}` 或 `{"ok": false, "error": "..."}`。

## 命令速查

| 命令 | 用途 | 示例 |
|---|---|---|
| `test` | 连接+登录自检 | `-p zju test` |
| `folders` | 列文件夹 | `-p qq folders` |
| `list` | 列最新邮件（uid/发件人/主题/时间/未读） | `-f INBOX -n 10 --unread --since 2026-08-01` |
| `read <uid>` | 读全文+附件名 | `-f INBOX` |
| `search <query>` | 关键词搜邮件 | `-n 20` |
| `attachments <uid>` | 列出/下载附件 | `-d /path/to/dir` 下载 |
| `send` | 发新邮件 | `--to a@x.com,b@x.com --cc c@x.com --subject S --body B --attach f.pdf` |
| `reply <uid>` | 回复（自动引用原文、In-Reply-To） | `--body "..." --all` 表示回复全部 |
| `draft` | 存草稿到服务器草稿箱（自动探测 Drafts/草稿箱文件夹） | `--subject S --body B`，`--to/--cc` 可选可后补 |
| `mark <uid>` | 打标签：已读/未读、星标、自定义关键字标签 | `--seen` `--unseen` `--flag` `--unflag` `--keyword 重要 Review` |

## 行为规则

1. **发信（send / reply）前必须向用户展示完整收件人、主题、正文并获确认**。收发件人地址必须原样保留，不得自动补全或改写。
2. 读信（list/read/search/attachments）只读操作，可直接执行；wrapper 用 `BODY.PEEK`，不会把邮件标记为已读。
3. `draft`（存草稿）和 `mark`（标签/旗标/已读状态）是轻量写操作：用户明确要求时直接执行，执行后报告结果。
4. 展示邮件用中文标签（发件人/收件人/主题/时间/正文/附件），时间格式 YYYY-MM-DD HH:MM:SS。
5. 邮件正文不添加任何自动签名或"由 AI 代发"类脚注。
6. 附件下载默认存到用户指定的目录；未指定时先问。
7. 未实现的操作：转发（forward）、移动/删除邮件。需要时先在源 repo 给 wrapper 加子命令，再跑同步，不要用别的工具绕。

## 故障排查

| 现象 | 处理 |
|---|---|
| exit 2（凭据缺失） | 按上面命令写 Keychain |
| exit 3（连不上服务器） | 检查网络；zju 校外一般可直连，被限时提示用户连学校 VPN（myvpn.zju.edu.cn） |
| exit 4（登录失败） | zju：客户端专用密码错/被删，网页端重新生成；qq：授权码错或 IMAP/SMTP 服务未开启，网页端检查 |
| 搜中文无结果但邮件存在 | Coremail 的 UTF-8 SEARCH 支持不稳，脚本已自动降级 SUBJECT/TEXT；仍不行就用 `list --since` 翻列表 |
| draft 返回的 uid 与文件夹实际 uid 不符 | 已知 Coremail 怪癖：APPENDUID 返回时间戳样式数字，仅作参考，以 `list -f Drafts` 为准 |

## 健康检查

```bash
python3 <skill_dir>/mail.py -p zju test
python3 <skill_dir>/mail.py -p qq test
```

connections.yaml 里 `school-email` / `qq-mail` 条目登记此连接；状态源是 repo 的 `config/connections.yaml`。
