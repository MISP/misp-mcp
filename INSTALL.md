# Install and Run MISP MCP

This project is an MCP server for read-only MISP access through PyMISP.

## Requirements

- Python 3.13 recommended. The current package metadata allows Python 3.10+.
- `uv` for dependency management and command execution.
- A reachable MISP instance.
- A MISP API key with read access.

## Configure MISP access

Set these environment variables before running the server:

| Variable | Required | Example | Notes |
|---|---:|---|---|
| `MISP_URL` | Yes | `https://misp.example.org` | Base URL of the MISP instance. |
| `MISP_API_KEY` | Yes | `...` | MISP auth key. Do not commit it. |
| `MISP_VERIFYCERT` | No | `true` | Set to `false` for a development instance with a self-signed certificate. |
| `MISP_TIMEOUT` | No | `30` | PyMISP request timeout in seconds. |

Example shell setup:

```bash
export MISP_URL="https://misp.example.org"
export MISP_API_KEY="replace-with-your-auth-key"
export MISP_VERIFYCERT="true"
export MISP_TIMEOUT="30"
```

For local development, a `.env` file can be used by your shell or MCP client,
but the server reads environment variables directly. Do not commit secrets.

Minimal `.env` for local development:

```dotenv
MISP_URL=https://misp.example.org
MISP_API_KEY=replace-with-your-auth-key
MISP_VERIFYCERT=true
MISP_TIMEOUT=30
```

For a development MISP instance with a self-signed certificate, use
`MISP_VERIFYCERT=false`.

## Install from source

```bash
git clone https://github.com/MISP/misp-mcp.git
cd misp-mcp
uv sync --extra dev
```

## Run the MCP server

Run the server in stdio mode:

```bash
uv run misp-mcp
```

The process waits for MCP messages on stdin/stdout. Stop it with `Ctrl+C`.

The server does not open an HTTP port in this mode. MCP clients start it as a
child process and talk to it over stdin/stdout.

## Architecture

The MCP server is a local adapter between an MCP-capable client and a remote or
local MISP instance:

```text
Claude Code / opencode.ai / other MCP client
        |
        | MCP over stdio
        v
misp-mcp process
        |
        | HTTPS via PyMISP
        v
MISP server API
```

- **MISP server**: The threat-intelligence platform and source of truth. It can
  run on another host, such as `https://misp-dev.lo-res.org`, or on the same
  machine as the MCP server.
- **MCP server (`misp-mcp`)**: A Python process started by the MCP client. It
  usually runs on the same host as the client because stdio MCP clients launch it
  as a child process. It does not need to run on the MISP host.
- **Client**: Claude Code, opencode.ai, Claude Desktop, or another MCP-capable
  tool. The client sends tool calls to `misp-mcp`; `misp-mcp` converts them to
  read-only PyMISP calls.

For most desktop or CLI usage, run `misp-mcp` on the analyst workstation and
point `MISP_URL` at the central MISP server. Running `misp-mcp` on the same host
as MISP is only necessary when network policy requires local API access.

Common layouts:

| Layout | Where `misp-mcp` runs | When to use it |
|---|---|---|
| Analyst workstation to central MISP | Same machine as Claude Code, Codex, opencode.ai, or Claude Desktop | Default setup. The MCP client launches `misp-mcp`; `misp-mcp` calls `MISP_URL` over HTTPS. |
| MISP host local adapter | Same machine as the MISP server | Useful when the MISP API is only reachable from localhost or an internal network segment. |
| Raspberry Pi / small jump host | On a Pi or small Linux host that can reach MISP | Useful as a lightweight analyst box or network bridge. The MCP client still needs local stdio access to the process, normally via an SSH session or by running the client on the Pi. |

Do not expose the stdio server directly to the network. If a remote MCP
transport is needed later, add an authenticated HTTP MCP transport deliberately
and review the security model first.

## MCP client configuration

For an MCP client that supports command/args configuration, run from the cloned
repository with:

```json
{
  "mcpServers": {
    "misp": {
      "command": "uv",
      "args": ["run", "misp-mcp"],
      "cwd": "/absolute/path/to/misp-mcp",
      "env": {
        "MISP_URL": "https://misp.example.org",
        "MISP_API_KEY": "replace-with-your-auth-key",
        "MISP_VERIFYCERT": "true",
        "MISP_TIMEOUT": "30"
      }
    }
  }
}
```

If the package is installed into an environment available on `PATH`, the command
can instead be:

```json
{
  "mcpServers": {
    "misp": {
      "command": "misp-mcp",
      "env": {
        "MISP_URL": "https://misp.example.org",
        "MISP_API_KEY": "replace-with-your-auth-key",
        "MISP_VERIFYCERT": "true",
        "MISP_TIMEOUT": "30"
      }
    }
  }
}
```

### Codex

Codex local MCP configuration uses a TOML `mcp_servers` table. Add a server like
this to your Codex config, typically `~/.codex/config.toml`:

```toml
[mcp_servers.misp]
command = "uv"
args = ["run", "misp-mcp"]
cwd = "/absolute/path/to/misp-mcp"
env = {
  MISP_URL = "https://misp.example.org",
  MISP_API_KEY = "replace-with-your-auth-key",
  MISP_VERIFYCERT = "true",
  MISP_TIMEOUT = "30",
}
startup_timeout_sec = 20
tool_timeout_sec = 60
```

If `misp-mcp` is installed on `PATH`, use:

