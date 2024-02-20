#!/usr/bin/env python
"""
S3 Module
"""

import boto3
from .decorators import notify
from .config import config

@notify
def setup_s3():
    """
    S3 Setup session and set correct variables
    """
    s3_keys = {'s3_bucket', 's3_endpoint_url', 's3_directory'}

    env_vars ={}

    if not s3_keys <= config.get_active_config().keys():
        return False

    env_vars = {
        "s3_bucket": config.get_active_config()['s3_bucket'],
        "s3_endpoint": config.get_active_config()["s3_endpoint_url"],
        "s3_directory": config.get_active_config()["s3_directory"]
    }

    for var_name, value in env_vars.items():
        if value is None and value == "":
            raise Exception(f"Missing {var_name} from config or OS env var.")

    days_to_keep = config.get_active_config().get('days_to_keep', 30)

    session = boto3.Session()

    # Create an S3 client object using the session
    s3 = session.client('s3', endpoint_url=env_vars['s3_endpoint']) # pylint: disable=invalid-name

    return (s3, env_vars['s3_bucket'],
            env_vars['s3_directory'],
            days_to_keep,
            env_vars['s3_endpoint'])
