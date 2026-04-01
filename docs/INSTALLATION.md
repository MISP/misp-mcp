# Installation

## Requirements

- Python 3.10 or later
- A running MISP instance (2.4+)
- A MISP API key with read access

## Install from PyPI

```bash
pip install misp-mcp
```

## Install from source

```bash
git clone https://github.com/MISP/misp-mcp.git
cd misp-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

For development (includes test dependencies):

```bash
pip install -e ".[dev]"
```

## Configuration

The server requires two environment variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `MISP_URL` | Yes | — | Full URL of your MISP instance |
| `MISP_API_KEY` | Yes | — | API authentication key |
| `MISP_VERIFYCERT` | No | `true` | Verify TLS certificates |

### Getting your API key

1. Log in to your MISP instance
2. Go to **Administration > List Users** (or your user profile)
3. Copy the **Authkey** value

### Self-signed certificates

If your MISP instance uses a self-signed certificate, set:

```bash
export MISP_VERIFYCERT=false
```

## Verify installation

```bash
export MISP_URL="https://your-misp-instance"
export MISP_API_KEY="your-api-key"
misp-mcp
```

The server starts in stdio mode and waits for MCP messages. Press `Ctrl+C` to stop.

## Configure as an MCP server

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "misp": {
      "command": "misp-mcp",
      "env": {
        "MISP_URL": "https://your-misp-instance",
        "MISP_API_KEY": "your-api-key"
      }
    }
  }
}
```

If installed in a virtualenv, use the full path:

```json
{
  "mcpServers": {
    "misp": {
      "command": "/path/to/misp-mcp/venv/bin/misp-mcp",
      "env": {
        "MISP_URL": "https://your-misp-instance",
        "MISP_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Claude Code

Add to your project's `.mcp.json` or global MCP settings:

```json
{
  "mcpServers": {
    "misp": {
      "command": "misp-mcp",
      "env": {
        "MISP_URL": "https://your-misp-instance",
        "MISP_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Updating

```bash
pip install --upgrade misp-mcp
```

Or from source:

```bash
cd misp-mcp
git pull
pip install -e .
```
