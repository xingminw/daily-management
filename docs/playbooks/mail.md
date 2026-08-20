# Playbook · 邮箱（待启用）

**状态**：⏸ 阻塞中——个人飞书邮箱功能未开通（API 报 15180001 "user not found"），学校邮箱 @zju.edu.cn 2026 年 9 月报到后才有。

## 启用步骤（9 月执行）

1. 用户在飞书 设置 → 邮箱 开通飞书邮箱（免费）。
2. 拿到 @zju.edu.cn 账号后，优先尝试：飞书邮箱 → 设置 → 账户 → 添加外部邮箱账户（若学校邮箱是腾讯企业邮托管大概率可成）。
3. 验证 API 可见性：
   ```bash
   lark-cli mail user_mailbox.messages list --user-mailbox-id me --page-size 5
   ```
4. 不成则走 IMAP/SMTP（学校邮件服务器地址待查，TLS 加密，凭据存钥匙串不进 repo）。

## 可用命令速查（开通后）

```bash
lark-cli mail user_mailbox.messages list --user-mailbox-id me --page-size 20 [--only-unread]
lark-cli mail +message <message-id>          # 读单封全文
lark-cli mail +reply <message-id>            # 回复草稿（默认不直接发）
lark-cli mail +draft-send <draft-id>         # 发送前必须用户确认
```

## 安全约定

- 发送类操作（+send / +reply --confirm-send / +forward --confirm-send）执行前必须向用户展示完整收件人和正文摘要。
- 草稿默认不发送；用户说"发"才算确认。