```toml
[mcp_servers.misp]
command = "misp-mcp"
env = {
  MISP_URL = "https://misp.example.org",
  MISP_API_KEY = "replace-with-your-auth-key",
  MISP_VERIFYCERT = "true",
  MISP_TIMEOUT = "30",
}
startup_timeout_sec = 20
tool_timeout_sec = 60
```

Restart Codex after changing the config. Then ask Codex something like:

```text
Use the MISP MCP server to search for recent events tagged tlp:white.
```

### Claude Code

Claude Code can add a local stdio MCP server with `claude mcp add`. Use user or
local scope for real API keys so secrets are not committed to a project file:

```bash
claude mcp add \
  --transport stdio \
  --scope user \
  --env MISP_URL=https://misp.example.org \
  --env MISP_API_KEY=replace-with-your-auth-key \
  --env MISP_VERIFYCERT=true \
  --env MISP_TIMEOUT=30 \
  misp \
  -- uv --directory /absolute/path/to/misp-mcp run misp-mcp
```

For a self-signed development MISP instance:

```bash
claude mcp add \
  --transport stdio \
  --scope user \
  --env MISP_URL=https://misp-dev.example.org \
  --env MISP_API_KEY=replace-with-your-auth-key \
  --env MISP_VERIFYCERT=false \
  --env MISP_TIMEOUT=30 \
  misp \
  -- uv --directory /absolute/path/to/misp-mcp run misp-mcp
```

Manage and verify the server:

```bash
claude mcp list
claude mcp get misp
claude
```

Inside Claude Code, run `/mcp` and confirm that `misp` is connected. Example
prompts:

```text
Use MISP to look up the attribute value 8.8.8.8.
List event reports for MISP event 3.
Search the MISP galaxies for APT28.
```

Claude Code also accepts JSON configuration in `.mcp.json` or `~/.claude.json`.
Use this shape if you prefer editing JSON directly:

```json
{
  "mcpServers": {
    "misp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/misp-mcp", "run", "misp-mcp"],
      "env": {
        "MISP_URL": "https://misp.example.org",
        "MISP_API_KEY": "replace-with-your-auth-key",
        "MISP_VERIFYCERT": "true",
        "MISP_TIMEOUT": "30"
      }
    }
  }
}
```

### opencode.ai

opencode.ai config uses an `mcp` object. Add a local server to `opencode.json`
or `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "misp": {
      "type": "local",
      "command": [
        "uv",
        "--directory",
        "/absolute/path/to/misp-mcp",
        "run",
        "misp-mcp"
      ],
      "environment": {
        "MISP_URL": "https://misp.example.org",
        "MISP_API_KEY": "replace-with-your-auth-key",
        "MISP_VERIFYCERT": "true",
        "MISP_TIMEOUT": "30"
      },
      "enabled": true,
      "timeout": 10000
    }
  }
}
```

Then start opencode from the workspace where that config applies and prompt:

```text
Use the misp MCP server to search for attributes matching example.com.
```

### Raspberry Pi or other small Linux host

Use this when the Pi can reach MISP and you want to run the MCP client on the Pi
or inside an SSH session to the Pi.

Install system prerequisites:

```bash
sudo apt-get update
sudo apt-get install -y git curl python3 python3-venv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install `misp-mcp`:

```bash
git clone https://github.com/MISP/misp-mcp.git
cd misp-mcp
uv sync --extra dev
```

Create a local environment file on the Pi:

```bash
cat > .env <<'EOF'
MISP_URL=https://misp.example.org
MISP_API_KEY=replace-with-your-auth-key
MISP_VERIFYCERT=true
MISP_TIMEOUT=30
EOF
chmod 600 .env
```

Run a connectivity check:

```bash
set -a
. ./.env
set +a
uv run python - <<'PY'
import os
from pymisp import PyMISP

client = PyMISP(
    url=os.environ["MISP_URL"],
    key=os.environ["MISP_API_KEY"],
    ssl=os.environ.get("MISP_VERIFYCERT", "true").lower()
    in {"true", "1", "yes"},
    timeout=int(os.environ.get("MISP_TIMEOUT", "30")),
)
print(client.search_index(limit=1, page=1))
PY
```

If you run Claude Code, Codex, or opencode.ai on the Pi, use the same local MCP
configuration examples above with `cwd` or `--directory` pointing to the cloned
repository on the Pi.

If your desktop client runs on another machine, do not point it at the Pi's
stdio process over the network. Instead, either SSH into the Pi and run the MCP
client there, or implement a separate authenticated remote MCP transport.

## Verify locally

Run the unit tests:

```bash
uv run --extra dev pytest
```

Run the server import check:

```bash
uv run python -c "from misp_mcp.server import mcp; print(mcp.name)"
```

Run a read-only PyMISP connectivity check:

```bash
uv run python - <<'PY'
import os
from pymisp import PyMISP

client = PyMISP(
    url=os.environ["MISP_URL"],
    key=os.environ["MISP_API_KEY"],
    ssl=os.environ.get("MISP_VERIFYCERT", "true").lower()
    in {"true", "1", "yes"},
    timeout=int(os.environ.get("MISP_TIMEOUT", "30")),
)
print(client.search_index(limit=1, page=1))
PY
```

## Implemented read-only tool groups

- Events, attributes, objects, and event reports.
- Attribute metadata helpers.
- Tags and taxonomies.
- Galaxies and galaxy clusters.
- Feeds.

The server intentionally does not expose write, publish, enrichment execution,
feed fetch, synchronisation, worker-control, or admin mutation tools.
