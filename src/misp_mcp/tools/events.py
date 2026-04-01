"""Event, attribute, and object search tools."""

from pymisp import PyMISP


def register(mcp, get_client):
    """Register event/attribute/object tools."""

    @mcp.tool()
    def search_events(
        value: str | None = None,
        type_attribute: str | None = None,
        category: str | None = None,
        org: str | None = None,
        tags: list[str] | None = None,
        event_tags: list[str] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        eventid: int | list[int] | None = None,
        eventinfo: str | None = None,
        published: bool | None = None,
        enforce_warninglist: bool | None = None,
        to_ids: bool | None = None,
        include_correlations: bool = False,
        include_sightings: bool = False,
        metadata: bool = False,
        limit: int = 25,
        page: int = 1,
        quick_filter: str | None = None,
    ) -> dict:
        """Search MISP events.

        Use this to find threat intelligence events matching
        specific criteria. Returns event data including
        attributes and objects.

        Args:
            value: Search by attribute value (IP, domain,
                hash, etc.)
            type_attribute: Filter by attribute type
                (ip-src, domain, md5, sha256, etc.)
            category: Filter by category (Network activity,
                Payload delivery, etc.)
            org: Filter by organisation name or ID
            tags: Filter by tags (e.g. tlp:white,
                misp-galaxy:threat-actor)
            event_tags: Filter specifically by event-level
                tags
            date_from: Events from date (YYYY-MM-DD)
            date_to: Events until date (YYYY-MM-DD)
            eventid: Specific event ID(s)
            eventinfo: Search in event info field
            published: Filter by published status
            enforce_warninglist: Only return values not on
                warninglists
            to_ids: Filter by IDS flag
            include_correlations: Include correlation data
            include_sightings: Include sighting data
            metadata: Only return event metadata (no
                attributes/objects)
            limit: Max results to return (default 25)
            page: Page number for pagination
            quick_filter: Quick text search across all fields
        """
        client = get_client()
        result = client.search(
            controller="events",
            value=value,
            type_attribute=type_attribute,
            category=category,
            org=org,
            tags=tags,
            event_tags=event_tags,
            date_from=date_from,
            date_to=date_to,
            eventid=eventid,
            eventinfo=eventinfo,
            published=published,
            enforce_warninglist=enforce_warninglist,
            to_ids=to_ids,
            include_correlations=include_correlations,
            include_sightings=include_sightings,
            metadata=metadata,
            limit=limit,
            page=page,
            quick_filter=quick_filter,
        )
        if isinstance(result, dict):
            return result
        return [
            e.to_dict() if hasattr(e, "to_dict") else e
            for e in result
        ]

    @mcp.tool()
    def search_attributes(
        value: str | None = None,
        type_attribute: str | None = None,
        category: str | None = None,
        org: str | None = None,
        tags: list[str] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        eventid: int | list[int] | None = None,
        published: bool | None = None,
        enforce_warninglist: bool | None = None,
        to_ids: bool | None = None,
        include_event_uuid: bool = True,
        include_event_tags: bool = False,
        include_correlations: bool = False,
        include_sightings: bool = False,
        include_decay_score: bool = False,
        limit: int = 50,
        page: int = 1,
    ) -> dict:
        """Search MISP attributes directly.

        Returns individual attributes (indicators) across all
        events. More granular than event search when looking
        for specific IOCs.

        Args:
            value: Attribute value to search for (IP, hash,
                domain, etc.)
            type_attribute: Attribute type (ip-src, ip-dst,
                domain, md5, sha256, url, email-src, etc.)
            category: Category filter
            org: Organisation filter
            tags: Tag filter
            date_from: From date (YYYY-MM-DD)
            date_to: To date (YYYY-MM-DD)
            eventid: Limit to specific event(s)
            published: Filter by event published status
            enforce_warninglist: Exclude warninglisted values
            to_ids: Filter by IDS flag
            include_event_uuid: Include parent event UUID
            include_event_tags: Include parent event tags
            include_correlations: Include correlations
            include_sightings: Include sightings
            include_decay_score: Include decay score
            limit: Max results (default 50)
            page: Page number
        """
        client = get_client()
        result = client.search(
            controller="attributes",
            value=value,
            type_attribute=type_attribute,
            category=category,
            org=org,
            tags=tags,
            date_from=date_from,
            date_to=date_to,
            eventid=eventid,
            published=published,
            enforce_warninglist=enforce_warninglist,
            to_ids=to_ids,
            include_event_uuid=include_event_uuid,
            include_event_tags=include_event_tags,
            include_correlations=include_correlations,
            include_sightings=include_sightings,
            include_decay_score=include_decay_score,
            limit=limit,
            page=page,
        )
        if isinstance(result, dict):
            return result
        return [
            a.to_dict() if hasattr(a, "to_dict") else a
            for a in result
        ]

    @mcp.tool()
    def search_objects(
        value: str | None = None,
        type_attribute: str | None = None,
        category: str | None = None,
        org: str | None = None,
        tags: list[str] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        eventid: int | list[int] | None = None,
        object_name: str | None = None,
        limit: int = 25,
        page: int = 1,
    ) -> dict:
        """Search MISP objects.

        Objects group related attributes together (e.g. a
        file object contains filename, hash, size).

        Args:
            value: Search by contained attribute value
            type_attribute: Filter by contained attribute type
            category: Category filter
            org: Organisation filter
            tags: Tag filter
            date_from: From date (YYYY-MM-DD)
            date_to: To date (YYYY-MM-DD)
            eventid: Limit to specific event(s)
            object_name: Filter by object template name
                (file, ip-port, domain-ip, email, etc.)
            limit: Max results (default 25)
            page: Page number
        """
        client = get_client()
        result = client.search(
            controller="objects",
            value=value,
            type_attribute=type_attribute,
            category=category,
            org=org,
            tags=tags,
            date_from=date_from,
            date_to=date_to,
            eventid=eventid,
            object_name=object_name,
            limit=limit,
            page=page,
        )
        if isinstance(result, dict):
            return result
        return [
            o.to_dict() if hasattr(o, "to_dict") else o
            for o in result
        ]

    @mcp.tool()
    def search_event_index(
        eventinfo: str | None = None,
        tags: list[str] | None = None,
        org: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        eventid: str | None = None,
        threatlevel: int | None = None,
        published: bool | None = None,
        analysis: int | None = None,
        timestamp: str | None = None,
        publish_timestamp: str | None = None,
        attribute: str | None = None,
        minimal: bool = False,
        sort: str | None = None,
        desc: bool | None = None,
        limit: int = 25,
        page: int = 1,
    ) -> dict:
        """Search the MISP event index (lightweight).

        Returns event metadata without full attribute/object
        data. Faster than search_events for browsing and
        filtering.

        Args:
            eventinfo: Search in event info/title
            tags: Filter by tags
            org: Filter by organisation
            date_from: From date (YYYY-MM-DD)
            date_to: To date (YYYY-MM-DD)
            eventid: Specific event ID
            threatlevel: Threat level (1=High, 2=Medium,
                3=Low, 4=Undefined)
            published: Published status filter
            analysis: Analysis level (0=Initial,
                1=Ongoing, 2=Complete)
            timestamp: Filter by last modification timestamp
            publish_timestamp: Filter by publish timestamp
            attribute: Search for events containing this
                attribute value
            minimal: Return minimal event data only
            sort: Sort field
            desc: Sort descending
            limit: Max results (default 25)
            page: Page number
        """
        client = get_client()
        result = client.search_index(
            eventinfo=eventinfo,
            tags=tags,
            org=org,
            date_from=date_from,
            date_to=date_to,
            eventid=eventid,
            threatlevel=threatlevel,
            published=published,
            analysis=analysis,
            timestamp=timestamp,
            publish_timestamp=publish_timestamp,
            attribute=attribute,
            minimal=minimal,
            sort=sort,
            desc=desc,
            limit=limit,
            page=page,
        )
        if isinstance(result, dict):
            return result
        return [
            e.to_dict() if hasattr(e, "to_dict") else e
            for e in result
        ]

    @mcp.tool()
    def get_event(
        event_id: int,
        include_correlations: bool = False,
        include_sightings: bool = False,
    ) -> dict:
        """Get a specific MISP event by ID.

        Returns the full event with all attributes, objects,
        tags, and metadata.

        Args:
            event_id: The event ID to retrieve
            include_correlations: Include correlation data
            include_sightings: Include sighting data
        """
        client = get_client()
        if include_correlations or include_sightings:
            result = client.search(
                controller="events",
                eventid=event_id,
                include_correlations=include_correlations,
                include_sightings=include_sightings,
                limit=1,
            )
            if isinstance(result, list) and result:
                e = result[0]
                return (
                    e.to_dict()
                    if hasattr(e, "to_dict")
                    else e
                )
            return result if isinstance(result, dict) else {}
        result = client.get_event(event_id, pythonify=False)
        return result

    @mcp.tool()
    def get_attribute(attribute_id: int) -> dict:
        """Get a specific MISP attribute by ID.

        Args:
            attribute_id: The attribute ID to retrieve
        """
        client = get_client()
        result = client.get_attribute(
            attribute_id, pythonify=False
        )
        return result

    @mcp.tool()
    def get_object(object_id: int) -> dict:
        """Get a specific MISP object by ID.

        Returns the object with all its attributes.

        Args:
            object_id: The object ID to retrieve
        """
        client = get_client()
        result = client.get_object(
            object_id, pythonify=False
        )
        return result
