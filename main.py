import logging

logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info("It works!")


if __name__ == "__main__":
    handler({}, {})
