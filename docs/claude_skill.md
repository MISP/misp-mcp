# Setting up MISP MCP for Claude Code

A step-by-step guide to connect Claude Code to your MISP instance via the MCP server.

## Prerequisites

- A running MISP instance
- Your MISP API key (found under Administration > List Users or your user profile)
- Python 3.10+
- Claude Code installed

## Step 1: Install misp-mcp

Clone the repository and install in a virtualenv:

```bash
cd /path/to/misp-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Note the full path to the `misp-mcp` binary — you'll need it in the next step:

```bash
which misp-mcp
# e.g. /path/to/misp-mcp/venv/bin/misp-mcp
```

## Step 2: Add the MCP server to Claude Code

Run the following command, replacing the values with your own:

```bash
claude mcp add \
  --transport stdio \
  --scope project \
  --env MISP_URL=https://your-misp-instance \
  --env MISP_API_KEY=your-api-key-here \
  --env MISP_VERIFYCERT=true \
  misp \
  -- /path/to/misp-mcp/venv/bin/misp-mcp
```

### Example with a local dev instance

```bash
claude mcp add \
  --transport stdio \
  --scope project \
  --env MISP_URL=http://localhost:8080 \
  --env MISP_API_KEY=dHVxEx4WhIwRdS6QDVsBmW9PE6pOkmgIH1FPQWiC \
  --env MISP_VERIFYCERT=false \
  misp \
  -- /path/to/misp-mcp/venv/bin/misp-mcp
```

### Scope options

- `--scope project` — saves to `.mcp.json` in the project root (shared with team)
- `--scope user` — saves to `~/.claude.json` (personal, available across all projects)

For MISP API keys, `--scope user` is recommended to avoid committing secrets to git.

## Step 3: Start a new Claude Code session

```bash
claude
```

The MISP MCP server loads automatically when Claude Code starts. You can verify it's connected by running `/mcp` inside Claude Code.

## Step 4: Query MISP

You can now ask Claude to query your MISP instance using natural language:

- "Search MISP for events related to 192.168.1.1"
- "Find all events tagged tlp:white from the last 30 days"
- "Look up the threat actor APT28 in MISP galaxies"
- "What ATT&CK techniques are in the MISP galaxy?"
- "Search for MD5 hash abc123def456 in MISP attributes"
- "List the most recent high-threat events"
- "What taxonomies are available in MISP?"

## Managing the server

```bash
# List configured MCP servers
claude mcp list

# View details
claude mcp get misp

# Remove
claude mcp remove misp
```

## Troubleshooting

### Server not loading

1. Check `/mcp` in Claude Code — the server should appear in the list
2. Verify the path to `misp-mcp` is correct: run it manually and confirm it starts without errors
3. Start a fresh Claude Code session

### Connection errors

1. Verify your MISP instance is reachable: `curl -k https://your-misp-instance`
2. Check your API key is valid: `curl -k -H "Authorization: YOUR_KEY" https://your-misp-instance/servers/getVersion.json`
3. For self-signed certs, ensure `MISP_VERIFYCERT=false` is set

### Updating

```bash
cd /path/to/misp-mcp
git pull
source venv/bin/activate
pip install -e .
```

No need to reconfigure Claude Code — the next session will use the updated code.
