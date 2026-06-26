# MISP MCP API Gap Report

Generated on 2026-06-26 for the current `misp-mcp` working tree.

## Scope and baseline

This report compares the current MCP tool surface against the most relevant
read-only analyst capabilities in MISP. The server currently presents itself as
read-only, so create, update, delete, publish, enrichment execution, feed
fetching, synchronisation, worker control, and other side-effectful operations
are treated as out of scope rather than primary product gaps.

Reference baseline:

- Local implementation: `src/misp_mcp/server.py` and `src/misp_mcp/tools/`.
- MISP OpenAPI 2.5: `MISP/MISP` `app/webroot/doc/openapi.yaml`.
- PyMISP 2.5.34.1: installed `pymisp.PyMISP` public methods.
- MISP documentation: MISP concepts around events, attributes, objects, tags,
  taxonomies, galaxies, warninglists, sightings, feeds, and sharing context.
- `misp-modules`: separate module service for expansion, import, export, and
  workflow actions.

The MISP OpenAPI reference currently exposes 158 paths across 22 top-level
groups. This MCP server exposes 14 tools across parts of 7 MISP capability
groups.

## Current MCP surface

| Capability area | Current MCP tools | MISP/PyMISP coverage used | Notes |
|---|---|---|---|
| Events | `search_events`, `search_event_index`, `get_event` | `events/restSearch`, `events/index`, `events/view/{eventId}`; PyMISP `search`, `search_index`, `get_event` | Covers common event discovery and retrieval. Does not expose reports, sightings-only views, proposals, delegations, publication state changes, or event enrichment. |
| Attributes | `search_attributes`, `get_attribute` | `attributes/restSearch`, `attributes/view/{attributeId}`; PyMISP `search`, `get_attribute` | Covers IOC search and single attribute lookup. Missing type metadata, statistics, existence checks, base64 value lookup, proposals, restore, tagging, and enrichment. |
| Objects | `search_objects`, `get_object` | `objects/restsearch`, `objects/view/{objectId}`; PyMISP `search`, `get_object` | Covers object search and retrieval. Missing object templates and object-reference inspection. |
| Tags | `search_tags` | `tags/search/{tagSearchTerm}`; PyMISP `search_tags` | Search only. Missing tag listing and direct tag lookup. Mutating tag attach/detach is out of scope. |
| Taxonomies | `list_taxonomies`, `get_taxonomy` | `taxonomies`, `taxonomies/view/{taxonomyId}`; PyMISP `taxonomies`, `get_taxonomy` | Useful read-only baseline. Missing taxonomy tag export/listing helper. Enable/disable/update operations are out of scope. |
| Galaxies | `search_galaxies`, `get_galaxy`, `search_galaxy_clusters` | `galaxies`, `galaxies/view/{galaxyId}`, `galaxy_clusters/index/{galaxyId}`; PyMISP `search_galaxy`, `get_galaxy`, `search_galaxy_clusters` | Partially covers galaxies and clusters. Missing direct cluster view by cluster ID and explicit galaxy/cluster listing tools. |
| Feeds | `search_feeds` | `feeds`; PyMISP `feeds`, `search_feeds` | Covers listing/searching configured feeds. Missing direct feed view. Fetch/cache/enable/disable are out of scope. |

Current limits:

- The server has no explicit output normalization contract; tools mostly return
  raw PyMISP dictionaries/lists.
- Some implemented groups are partial: tags, feeds, galaxies/clusters,
  attributes, and objects all have useful read-only endpoints not yet exposed.
- The local `.env` available during validation contained `MISP_API_KEY` but not
  `MISP_URL`, so validation used the MISP host supplied in the task prompt.

## Primary read-only gaps

