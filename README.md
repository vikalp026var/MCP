# RemoteMCP

## MCP Inspector (browser UI)

**Stop any old inspector first** (Ctrl+C), then:

```bash
chmod +x inspect.sh
./inspect.sh
```

Or:

```bash
source .venv/bin/activate
fastmcp dev inspector main.py
```

When the browser opens, leave transport as **STDIO** and press **Connect**.  
Command should be `fastmcp`, not `uv`.

### If Connect still fails — set these manually in the inspector UI

| Field | Value |
|-------|-------|
| Transport | STDIO |
| Command | `/Users/vikalpv/GenAI/MCP/RemoteMCP/.venv/bin/fastmcp` |
| Arguments | `run main.py --no-banner` |

### Alternative — connect over HTTP (no stdio)

**Terminal 1** — start the server:

```bash
.venv/bin/python main.py
```

**Inspector UI** — change settings:

| Field | Value |
|-------|-------|
| Transport | Streamable HTTP |
| URL | `http://127.0.0.1:8000/mcp` |

Then press **Connect**.

## HTTP server only

```bash
.venv/bin/python main.py
```

Endpoint: http://127.0.0.1:8000/mcp

# https://nervous-blush-bird.fastmcp.app/mcp