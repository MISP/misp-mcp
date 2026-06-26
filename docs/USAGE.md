# Usage Guide

This document describes all available tools and how to use them effectively with an AI assistant.

## Overview

The MISP MCP server provides read-only access to threat intelligence stored in MISP. All tools query the MISP REST API via PyMISP and return JSON data.

## Tools

### Event Search

#### `search_events`

Search for threat intelligence events by IOC values, tags, dates, and other criteria. Returns full event data including attributes and objects.

**Key parameters:**

| Parameter | Type | Description |
|---|---|---|
| `value` | string | IOC value to search for (IP, domain, hash, URL, email) |
| `type_attribute` | string | Attribute type filter (see [Attribute Types](#attribute-types)) |
| `category` | string | Category filter (see [Categories](#categories)) |
| `org` | string | Organisation name or ID |
| `tags` | list[string] | Tag filter (e.g. `["tlp:white", "misp-galaxy:threat-actor=\"APT28\""]`) |
| `date_from` | string | Start date (`YYYY-MM-DD`) |
| `date_to` | string | End date (`YYYY-MM-DD`) |
| `eventinfo` | string | Search in event title/info field |
| `published` | bool | Filter by published status |
| `enforce_warninglist` | bool | Exclude values matching warninglists |
| `to_ids` | bool | Filter by IDS export flag |
| `metadata` | bool | Return only event metadata (faster) |
| `limit` | int | Max results (default: 25) |
| `page` | int | Page number for pagination |

**Example prompts:**
- "Search MISP for events related to 192.168.1.1"
- "Find events tagged tlp:white from the last 30 days"
- "Search for events containing SHA256 hashes related to ransomware"

---

#### `search_event_index`

Lightweight event metadata search. Faster than `search_events` when you only need event summaries without full attribute/object data.

**Key parameters:**

| Parameter | Type | Description |
|---|---|---|
| `eventinfo` | string | Search in event title |
| `tags` | list[string] | Tag filter |
| `org` | string | Organisation filter |
| `date_from` / `date_to` | string | Date range |
| `threatlevel` | int | 1=High, 2=Medium, 3=Low, 4=Undefined |
| `analysis` | int | 0=Initial, 1=Ongoing, 2=Complete |
| `published` | bool | Published status |
| `minimal` | bool | Return minimal data only |
| `limit` | int | Max results (default: 25) |

**Example prompts:**
- "List the most recent high-threat events in MISP"
- "How many events are still in initial analysis?"

---

#### `get_event`

Retrieve a specific event by ID with full details.

| Parameter | Type | Description |
|---|---|---|
| `event_id` | int | **Required.** Event ID |
| `include_correlations` | bool | Include correlated attributes |
| `include_sightings` | bool | Include sighting data |

---

#### `list_event_reports`

List analyst-written reports attached to an event.

| Parameter | Type | Description |
|---|---|---|
| `event_id` | int | **Required.** Event ID |

---

#### `get_event_report`

Retrieve a specific event report by ID.

| Parameter | Type | Description |
|---|---|---|
| `event_report_id` | int | **Required.** Event report ID |

---

### Attribute Search

#### `search_attributes`

Search individual indicators of compromise (IOCs) across all events. More granular than event search for finding specific indicators.

**Key parameters:**

| Parameter | Type | Description |
|---|---|---|
| `value` | string | Attribute value (IP, hash, domain, etc.) |
| `type_attribute` | string | Attribute type filter |
| `category` | string | Category filter |
| `tags` | list[string] | Tag filter |
| `date_from` / `date_to` | string | Date range |
| `eventid` | int or list[int] | Limit to specific event(s) |
| `to_ids` | bool | IDS export flag filter |
| `include_correlations` | bool | Include correlations |
| `include_decay_score` | bool | Include decay scoring |
| `limit` | int | Max results (default: 50) |

**Example prompts:**
- "Search MISP for the IP address 8.8.8.8"
- "Find all MD5 hashes added in the last week"
- "Are there any attributes correlated with this SHA256?"

---

#### `get_attribute`

Retrieve a specific attribute by ID.

| Parameter | Type | Description |
|---|---|---|
| `attribute_id` | int | **Required.** Attribute ID |

---

#### `describe_attribute_types`

Describe valid MISP attribute types and categories.

No parameters.

---

#### `get_attribute_statistics`

Get aggregate attribute statistics by type or category.

| Parameter | Type | Description |
|---|---|---|
| `context` | string | `type` or `category` (default: `type`) |
| `percentage` | bool | Return percentages instead of counts |

---

#### `attribute_exists`

Check whether an attribute exists by ID or UUID.

| Parameter | Type | Description |
|---|---|---|
| `attribute_id` | int or string | **Required.** Attribute ID or UUID |

---

#### `get_attribute_by_base64_value`

Retrieve an attribute by its base64-encoded value.

| Parameter | Type | Description |
|---|---|---|
| `base64_value` | string | **Required.** Base64-encoded attribute value |

---

### Object Search

#### `search_objects`

Search MISP objects (grouped attributes like file objects, network connections).

**Key parameters:**

| Parameter | Type | Description |
|---|---|---|
| `value` | string | Search by contained attribute value |
| `type_attribute` | string | Filter by contained attribute type |
| `object_name` | string | Object template name (e.g. `file`, `ip-port`, `domain-ip`, `email`) |
| `eventid` | int or list[int] | Limit to specific event(s) |
| `limit` | int | Max results (default: 25) |

**Example prompts:**
- "Find all file objects in MISP containing this hash"
- "Search for domain-ip objects related to example.com"

---

#### `get_object`

Retrieve a specific object by ID with all its attributes.

| Parameter | Type | Description |
|---|---|---|
| `object_id` | int | **Required.** Object ID |

---

### Tags

#### `search_tags`

Search tags by name. Tags classify events and attributes using standardised vocabularies.

| Parameter | Type | Description |
|---|---|---|
| `tagname` | string | **Required.** Tag name or partial name |
| `strict` | bool | Exact match (default: false) |

**Example prompts:**
- "What TLP tags are available in MISP?"
- "Search for tags related to ransomware"

---

#### `list_tags`

List all available tags.

| Parameter | Type | Description |
|---|---|---|
| `limit` | int | Max results (default: 100) |
| `page` | int | Page number for pagination |

---

#### `get_tag`

Retrieve a specific tag by ID.

| Parameter | Type | Description |
|---|---|---|
| `tag_id` | int | **Required.** Tag ID |

---

### Taxonomies

#### `list_taxonomies`

List all available taxonomy vocabularies. Taxonomies provide standardised classification schemes (TLP, admiralty scale, kill chain, etc.).

No parameters.

---

#### `get_taxonomy`

Get a specific taxonomy with all its predicates and values.

| Parameter | Type | Description |
|---|---|---|
| `taxonomy_id` | int | **Required.** Taxonomy ID |

---

### Galaxies

#### `search_galaxies`

Search MISP galaxies — knowledge bases of threat actors, malware families, ATT&CK techniques, tools, and more.

| Parameter | Type | Description |
|---|---|---|
| `value` | string | **Required.** Search term |
| `with_clusters` | bool | Include cluster data (default: false) |

**Example prompts:**
- "Search MISP galaxies for MITRE ATT&CK"
- "Find the threat actor galaxy"

---

#### `get_galaxy`

Get a specific galaxy with its clusters.

| Parameter | Type | Description |
|---|---|---|
| `galaxy_id` | int | **Required.** Galaxy ID |
| `with_clusters` | bool | Include clusters (default: true) |

---

#### `search_galaxy_clusters`

Search within a specific galaxy for individual entries (e.g. specific threat actors, malware families, ATT&CK techniques).

| Parameter | Type | Description |
|---|---|---|
| `galaxy_id` | int | **Required.** Galaxy ID to search within |
| `search_term` | string | Text to search in names, descriptions, synonyms |
| `context` | string | Additional context filter |

**Example prompts:**
- "Search the threat actor galaxy for APT28"
- "Find ATT&CK techniques related to credential dumping"
- "Look up the Emotet malware in MISP galaxies"

---

#### `get_galaxy_cluster`

Retrieve a specific galaxy cluster by ID.

| Parameter | Type | Description |
|---|---|---|
| `galaxy_cluster_id` | int | **Required.** Galaxy cluster ID |

---

#### `list_galaxy_clusters`

List all clusters for a specific galaxy.

| Parameter | Type | Description |
|---|---|---|
| `galaxy_id` | int | **Required.** Galaxy ID |

---

### Feeds

#### `search_feeds`

Search or list configured threat intelligence feeds.

| Parameter | Type | Description |
|---|---|---|
| `value` | string | Search term (omit to list all feeds) |

---

## Reference

### Attribute Types

Common MISP attribute types:

| Type | Description | Example |
|---|---|---|
| `ip-src` | Source IP address | `192.168.1.1` |
| `ip-dst` | Destination IP address | `10.0.0.1` |
| `domain` | Domain name | `example.com` |
| `hostname` | Hostname | `mail.example.com` |
| `url` | URL | `https://evil.com/malware` |
| `md5` | MD5 hash | `d41d8cd98f00b204e9800998ecf8427e` |
| `sha1` | SHA1 hash | `da39a3ee5e6b...` |
| `sha256` | SHA256 hash | `e3b0c44298fc...` |
| `email-src` | Sender email | `attacker@evil.com` |
| `email-dst` | Recipient email | `victim@target.com` |
| `filename` | File name | `malware.exe` |
| `mutex` | Mutex name | `Global\MalwareMutex` |
| `regkey` | Registry key | `HKLM\Software\...` |

### Categories

Common MISP attribute categories:

- **Network activity** — IPs, domains, URLs, user-agents
- **Payload delivery** — Hashes, filenames, email attachments
- **Payload installation** — Installed malware indicators
- **Persistence mechanism** — Registry keys, scheduled tasks
- **External analysis** — Links to analysis reports
- **Attribution** — Threat actor identifiers
- **Artifacts dropped** — Files, registry changes left by malware

### Tag Formats

- **Taxonomy tags**: `namespace:predicate="value"` (e.g. `tlp:white`, `admiralty-scale:source-reliability="a"`)
- **Galaxy tags**: `misp-galaxy:galaxy-type="cluster-value"` (e.g. `misp-galaxy:threat-actor="APT28"`)
- **Custom tags**: Free-form text (e.g. `ransomware`, `apt`)

### Pagination

All search tools support `limit` and `page` parameters. To iterate through results:

1. First call with default `limit` and `page=1`
2. If you receive `limit` results, there may be more — increment `page`
3. Continue until fewer than `limit` results are returned
