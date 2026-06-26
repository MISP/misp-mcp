"""Galaxy and galaxy cluster tools."""


def register(mcp, get_client):
    """Register galaxy tools."""

    @mcp.tool()
    def search_galaxies(
        value: str,
        with_clusters: bool = False,
    ) -> dict:
        """Search MISP galaxies by name or description.

        Galaxies are knowledge bases of threat actors,
        malware, attack techniques (MITRE ATT&CK), tools,
        and other threat intelligence concepts.

        Args:
            value: Text to search for in galaxy names and
                descriptions
            with_clusters: Include cluster data in results
        """
        client = get_client()
        result = client.search_galaxy(
            value=value,
            withCluster=with_clusters,
            pythonify=False,
        )
        return result

    @mcp.tool()
    def get_galaxy(
        galaxy_id: int,
        with_clusters: bool = True,
    ) -> dict:
        """Get a specific galaxy with its clusters.

        Returns the galaxy definition and optionally all its
        clusters (e.g. all threat actors in the threat-actor
        galaxy).

        Args:
            galaxy_id: The galaxy ID to retrieve
            with_clusters: Include clusters (default True)
        """
        client = get_client()
        result = client.get_galaxy(
            galaxy_id,
            withCluster=with_clusters,
            pythonify=False,
        )
        return result

    @mcp.tool()
    def search_galaxy_clusters(
        galaxy_id: int,
        search_term: str | None = None,
        context: str | None = None,
    ) -> dict:
        """Search clusters within a specific galaxy.

        Clusters are individual entries in a galaxy, e.g.
        specific threat actors, malware families, or ATT&CK
        techniques.

        Args:
            galaxy_id: The galaxy ID to search within
            search_term: Text to search for in cluster names,
                descriptions, and synonyms
            context: Additional context filter
        """
        client = get_client()
        result = client.search_galaxy_clusters(
            galaxy=galaxy_id,
            searchall=search_term,
            context=context,
            pythonify=False,
        )
        return result

    @mcp.tool()
    def get_galaxy_cluster(
        galaxy_cluster_id: int,
    ) -> dict:
        """Get a specific galaxy cluster by ID.

        Clusters are individual galaxy entries, such as a
        threat actor, malware family, tool, or ATT&CK
        technique.

        Args:
            galaxy_cluster_id: The galaxy cluster ID to
                retrieve
        """
        client = get_client()
        result = client.get_galaxy_cluster(
            galaxy_cluster_id,
            pythonify=False,
        )
        return result

    @mcp.tool()
    def list_galaxy_clusters(
        galaxy_id: int,
    ) -> list[dict] | dict:
        """List clusters for a specific MISP galaxy.

        Args:
            galaxy_id: The galaxy ID whose clusters should be
                listed
        """
        client = get_client()
        result = client.search_galaxy_clusters(
            galaxy=galaxy_id,
            searchall=None,
            context="all",
            pythonify=False,
        )
        return result
