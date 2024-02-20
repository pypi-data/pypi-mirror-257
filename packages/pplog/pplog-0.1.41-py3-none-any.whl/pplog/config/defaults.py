""" Default setup_pplog config """

_DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            # pylint: disable-next=line-too-long
            "format": "%(asctime)s - %(name)s - [%(levelname)s] - [%(filename)s:%(lineno)d] [%(funcName)s] - %(message)s"  
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "splunk": {
            "()": "pplog.handlers.get_splunk_handler_databricks",
            "level": "INFO",
            "event_type": "<your_project_event_type>",
        },
    },
    "loggers": {
        "py4j.java_gateway": {"level": "ERROR", "propagate": True},
        "azure.core": {"level": "ERROR", "propagate": True},
    },
    "root": {"level": "DEBUG", "handlers": ["console", "splunk"]},
}
