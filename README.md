# 🐋 serpapi_mcp

> 自定义 SerpAPI MCP 服务器 — 让 AI 助手拥有 Google Scholar 学术搜索能力

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 功能特性

| 工具 | 功能 | 支持 |
|------|------|:--:|
| `search_google_scholar` | Google Scholar 学术论文搜索 | 中英文关键词、PDF 链接、引用数 |
| `search_google` | Google 通用网页搜索 | 网页标题、链接、摘要 |

---

## 📦 安装

### 1. 克隆项目

```bash
git clone https://github.com/Yotsuki2213/serpapi_mcp.git
cd serpapi_mcp
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 获取 SerpAPI Key

前往 [serpapi.com](https://serpapi.com) 注册（免费 100 次/月）

在 Dashboard 中复制你的 API Key。

---

## ⚙️ 配置 MCP 客户端

### Cherry Studio

**设置 → MCP 管理 → 以 JSON 编辑**，添加：

```json
{
  "mcpServers": {
    "serpapi-custom": {
      "type": "stdio",
      "command": "python",
      "args": ["下载路径\\serpapi_mcp\\serpapi_mcp_server.py"],
      "env": {
        "SERPAPI_API_KEY": "你的SerpAPI密钥"
      }
    }
  }
}
```

把 `下载路径` 替换为实际路径，例如 `C:\\Users\\你的用户名\\serpapi_mcp`

### Claude Desktop

编辑 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "serpapi-custom": {
      "command": "python",
      "args": ["/path/to/serpapi_mcp/serpapi_mcp_server.py"],
      "env": {
        "SERPAPI_API_KEY": "你的SerpAPI密钥"
      }
    }
  }
}
```

---

## 🧪 测试

### 终端测试

```bash
# Windows CMD
set SERPAPI_API_KEY=你的密钥
python serpapi_mcp_server.py

# Mac / Linux
export SERPAPI_API_KEY=你的密钥
python serpapi_mcp_server.py
```

没报错即正常（Ctrl+C 退出）。

### Cherry Studio 中测试

新建对话，输入：

> 在 Google Scholar 搜索：蔡晋辉 中国计量大学

能返回论文列表即成功。

---

## 🛠 工具详解

### `search_google_scholar` — Google Scholar 搜索

| 参数 | 类型 | 必填 | 说明 |
|------|------|:--:|------|
| `query` | string | 是 | 搜索关键词，支持中文 |
| `num_results` | integer | 否 | 返回数量，默认 10 |
| `language` | string | 否 | `zh-cn` 或 `en`，默认 `zh-cn` |

返回内容：标题、作者、摘要（前300字）、引用数、PDF 链接。

### `search_google` — Google 通用搜索

| 参数 | 类型 | 必填 | 说明 |
|------|------|:--:|------|
| `query` | string | 是 | 搜索关键词 |
| `num_results` | integer | 否 | 返回数量，默认 10 |

返回内容：网页标题、链接、摘要（前200字）。

---

## ❓ 常见问题

| 问题 | 解决 |
|------|------|
| MCP 连接失败 | 检查 Python 路径、依赖是否安装、API Key 是否正确 |
| 搜索无结果 | 检查 API Key 额度（免费 100 次/月） |
| 中文乱码 | 确保脚本文件编码为 UTF-8 |
| `ModuleNotFoundError: mcp` | `pip install mcp` |

---

## 📄 许可证

MIT © Yotsuki2213

---

> 🐋 有问题开 Issue！