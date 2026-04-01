"""Tests for galaxy tools."""

import pytest


SAMPLE_GALAXY = {
    "Galaxy": {
        "id": "1",
        "name": "Threat Actor",
        "type": "threat-actor",
        "description": "Known threat actors",
    }
}

SAMPLE_CLUSTER = {
    "GalaxyCluster": {
        "id": "100",
        "value": "APT28",
        "description": "Fancy Bear",
        "galaxy_id": "1",
    }
}


class TestSearchGalaxies:
    @pytest.mark.asyncio
    async def test_search(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_galaxy.return_value = (
            SAMPLE_GALAXY
        )
        await mcp_server.call_tool(
            "search_galaxies", {"value": "threat actor"}
        )
        mock_pymisp.search_galaxy.assert_called_once_with(
            value="threat actor",
            withCluster=False,
            pythonify=False,
        )

    @pytest.mark.asyncio
    async def test_search_with_clusters(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_galaxy.return_value = (
            SAMPLE_GALAXY
        )
        await mcp_server.call_tool(
            "search_galaxies",
            {"value": "threat", "with_clusters": True},
        )
        call_kwargs = (
            mock_pymisp.search_galaxy.call_args[1]
        )
        assert call_kwargs["withCluster"] is True


class TestGetGalaxy:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_galaxy.return_value = (
            SAMPLE_GALAXY
        )
        await mcp_server.call_tool(
            "get_galaxy", {"galaxy_id": 1}
        )
        mock_pymisp.get_galaxy.assert_called_once_with(
            1, withCluster=True, pythonify=False
        )

    @pytest.mark.asyncio
    async def test_get_without_clusters(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.get_galaxy.return_value = (
            SAMPLE_GALAXY
        )
        await mcp_server.call_tool(
            "get_galaxy",
            {"galaxy_id": 1, "with_clusters": False},
        )
        call_kwargs = (
            mock_pymisp.get_galaxy.call_args[1]
        )
        assert call_kwargs["withCluster"] is False


class TestSearchGalaxyClusters:
    @pytest.mark.asyncio
    async def test_search_clusters(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_galaxy_clusters.return_value = (
            SAMPLE_CLUSTER
        )
        await mcp_server.call_tool(
            "search_galaxy_clusters",
            {"galaxy_id": 1, "search_term": "APT28"},
        )
        mock_pymisp.search_galaxy_clusters.assert_called_once_with(
            galaxy=1,
            searchall="APT28",
            context=None,
            pythonify=False,
        )

    @pytest.mark.asyncio
    async def test_search_without_term(
        self, mcp_server, mock_pymisp
    ):
        mock_pymisp.search_galaxy_clusters.return_value = (
            []
        )
        await mcp_server.call_tool(
            "search_galaxy_clusters", {"galaxy_id": 1}
        )
        call_kwargs = (
            mock_pymisp.search_galaxy_clusters.call_args[1]
        )
        assert call_kwargs["searchall"] is None
