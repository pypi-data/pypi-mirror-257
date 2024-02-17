"""Module for getting a splunk handler inside Databricks environment."""

# pylint: disable=no-name-in-module, import-error
from azure.eventgrid import EventGridPublisherClient
from pyspark.dbutils import DBUtils  # type: ignore

from pplog.azure import get_event_grid_published_client
from pplog.config import get_ppconfig
from pplog.dbricks import get_databricks_log_properties
from pplog.handlers.splunk_handler import SplunkHandler

from typing import Optional, Union


def get_splunk_handler_databricks(
    dbutils: DBUtils,
    event_type: str,
    custom_log_properties: Optional[Union[dict, None]] = None,
) -> SplunkHandler:
    """Returns a SplunkHandler instance

    Args:
        dbutils (DBUtils): Databricks Utilities instance
        event_type (str): Splunk Event identifier
        custom_log_properties (Optional[dict]): additional dynamic properties
        level (str): level of events the handler will consider

    Returns:
        SplunkHandler: Splunk Handler Instance
    """
    prj_config = get_ppconfig()
    custom_properties: dict = get_databricks_log_properties(dbutils)

    # Merge arguments with default properties
    if custom_log_properties:
        custom_properties = {**custom_properties, **custom_log_properties}


    event_grid_published_client: EventGridPublisherClient = get_event_grid_published_client(
        prj_config, dbutils
    )

    splunk_handler = SplunkHandler(event_grid_published_client, event_type, custom_properties)
    splunk_handler.set_name(name="uapc-splunk")
    return splunk_handler
