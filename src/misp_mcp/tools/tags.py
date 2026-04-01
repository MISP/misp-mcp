"""Tag and taxonomy tools."""


def register(mcp, get_client):
    """Register tag and taxonomy tools."""

    @mcp.tool()
    def search_tags(
        tagname: str,
        strict: bool = False,
    ) -> dict:
        """Search MISP tags by name.

        Tags are used to classify and filter events and
        attributes. Common tag formats include taxonomies
        (tlp:white), galaxies (misp-galaxy:threat-actor=
        "APT28"), and custom tags.

        Args:
            tagname: Tag name or partial name to search for
            strict: If True, match tag name exactly
        """
        client = get_client()
        result = client.search_tags(
            tagname=tagname,
            strict_tagname=strict,
            pythonify=False,
        )
        return result

    @mcp.tool()
    def list_taxonomies() -> list[dict]:
        """List all available MISP taxonomies.

        Taxonomies provide standardised tag vocabularies for
        classifying threat intelligence (e.g. TLP, admiralty
        scale, kill chain, CIRCL taxonomy).
        """
        client = get_client()
        result = client.taxonomies(pythonify=False)
        if isinstance(result, list):
            return result
        return [result]

    @mcp.tool()
    def get_taxonomy(taxonomy_id: int) -> dict:
        """Get a specific taxonomy with all its entries.

        Returns the full taxonomy including all predicates
        and values that can be used as tags.

        Args:
            taxonomy_id: The taxonomy ID to retrieve
        """
        client = get_client()
        result = client.get_taxonomy(
            taxonomy_id, pythonify=False
        )
        return result