| Priority | Capability area | Relevant MISP/OpenAPI/PyMISP functions | Current `misp-mcp` coverage | Missing MCP tool candidates | Analyst use case | Evidence source |
|---|---|---|---|---|---|---|
| High | Sightings | OpenAPI `sightings/index/{eventId}`; PyMISP `sightings`, `search_sightings` | Only optional `include_sightings` embedded in event/attribute searches | `search_sightings`, `list_event_sightings`, `list_attribute_sightings` | Validate whether an IOC or event has been observed, where, and when without retrieving full event payloads. | OpenAPI `sightings`; PyMISP method support; live validation `search_sightings` returned `list[0]`. |
| High | Warninglists | OpenAPI `warninglists`, `warninglists/view/{warninglistId}`, `warninglists/checkValue`; PyMISP `warninglists`, `get_warninglist`, `values_in_warninglist` | `enforce_warninglist` can be passed into searches, but no direct warninglist inspection | `list_warninglists`, `get_warninglist`, `check_warninglist_values` | Explain why values are filtered or should be treated as benign/common infrastructure. | OpenAPI `warninglists`; PyMISP method support; live validation `warninglists` returned `list[119]`, value check returned `list[0]`. |
| High | Noticelists | OpenAPI `noticelists`, `noticelists/view/{noticelistId}`; PyMISP `noticelists`, `get_noticelist` | None | `list_noticelists`, `get_noticelist` | Surface legal, policy, or handling notices that affect interpretation of MISP data. | OpenAPI `noticelists`; PyMISP method support; live validation returned `list[1]`. |
| High | Event reports | OpenAPI `eventReports/view/{eventReportId}`, `eventReports/index`; PyMISP `get_event_reports`, `get_event_report` | `get_event` returns event data, but report-specific listing/view tools are absent | `list_event_reports`, `get_event_report` | Retrieve analyst-written event narratives, summaries, and linked report content. | OpenAPI `eventReports`; PyMISP method support. |
| High | Analyst data | OpenAPI `analystData/index/{analystType}`, `analystData/view/{analystType}/{analystDataID}`; PyMISP `get_analyst_data`, `get_note`, `get_opinion`, `get_relationship` | None | `get_analyst_note`, `get_analyst_opinion`, `get_analyst_relationship`, `search_analyst_data` | Inspect notes, opinions, and relationships attached to MISP entities for analyst context. | OpenAPI `analystData`; PyMISP method support. |
| High | Attribute metadata helpers | OpenAPI `attributes/describeTypes`, `attributes/attributeStatistics/{context}/{percentage}`, `attributes/getAttributeByB64Value/{base64Value}`; PyMISP `attributes_statistics`, `attribute_exists` | Attribute search and get-by-ID only | `describe_attribute_types`, `get_attribute_statistics`, `attribute_exists`, `get_attribute_by_base64_value` | Help agents choose valid attribute types/categories, summarize IOC distribution, and resolve encoded values. | OpenAPI `attributes`; PyMISP method support for statistics/existence. |
| High | Object templates | OpenAPI object-template support is present through MISP/PyMISP even though not prominent in the current path grouping; PyMISP `object_templates`, `get_object_template`, `get_raw_object_template` | Object search and get-by-ID only | `list_object_templates`, `get_object_template` | Understand expected object relations and fields before interpreting or creating object-shaped analysis. | PyMISP method support; live validation returned `list[374]`. |
| Medium | Galaxy cluster direct access | OpenAPI `galaxy_clusters/index/{galaxyId}`, `galaxy_clusters/view/{galaxyClusterId}`; PyMISP `get_galaxy_cluster`, `search_galaxy_clusters` | Search clusters inside a galaxy; no direct cluster lookup | `get_galaxy_cluster`, `list_galaxy_clusters` | Resolve a known cluster ID/UUID directly and inspect metadata, synonyms, and relationships. | OpenAPI `galaxy_clusters`; PyMISP method support. |
| Medium | Feed detail | OpenAPI `feeds`, `feeds/view/{feedId}`; PyMISP `feeds`, `get_feed`, `search_feeds` | Search/list feeds only | `get_feed` | Inspect a configured feed's source, provider, rules, distribution, and status without fetching it. | OpenAPI `feeds`; PyMISP method support; live validation `feeds` returned `list[2]`. |
| Medium | Tag list and direct tag view | OpenAPI `tags`, `tags/view/{tagId}`, `tags/search/{tagSearchTerm}`; PyMISP `tags`, `get_tag`, `search_tags` | Search tags only | `list_tags`, `get_tag` | Browse available tags and resolve exact tag metadata by ID. | OpenAPI `tags`; PyMISP method support. |
| Medium | Organisations | OpenAPI `organisations`, `organisations/view/{organisationId}`; PyMISP `organisations`, `get_organisation` | Organisation filters exist in searches, but organisation objects are not exposed | `list_organisations`, `get_organisation` | Interpret event ownership, creator organisations, and sharing context. | OpenAPI `organisations`; PyMISP method support; live validation returned `list[1]`. |
| Medium | Sharing groups | OpenAPI `sharing_groups`, `sharing_groups/view/{sharingGroupId}`; PyMISP `sharing_groups`, `get_sharing_group` | None | `list_sharing_groups`, `get_sharing_group` | Explain restricted distribution and who can see shared threat intelligence. | OpenAPI `sharing_groups`; PyMISP method support; live validation returned `list[0]`. |
| Medium | Server/version/status read-only summary | OpenAPI `servers`, `servers/serverSettings`, `servers/getWorkers`, `servers/getSetting/{settingName}`; PyMISP `servers`, `server_settings`, `get_server_setting`, `get_workers` | None | `get_misp_server_status`, `list_servers`, `get_server_setting` | Diagnose compatibility, enabled subsystems, and instance health before interpreting API behavior. | OpenAPI `servers`; PyMISP method support; live validation returned server/settings/workers dictionaries. |
| Low | Logs | OpenAPI `admin/logs`; PyMISP `search_logs` | None | `search_logs` | Audit analyst-relevant changes when permissions allow. This may expose sensitive administrative metadata, so default filters and permission notes are needed. | OpenAPI `admin/logs`; PyMISP method support; live validation returned `list[1]`. |
| Low | Communities | PyMISP `communities`, `get_community`, `request_community_access` | None | `list_communities`, `get_community` | Discover MISP community metadata. Access requests are out of scope. | PyMISP method support. |
| Low | Collections | OpenAPI `collections/view/{collectionId}`, `collections/index/{filter}` | None | `search_collections`, `get_collection` | Inspect curated collections if the instance uses them. | OpenAPI `collections`. |

