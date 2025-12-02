# PikPakAPI

异步 Python SDK + 简易 Web 管理界面，用于调用 PikPak 官方 REST API。

## 安装 / 依赖
- Python 3.8+
- 依赖：`httpx`, `fastapi`, `uvicorn[standard]`, `python-multipart`
- 安装 SDK：`pip install pikpakapi`

## SDK 快速示例
```python
import asyncio
from pikpakapi import PikPakApi

async def main():
    client = PikPakApi(username="your_username", password="your_password")
    await client.login()
    await client.refresh_access_token()
    files = await client.file_list()
    print(files)

asyncio.run(main())
```

## Web 管理界面
个人用途的轻量 UI，基于 FastAPI。默认使用内存 session（浏览器 cookie 里保存 session_id），适合单实例运行。

### 启动
```bash
pip install -r requirements.txt  # 或 poetry install
uvicorn app.main:app --reload
```
访问 `http://localhost:8000/login`，用你的 PikPak 账号密码登录。

### 功能
- **路径导航**：路径输入框 + “不存在则创建”，可直接跳转目录；面包屑可通过返回按钮回退。
- **空间使用**：顶部展示配额进度条。
- **离线任务**：创建磁力/直链离线下载；列表展示，支持重试/删除，手动刷新。
- **批量转存分享链接**：每行一个分享链接，支持输入分享密码，调用 `restore` 批量转存。
- **文件移动/复制**：按路径批量移动或复制，可选择自动创建目标路径。
- **主题切换**：日间/夜间模式，记忆上次选择。

### 注意
- Session 保存在内存，服务重启需重新登录；若要多实例/持久化，可改为 Redis 存储。
- 文件/路径操作使用现有 SDK 能力，未修改核心逻辑。
- 本项目定位个人自用，暂未提供 Docker；如需容器化可自行添加简单的 Dockerfile/compose。

## 开源协议
GPL-3.0-only
