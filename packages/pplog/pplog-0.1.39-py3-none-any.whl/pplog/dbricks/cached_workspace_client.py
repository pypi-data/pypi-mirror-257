"""Hosts CachedWorkspaceClient"""

import functools
from typing import List

# pylint: disable=import-error
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.compute import (
    ClusterDetails,
    ClusterEvent,
    EventType,
    GetEventsOrder,
    ListNodeTypesResponse,
    NodeType,
)

from pplog.config import safe_access


class SimpleWorkspaceClient:
    """Calls DatabricksSDK with lru cache.

    This makes sure no duplicate calls are done to the API.
    """

    def __init__(self, workspace_client):
        """Initializes the static caching wrapper with a workspace client."""
        self.workspace_client = workspace_client

    def get_current_list_of_node_types(self) -> List[NodeType]:
        """Retrieve up-to-date list of node types from Databricks.

        This is necessary for two reasons:
            - Retrieving additional info, such as memory/CPU of each worker type
            - Checking whether we have unmapped nodes in the hardcoded DBU table.
        """
        node_types_response: ListNodeTypesResponse = (
            self.workspace_client.clusters.list_node_types()
        )
        return safe_access(node_types_response, "node_types")

    def get_cluster_details(self, cluster_id: str) -> ClusterDetails:
        """Retrieves cluster details using Databricks SDK."""
        return self.workspace_client.clusters.get(cluster_id)

    def get_cluster_events(
        self, cluster_id: str, start_timestamp_in_milliseconds: int
    ) -> List[ClusterEvent]:
        """Get cluster events (specially useful for auto-scaling)."""
        return list(
            self.workspace_client.clusters.events(
                cluster_id,
                start_time=start_timestamp_in_milliseconds,
                order=GetEventsOrder.DESC,
                event_types=[EventType.RUNNING, EventType.RESIZING, EventType.UPSIZE_COMPLETED],
            )
        )


@functools.lru_cache
def get_cached_workspace_client() -> SimpleWorkspaceClient:
    """Returns an initialized cached workspace client"""
    return SimpleWorkspaceClient(WorkspaceClient())
