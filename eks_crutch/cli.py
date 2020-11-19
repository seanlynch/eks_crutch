"""Console script for eks_crutch."""
import argparse
import getpass
import socket
import os
import sys

from . import eks_crutch


def main():
    """Console script for eks_crutch."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--token-path',
        default=None,
        help='Path to read OIDC token from'
    )
    parser.add_argument(
        '--session-name',
        default=None,
        help='Session name to use for AssumeRoleWithWebIdentity call'
    )
    parser.add_argument(
        '--duration',
        default=3600,
        help='Session duration in seconds'
    )
    parser.add_argument(
        '--role-arn',
        default=None,
        help='ARN of role to assume'
    )
    parser.add_argument('command')
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()

    session_name = args.session_name
    if session_name is None:
        user = getpass.getuser()
        hostname = socket.gethostname()
        session_name = '{}@{}'.format(user, hostname)

    role_arn = args.role_arn if args.role_arn is not None else os.environ['AWS_ROLE_ARN']
    token_path = str(args.token_path) if args.token_path is not None else os.environ['AWS_WEB_IDENTITY_TOKEN_FILE']

    token = eks_crutch.read_token(token_path)
    credentials = eks_crutch.assume_role(
        role_arn=role_arn,
        session_name=session_name,
        token=token,
        duration=args.duration
    )
    env = eks_crutch.get_environment(credentials)
    os.environ.update(env)
    os.execvp(args.command, [args.command] + args.args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
