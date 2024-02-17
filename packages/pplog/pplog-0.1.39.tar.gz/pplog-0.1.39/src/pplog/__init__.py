""" Logging config method """
import logging
import logging.config

from pplog.config import get_ppconfig


#  pylint:disable=line-too-long
#  Adapted from UAPC-TPL
def setup_pplog(**kwargs):
    """Set basic logging configuration.
    Configuration of the root logger to log any message to stdout.
    Configuration of the "project" logger with or without (depending on the logging_conf) SplunkHandler which sends
    custom logs to Splunk. Since project logger is a child of root logger all messages send via that logger are also
    send to stdout.
    Python logging module organizes loggers in a hierarchy. All loggers are descendants of the root logger.
    Each logger passes log messages on to its parent. Which means if you create module level loggers using the
    logging.getLogger("__name__") approach they are configured to send logs (depending on the logging_conf) to Splunk.
    Kwargs (Optional):
        conifg (dict): logging configuration to overwrite existing project configuration
        dbutils (DBUtils): databricks utilites class instance - needed for splunk handler
        custom_log_properties (dict): custom splunk properties

    """
    project_config = get_ppconfig()

    pplogging_conf = kwargs.get("config") or project_config["logging"]

    #  this function can be refactored to a class once we have more use cases
    if project_config.get("splunk_integration"):
        try:
            pplogging_conf["handlers"]["splunk"]["dbutils"] = kwargs["dbutils"]
        except KeyError as exp:
            raise KeyError(
                "setup_pplog() needs a DBUtils instance keyword argument to setup a splunk handler"
            ) from exp

    if (custom_log_properties:=kwargs.get("custom_log_properties")):
        pplogging_conf["handlers"]["splunk"]["custom_log_properties"] = custom_log_properties

    #  Setup logging
    logging.config.dictConfig(pplogging_conf)

    #  Set 3rd party loggers at ERROR level
    spark_logger = logging.getLogger("py4j.java_gateway")
    spark_logger.setLevel(logging.ERROR)

    spark_logger = logging.getLogger("azure.core")
    spark_logger.setLevel(logging.ERROR)

    #  Reporting
    project_logger_name = __name__.rsplit(".", maxsplit=1)[
        0
    ]  # assuming __name__ is used for module level logger names
    project_logger = logging.getLogger(project_logger_name)
    project_logger.info("PPlogging initialized!")
