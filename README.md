# Tg Bot Template

基于 Pyrogram 库的 Telegram Bot 模板
包含以下模块:

- 日志模块
- 配置模块
- 快捷管理脚本
- `uvloop` / `winloop` 优化
- 看门狗模块(Bot掉线自动重启)
- Dockerfile & Docker Compose

## 环境变量

将 `.env.example` 文件重命名为 `.env`

| 名称          | 描述                            | 默认值     |
|-------------|-------------------------------|---------|
| `ADMINS`    | 管理员用户ID，多个用户用逗号分隔             |         |
| `API_ID`    | 登录 https://my.telegram.org 获取 |         |
| `API_HASH`  | 登录 https://my.telegram.org 获取 |         |
| `BOT_TOKEN` | 在 https://t.me/BotFather 获取   |         |
| `BOT_PROXY` | Bot 代理, 海外服务器不用填              |         |
| `DEBUG`     | 调试模式开关，设置为 `true` 启用调试日志      | `false` |

## 开始部署

#### Docker (推荐):

**在项目根目录运行:**

```shell
sudo sh start.sh # 构建并运行 Bot
# 其他命令:
sudo sh start.sh -h # 查看帮助
sudo sh start.sh stop  # 停止 Bot
sudo sh start.sh restart # 重启 Bot
```

#### 直接运行:

**在项目根目录运行:**

```shell
# 安装依赖
apt install python3-pip -y
pip install uv --break-system-packages
uv venv --python 3.12
uv sync
# 运行 Bot
uv run bot.py 
```

## 使用

私聊 Bot 发送指令 `/menu` 即可自动设置菜单
