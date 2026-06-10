import structlog

structlog.configure()

logger = structlog.get_logger()