"""
SerpAPI Google Scholar MCP Server
自定义 MCP 服务器，将 SerpAPI 搜索封装为 MCP 工具

使用方法：
  1. 安装依赖：pip install mcp serpapi
  2. 设置环境变量：set SERPAPI_API_KEY=你的密钥
  3. 配置 Cherry Studio / Claude Desktop 使用 stdio 传输
"""

import os
import json
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import serpapi


# 从环境变量读取 API Key
API_KEY = os.environ.get("SERPAPI_API_KEY", "")

# 创建 MCP 服务器实例
server = Server("serpapi-server")


@server.list_tools()
async def list_tools():
    """列出所有可用工具"""
    return [
        Tool(
            name="search_google_scholar",
            description="在 Google Scholar 上搜索学术论文。返回标题、作者、摘要、引用数、PDF链接等。支持中英文关键词。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，支持中文。例如：'machine learning'"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "返回结果数量，默认 10",
                        "default": 10
                    },
                    "language": {
                        "type": "string",
                        "description": "语言：zh-cn（中文）或 en（英文）",
                        "default": "zh-cn"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_google",
            description="在 Google 上通用搜索。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "返回结果数量，默认 10",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """处理工具调用"""
    
    if name == "search_google_scholar":
        query = arguments.get("query", "")
        num = arguments.get("num_results", 10)
        lang = arguments.get("language", "zh-cn")
        
        client = serpapi.Client(api_key=API_KEY)
        results = client.search({
            "engine": "google_scholar",
            "q": query,
            "hl": lang,
            "num": num
        })
        
        organic = results.get("organic_results", [])
        
        # 格式化为易读文本
        output_lines = [f"🔍 Google Scholar 搜索：{query}\n"]
        output_lines.append(f"共找到 {len(organic)} 条结果\n")
        output_lines.append("=" * 60)
        
        for i, paper in enumerate(organic, 1):
            title = paper.get("title", "无标题")
            authors = paper.get("publication_info", {}).get("summary", "未知作者")
            snippet = paper.get("snippet", "无摘要")
            citations = paper.get("inline_links", {}).get("cited_by", {}).get("total", 0)
            pdf_url = paper.get("resources", [{}])[0].get("link", "") if paper.get("resources") else ""
            
            output_lines.append(f"\n📄 [{i}] {title}")
            output_lines.append(f"   作者: {authors}")
            output_lines.append(f"   引用: {citations} 次")
            output_lines.append(f"   摘要: {snippet[:300]}...")
            if pdf_url:
                output_lines.append(f"   PDF: {pdf_url}")
            output_lines.append("-" * 40)
        
        return [TextContent(type="text", text="\n".join(output_lines))]
    
    elif name == "search_google":
        query = arguments.get("query", "")
        num = arguments.get("num_results", 10)
        
        client = serpapi.Client(api_key=API_KEY)
        results = client.search({
            "engine": "google",
            "q": query,
            "num": num
        })
        
        organic = results.get("organic_results", [])
        
        output_lines = [f"🔍 Google 搜索：{query}\n"]
        output_lines.append("=" * 60)
        
        for i, r in enumerate(organic, 1):
            output_lines.append(f"\n[{i}] {r.get('title', '')}")
            output_lines.append(f"   链接: {r.get('link', '')}")
            output_lines.append(f"   摘要: {r.get('snippet', '')[:200]}...")
            output_lines.append("-" * 40)
        
        return [TextContent(type="text", text="\n".join(output_lines))]
    
    else:
        return [TextContent(type="text", text=f"未知工具: {name}")]


async def main():
    """启动 MCP 服务器"""
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
