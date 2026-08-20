# Playbook · 连接诊断（doctor）

**场景**：任何飞书/腾讯会议/日历操作报错时，按此排查。连接状态总览见 [../../config/connections.yaml](../../config/connections.yaml)。

## 排查顺序

```bash
# 1. 飞书整体健康（版本/配置/认证/连通性）
lark-cli doctor

# 2. 飞书身份与 scope
lark-cli auth status
#    报 missing_scope 时按提示补授权：
#    lark-cli auth login --scope "<缺失scope>" --no-wait --json
#    拿到 URL → 生成 QR 给用户扫 → 用户确认后 --device-code 完成

# 3. 腾讯会议
tmeet auth status
#    AccessToken 过期（~6h）→ tmeet auth login（阻塞式，前台运行）

# 4. GitHub（SSH）
ssh -T git@github.com   # 应回 "Hi xingminw!"

# 5. 网络（代理注意）
#    lark-cli 对 HTTPS_PROXY 敏感，异常时检查代理设置
```

## 常见错误速查

| 症状 | 原因 | 处理 |
|---|---|---|
| `missing_scope: calendar:...` | 该域 scope 未授权 | 按提示 auth login --scope 补 |
| `15180001 user not found`（mail） | 飞书邮箱未开通 | 用户去 设置→邮箱 开通 |
| `您不在该组织的 CLI 授权人员范围内`（dws） | 学校钉钉授权墙 | 已知死路，见 decisions.md D1 |
| search-event 搜不到刚建的事件 | 索引延迟 | 用 +agenda 按天查 |
| `user config is empty`（tmeet） | 未登录 | tmeet auth login |
| 外接 SSD 不识别 | exFAT 无 journaling 脆弱性 | 重新插拔；重灌 APFS 后应绝迹 |
