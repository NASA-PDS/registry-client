"""run.py.

Command-line runner
"""
import argparse
import json
import os
import urllib.parse
from typing import Dict
from typing import Iterable

import requests
from opensearchpy import RequestsAWSV4SignerAuth
from pds.aossrequestsigner.credentials import get_credentials_via_cognito_userpass_flow
from pds.aossrequestsigner.utils import get_checked_filepath
from pds.aossrequestsigner.utils import parse_path
from pds.aossrequestsigner.utils import process_data_arg


def run(
        aws_region: str,
        aws_account_id: str,
        client_id: str,
        identity_pool_id: str,
        user_pool_id: str,
        cognito_user: str,
        cognito_password: str,
        aoss_endpoint: str,
        request_path: str,
        data: Dict = None,
        additional_headers: Iterable[str] = None,
        output_filepath: str = None,
        verbose: bool = False,
        silent: bool = False,
        prettify_output: bool = False,
):
    """Runner."""
    credentials = get_credentials_via_cognito_userpass_flow(
        aws_region, aws_account_id, client_id, identity_pool_id, user_pool_id, cognito_user, cognito_password
    )

    auth = RequestsAWSV4SignerAuth(credentials, aws_region, "aoss")

    url = urllib.parse.urljoin(aoss_endpoint, request_path)
    if verbose:
        print(f"Making request to url: {url}")

    body = json.dumps(data)
    if verbose:
        print(f"Including POST body: {body}")

    headers = {"Content-Type": "application/json"}
    for raw_header_str in additional_headers:
        k, v = raw_header_str.split(":", maxsplit=1)
        headers.update({k, v.strip()})
    if verbose:
        print(f"Including headers: {json.dumps(headers)}")

    response = requests.post(url=url, data=body, auth=auth, headers=headers)
    output = json.dumps(response.json(), indent=2) if prettify_output else json.dumps(response.json())

    if output_filepath is not None:
        if verbose:
            print(f"Writing response content to {output_filepath}")
        with open(output_filepath, "w+") as out_file:
            out_file.write(output)

    if not silent:
        print(output)


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    args = argparse.ArgumentParser()

    verbosity_group = args.add_mutually_exclusive_group()
    verbosity_group.add_argument("-v", "--verbose", action="store_true", help="Provide verbose stdout output")
    verbosity_group.add_argument("-s", "--silent", action="store_true", help="Suppress stdout output")

    args.add_argument(
        "path",
        type=parse_path,
        help=("either a full URL (<scheme>://<host>/<path>) or a host-relative path (/<path>) for the request. "
              "Providing a full URL will not override the host endpoint provided as an environment variable "
              "(this may change in future)"),
    )
    args.add_argument(
        "-d",
        "--data",
        type=process_data_arg,
        default={"query": {"match_all": {}}},
        help=("POST body to include in the request. Defaults to an OpenSearch match-all query.  "
              "See https://opensearch.org/docs/latest/query-dsl/ for details."),
    )
    args.add_argument(
        "-o",
        "--output",
        dest="output_filepath",
        type=get_checked_filepath,
        default=None,
        help="Output filepath for response content",
    )
    args.add_argument(
        "-H",
        "--header",
        dest="headers",
        default=[],
        action="append",
        nargs="*",
        help=('Add an extra header to use in the request, in format "Key: Value". "Content-Type: application/json" is '
              'included by default but may be overwritten.'),
    )

    args.add_argument("-p", "--pretty", action="store_true", help="Prettify output with a 2-space-indent JSON format")

    return args.parse_args()


def main():
    """Main."""
    args = parse_args()

    cognito_user = os.environ["REQUEST_SIGNER_COGNITO_USER"]
    cognito_password = os.environ["REQUEST_SIGNER_COGNITO_PASSWORD"]

    aws_account_id = os.environ["REQUEST_SIGNER_AWS_ACCOUNT"]
    aws_region = os.environ.get("AWS_REGION", "us-west-2")
    client_id = os.environ["REQUEST_SIGNER_CLIENT_ID"]
    user_pool_id = os.environ["REQUEST_SIGNER_USER_POOL_ID"]
    identity_pool_id = os.environ["REQUEST_SIGNER_IDENTITY_POOL_ID"]

    aoss_endpoint = os.environ["REQUEST_SIGNER_AOSS_ENDPOINT"]

    run(
        aws_region,
        aws_account_id,
        client_id,
        identity_pool_id,
        user_pool_id,
        cognito_user,
        cognito_password,
        aoss_endpoint,
        args.path,
        data=args.data,
        additional_headers=args.headers,
        output_filepath=args.output_filepath,
        verbose=args.verbose,
        silent=args.silent,
        prettify_output=args.pretty,
    )
