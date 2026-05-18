# Scripts

This directory holds repo-local maintenance helpers.

## Available Scripts

- `sync_skills.sh`: syncs `skills/daily-manager` and `skills/personal-feishu-interface` from this repo into the installed Codex and Hermes skill locations on this machine.

## Boundary

This repo currently does not keep Feishu record CRUD wrappers. Day-to-day Feishu writes should use `lark-cli` directly, guided by `config/lark_daily_workspace.json` and the skills. Add CRUD scripts only after the same operation becomes repetitive enough to justify a stable helper.
