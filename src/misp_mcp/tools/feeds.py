"""Feed tools."""


def register(mcp, get_client):
    """Register feed tools."""

    @mcp.tool()
    def search_feeds(
        value: str | None = None,
    ) -> list[dict]:
        """Search MISP feeds.

        Feeds are external sources of threat intelligence
        that MISP can pull data from (OSINT feeds, commercial
        feeds, other MISP instances).

        Args:
            value: Search term to filter feeds by name or URL
        """
        client = get_client()
        if value:
            result = client.search_feeds(
                value=value, pythonify=False
            )
        else:
            result = client.feeds(pythonify=False)
        if isinstance(result, list):
            return result
        return [result]
