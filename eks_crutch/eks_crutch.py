"""Main module."""

import os
from typing import TypedDict, Union

import boto3


AnyPath = Union[str, bytes, os.PathLike]


class Credentials(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str


def assume_role(role_arn: str, session_name: str, token: str, duration: int = 3600) -> Credentials:
    sts = boto3.client('sts')
    r = sts.assume_role_with_web_identity(
        RoleArn = role_arn,
        RoleSessionName = session_name,
        WebIdentityToken = token)

    c = r['Credentials']
    return {
        'AccessKeyId': c['AccessKeyId'],
        'SecretAccessKey': c['SecretAccessKey'],
        'SessionToken': c['SessionToken']
    }


def read_token(path: AnyPath) -> str:
    with open(path, 'r') as fp:
        token = fp.read()

    return token


def get_environment(credentials: Credentials):
    return {
        'AWS_ACCESS_KEY_ID': credentials['AccessKeyId'],
        'AWS_SECRET_ACCESS_KEY': credentials['SecretAccessKey'],
        'AWS_SESSION_TOKEN': credentials['SessionToken']
    }