## Secondary and out-of-scope gaps

| Area | MISP/PyMISP examples | Status for this MCP server |
|---|---|---|
| Event, attribute, object mutation | `add_event`, `update_event`, `delete_event`, `add_attribute`, `delete_attribute`, `add_object`, `delete_object`, tag attach/detach | Out of scope for the current read-only contract. |
| Publication and workflow state changes | `publish`, `unpublish`, `delegate_event`, proposal accept/discard methods | Out of scope because they change MISP state or workflow status. |
| Enrichment execution | `enrich_event`, `enrich_attribute` | Out of scope for the current report because enrichment can call external services and mutate or append results. A future design should treat this separately. |
| Feed operations with side effects | `fetch_feed`, `cache_feed`, `cache_all_feeds`, `enable_feed`, `disable_feed` | Out of scope. Read-only `get_feed` remains a valid gap. |
| Synchronisation and remote server operations | `server_pull`, `server_push`, `import_server`, `set_server_setting`, worker start/stop/restart/kill | Out of scope. Read-only server status remains a valid gap. |
| Admin identity and authorization | users, roles, auth keys, user settings, password reset, TOTP delete | Mostly out of scope. Read-only user/org visibility should only be considered if there is a clear analyst use case and permission model. |
| Blocklists and correlation exclusions | event blocklists, organisation blocklists, correlation exclusions | Mostly operational/admin. Could be revisited for investigative debugging, but not a primary analyst gap. |
| MISP modules | `misp-modules` expansion, import, export, hover, and workflow actions exposed by the separate modules service | Separate integration gap. It should not be mixed with core MISP API parity. A future MCP design could add module discovery and safe read-only expansion calls. |

## Live validation notes

Selective read-only validation was performed against `https://misp-dev.lo-res.org`
using PyMISP only. The local `.env` contained `MISP_API_KEY`; because it did not
contain `MISP_URL`, the validation script used the MISP host supplied in the task
prompt.

No write operations, enrichment execution, feed fetching, sync, worker control,
or admin mutations were performed.

| Capability checked | Result |
|---|---|
| Event metadata search | OK, returned `list[1]`. |
| Attribute search | OK, returned `dict` with `Attribute`. |
| Event index search | OK, returned `list[1]`. |
| Sightings search | OK, returned `list[0]`. |
| Warninglists list | OK, returned `list[119]`. |
| Warninglist value check | OK, returned `list[0]`. |
| Noticelists list | OK, returned `list[1]`. |
| Object templates list | OK, returned `list[374]`. |
| Galaxies list | OK, returned `list[122]`. |
| Organisations list | OK, returned `list[1]`. |
| Sharing groups list | OK, returned `list[0]`. |
| Feeds list | OK, returned `list[2]`. |
| Servers list | OK, returned `list[1]`. |
| Server settings | OK, returned keys including `version`, `phpSettings`, `gpgStatus`, `proxyStatus`, and `zmqStatus`. |
| Workers | OK, returned keys including `cache`, `default`, `email`, `prio`, and `update`. |
| Logs search | OK, returned `list[1]`. |

The attempted `PyMISP.test_server()` call was not used as evidence because the
installed PyMISP signature requires a server argument. Other server status calls
validated successfully.

## Recommended build order

1. Add high-value analyst context tools: sightings, warninglists, noticelists,
   event reports, and analyst data.
2. Fill metadata and schema helpers: attribute types/statistics/existence and
   object templates.
3. Complete partial existing groups: direct galaxy cluster lookup, feed view,
   tag list/view.
4. Add sharing context: organisations and sharing groups.
5. Add carefully scoped operational read-only tools: server status and logs,
   with conservative defaults and clear permission caveats.

## Source links

- MISP documentation: <https://www.misp-project.org/documentation/>
- MISP OpenAPI: <https://www.misp-project.org/openapi/>
- MISP OpenAPI source: <https://github.com/MISP/MISP/blob/2.5/app/webroot/doc/openapi.yaml>
- MISP core repository: <https://github.com/MISP/MISP>
- PyMISP repository: <https://github.com/MISP/PyMISP>
- MISP modules repository: <https://github.com/MISP/misp-modules>
