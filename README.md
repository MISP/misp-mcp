# MISP MCP Server

An [MCP](https://modelcontextprotocol.io) server that provides read-only access to [MISP](https://www.misp-project.org/) threat intelligence data.

Start with [INSTALL.md](INSTALL.md) for architecture, MISP connection setup, and MCP client configuration examples for Codex, Claude Code, opencode.ai, and Raspberry Pi deployments.

## Features

- **Event search** - Find threat intelligence events by IOC values, tags, dates, organisations
- **Attribute search** - Search individual indicators of compromise across all events
- **Event reports** - Retrieve analyst-written reports attached to events
- **Attribute metadata** - Inspect attribute types, statistics, existence, and encoded values
- **Object search** - Find grouped attributes (file objects, network connections, etc.)
- **Event index** - Lightweight event metadata browsing
- **Tags & Taxonomies** - List, view, and search tags; browse taxonomy vocabularies
- **Galaxies** - Search galaxies and inspect galaxy clusters directly
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
| `MISP_VERIFYCERT` | No | Verify TLS certificates (default: `true`) |
| `MISP_TIMEOUT` | No | PyMISP request timeout in seconds (default: `30`) |

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
        "MISP_API_KEY": "your-api-key-here",
        "MISP_TIMEOUT": "30"
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
- `list_event_reports` - List reports attached to an event
- `get_event_report` - Get an event report by ID
- `describe_attribute_types` - Describe valid attribute types and categories
- `get_attribute_statistics` - Get aggregate attribute statistics
- `attribute_exists` - Check whether an attribute exists
- `get_attribute_by_base64_value` - Resolve an attribute from a base64-encoded value

### Tags & Taxonomies
- `search_tags` - Search tags by name
- `list_tags` - List all tags
- `get_tag` - Get tag details by ID
- `list_taxonomies` - List all taxonomy vocabularies
- `get_taxonomy` - Get taxonomy details and entries

### Galaxies
- `search_galaxies` - Search galaxies (threat actors, malware, ATT&CK, etc.)
- `get_galaxy` - Get galaxy with clusters
- `search_galaxy_clusters` - Search within a specific galaxy
- `get_galaxy_cluster` - Get a galaxy cluster by ID
- `list_galaxy_clusters` - List clusters for a galaxy

### Feeds
- `search_feeds` - Search/list configured threat intelligence feeds

## License

AGPL-3.0-or-later - same as MISP.

Copyright (C) 2026 Andras Iklody
