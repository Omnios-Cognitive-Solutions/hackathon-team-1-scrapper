import logging

import boto3
from src.config import config
from src.wrappers.aws.exception import AWSException

logger = logging.getLogger(__name__)


@AWSException.error_handling
def initialize_boto3_session():
    """
    Initializes a boto3 session with the credentials found in AWS config variables.
    Only uses SESSION_TOKEN (for Lambda) or DEFAULT_REGION if they are set.

    :return: The boto3 session object
    """

    session_parameters = {
        "aws_access_key_id": config.get("AWS", "access_key_id"),
        "aws_secret_access_key": config.get("AWS", "secret_access_key"),
    }
    if config.get("AWS", "session_token") is not None:
        session_parameters["aws_session_token"] = config.get("AWS", "session_token")
    if config.get("AWS", "default_region") is not None:
        session_parameters["region_name"] = config.get("AWS", "default_region")

    session = boto3.Session(**session_parameters)

    return session


boto3_session = initialize_boto3_session()
