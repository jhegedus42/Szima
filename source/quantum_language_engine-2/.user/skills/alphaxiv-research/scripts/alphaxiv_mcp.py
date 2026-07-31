#!/usr/bin/env python3
"""Minimal MCP (streamable HTTP) client for the alphaXiv research server.

Endpoint: https://api.alphaxiv.org/mcp/v1  (MCP v1.0.0, streamable HTTP transport)
Auth:     Authorization: Bearer <key>  (skips the OAuth browser flow)

Key resolution order:
  1. ALPHAXIV_API_KEY environment variable
  2. "api_key" field in config.json next to this script

Usage:
  python3 alphaxiv_mcp.py list-tools
  python3 alphaxiv_mcp.py call <tool_name> '<json_arguments>'

Examples:
  python3 alphaxiv_mcp.py call discover_papers '{"keywords":["hallucination","LLM"],"question":"Approaches to reducing hallucination in LLMs","difficulty":5}'
  python3 alphaxiv_mcp.py call get_paper_content '{"url":"https://arxiv.org/abs/1706.03762"}'
  python3 alphaxiv_mcp.py call answer_pdf_queries '{"paper":"2307.12307","queries":["What datasets were used?"]}'
  python3 alphaxiv_mcp.py call list_library '{}'

Prints the tool's text content to stdout. Diagnostics go to stderr.
Exit codes: 0 ok, 2 auth/config error, 1 other failure.
"""

import json
import os
import sys
import urllib.request
import urllib.error

ENDPOINT = "https://api.alphaxiv.org/mcp/v1"
PROTOCOL_VERSION = "2025-03-26"
TIMEOUT = 300  # discover_papers runs an agentic loop; high difficulty is slow


def load_api_key():
    key = os.environ.get("ALPHAXIV_API_KEY", "").strip()
    if key:
        return key
    cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    try:
        with open(cfg, "r", encoding="utf-8") as f:
            key = json.load(f).get("api_key", "").strip()
    except (OSError, json.JSONDecodeError):
        pass
    if not key or key.startswith("PASTE_YOUR"):
        return None
    return key


def parse_sse(body):
    """Extract JSON-RPC messages from a text/event-stream body."""
    messages = []
    data_lines = []
    for line in body.splitlines():
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
        elif line.strip() == "" and data_lines:
            payload = "\n".join(data_lines)
            data_lines = []
            try:
                messages.append(json.loads(payload))
            except json.JSONDecodeError:
                pass
    if data_lines:
        try:
            messages.append(json.loads("\n".join(data_lines)))
        except json.JSONDecodeError:
            pass
    return messages


class MCPClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session_id = None
        self._next_id = 0

    def _post(self, payload, is_notification=False):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            # Cloudflare blocks urllib's default signature (error 1010)
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        if self.api_key:
            headers["Authorization"] = "Bearer " + self.api_key
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                sid = resp.headers.get("Mcp-Session-Id")
                if sid:
                    self.session_id = sid
                if is_notification or resp.status == 202:
                    return None
                raw = resp.read().decode("utf-8", errors="replace")
                ctype = resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:500]
            if e.code in (401, 403):
                sys.stderr.write(
                    "AUTH ERROR (%s): missing, invalid, or revoked API key.\n"
                    "Set ALPHAXIV_API_KEY or put the key in config.json next to this script.\n"
                    "Create keys at https://www.alphaxiv.org -> Settings > API Keys.\n"
                    "Server said: %s\n" % (e.code, detail)
                )
                sys.exit(2)
            sys.stderr.write("HTTP %s from alphaXiv MCP: %s\n" % (e.code, detail))
            sys.exit(1)
        except urllib.error.URLError as e:
            sys.stderr.write("NETWORK ERROR reaching %s: %s\n" % (ENDPOINT, e.reason))
            sys.exit(1)

        if "text/event-stream" in ctype:
            for msg in parse_sse(raw):
                if not is_notification and msg.get("id") == payload.get("id"):
                    return msg
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            sys.stderr.write("Unparseable response body:\n%s\n" % raw[:1000])
            sys.exit(1)

    def _request(self, method, params):
        self._next_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id,
            "method": method,
            "params": params,
        }
        resp = self._post(payload)
        if resp is None:
            sys.stderr.write("No response received for %s\n" % method)
            sys.exit(1)
        if "error" in resp:
            err = resp["error"]
            sys.stderr.write(
                "MCP ERROR %s: %s\n" % (err.get("code"), err.get("message"))
            )
            sys.exit(1)
        return resp.get("result", {})

    def connect(self):
        self._request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "alphaxiv-research-skill", "version": "1.0.0"},
            },
        )
        self._post(
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            is_notification=True,
        )

    def list_tools(self):
        return self._request("tools/list", {}).get("tools", [])

    def call_tool(self, name, arguments):
        return self._request("tools/call", {"name": name, "arguments": arguments})


def print_result(result):
    contents = result.get("content", [])
    texts = [c.get("text", "") for c in contents if c.get("type") == "text"]
    if texts:
        print("\n\n".join(texts))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("isError"):
        sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if sys.argv[1] not in ("list-tools", "call"):
        sys.stderr.write("Unknown command: %s (expected list-tools|call)\n" % sys.argv[1])
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        sys.stderr.write(
            "NO API KEY FOUND.\n"
            "Either:\n"
            "  export ALPHAXIV_API_KEY=<key>\n"
            "or write {\"api_key\": \"<key>\"} into config.json next to this script.\n"
            "Create keys at https://www.alphaxiv.org -> Settings > API Keys.\n"
        )
        sys.exit(2)

    cmd = sys.argv[1]
    if cmd == "call":
        if len(sys.argv) < 4:
            sys.stderr.write("Usage: call <tool_name> '<json_arguments>'\n")
            sys.exit(1)
        try:
            args = json.loads(sys.argv[3])
        except json.JSONDecodeError as e:
            sys.stderr.write("Invalid JSON arguments: %s\n" % e)
            sys.exit(1)

    client = MCPClient(api_key)
    client.connect()

    if cmd == "list-tools":
        for t in client.list_tools():
            print("- %s: %s" % (t.get("name"), (t.get("description") or "")[:120]))
    else:
        print_result(client.call_tool(sys.argv[2], args))


if __name__ == "__main__":
    main()
