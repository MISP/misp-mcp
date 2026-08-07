# MISP MCP Server

An [MCP](https://modelcontextprotocol.io) server that provides read-only access to [MISP](https://www.misp-project.org/) threat intelligence data.

## Features

- **Event search** - Find threat intelligence events by IOC values, tags, dates, organisations
- **Attribute search** - Search individual indicators of compromise across all events
- **Object search** - Find grouped attributes (file objects, network connections, etc.)
- **Event index** - Lightweight event metadata browsing
- **Tags & Taxonomies** - Search tags and browse taxonomy vocabularies (TLP, kill chain, etc.)
- **Galaxies** - Search threat actors, malware, ATT&CK techniques, and other knowledge bases
- **Feeds** - Browse configured threat intelligence feeds

All access is **read-only** - no data modification is possible through this server.

## Installation

```bash
pip install misp-mcp
```

Or install from source:

```bash
cd misp-mcp
pip install -e .
```

## Configuration

Set the following environment variables:

| Variable | Required | Description |
|---|---|---|
| `MISP_URL` | Yes | URL of your MISP instance (e.g. `https://misp.example.com`) |
| `MISP_API_KEY` | Yes | Your MISP API authentication key |
| `MISP_VERIFYCERT` | No | Verify TLS certificates. `true`/`false`, or a path to a CA bundle file to verify against (default: `true`) |

## Usage

### Claude Desktop / Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "misp": {
      "command": "misp-mcp",
      "env": {
        "MISP_URL": "https://misp.example.com",
        "MISP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Standalone (stdio)

```bash
export MISP_URL="https://misp.example.com"
export MISP_API_KEY="your-api-key"
misp-mcp
```

## Available Tools

### Events & Attributes
- `search_events` - Search events by IOC values, tags, dates, organisations
- `search_attributes` - Search individual attributes/indicators
- `search_objects` - Search MISP objects
- `search_event_index` - Lightweight event metadata search
- `get_event` - Get full event by ID
- `get_attribute` - Get attribute by ID
- `get_object` - Get object by ID

### Tags & Taxonomies
- `search_tags` - Search tags by name
- `list_taxonomies` - List all taxonomy vocabularies
- `get_taxonomy` - Get taxonomy details and entries

### Galaxies
- `search_galaxies` - Search galaxies (threat actors, malware, ATT&CK, etc.)
- `get_galaxy` - Get galaxy with clusters
- `search_galaxy_clusters` - Search within a specific galaxy

### Feeds
- `search_feeds` - Search/list configured threat intelligence feeds

## License

AGPL-3.0-or-later - same as MISP.

Copyright (C) 2026 Andras Iklody
