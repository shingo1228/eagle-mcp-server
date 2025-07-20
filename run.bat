@echo off
cd /d "E:\00Eagle\eagle-mcp-server"
set PYTHONPATH=%cd%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
echo Starting Eagle MCP Server v2... 1>&2
uv run main.py