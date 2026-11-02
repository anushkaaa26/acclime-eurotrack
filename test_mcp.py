#!/usr/bin/env python3
"""
Test script for verifying MCP JSON-RPC protocol handling over stdio
Simulates Claude Desktop / Cursor connecting to mcp_server.py
"""

import subprocess
import json
import sys
import os

MCP_SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")

def run_rpc_test():
    proc = subprocess.Popen(
        [sys.executable, MCP_SERVER_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 1. Initialize
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "TestClient", "version": "1.0"}
        }
    }
    proc.stdin.write(json.dumps(init_req) + "\n")
    proc.stdin.flush()
    init_res = json.loads(proc.stdout.readline())
    print("Initialize Response:", init_res.get("result", {}).get("serverInfo"))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "acclime-eurotrack-mcp"
    
    # 2. List tools
    tools_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    proc.stdin.write(json.dumps(tools_req) + "\n")
    proc.stdin.flush()
    tools_res = json.loads(proc.stdout.readline())
    tools = tools_res.get("result", {}).get("tools", [])
    print(f"Tools advertised ({len(tools)}):", [t["name"] for t in tools])
    assert len(tools) == 3
    
    # 3. Call ask_companies_met_last_year tool
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "ask_companies_met_last_year",
            "arguments": {"country": "Germany", "met_last_year": True}
        }
    }
    proc.stdin.write(json.dumps(call_req) + "\n")
    proc.stdin.flush()
    call_res = json.loads(proc.stdout.readline())
    text_content = call_res.get("result", {}).get("content", [{}])[0].get("text", "")
    print("Tool Call Response preview:\n", text_content[:200], "...")
    assert "Bavaria Katalys Chem AG" in text_content
    
    proc.stdin.close()
    proc.terminate()
    print("\n✓ Full MCP JSON-RPC stdio protocol test passed successfully!")

if __name__ == "__main__":
    run_rpc_test()
