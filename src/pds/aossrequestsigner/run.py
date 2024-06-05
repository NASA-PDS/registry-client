import json
import urllib.parse
from typing import Dict, Iterable

import requests
from opensearchpy import RequestsAWSV4SignerAuth

from pds.aossrequestsigner.credentials import get_credentials_via_cognito_userpass_flow


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
    credentials = get_credentials_via_cognito_userpass_flow(
        aws_region,
        aws_account_id,
        client_id,
        identity_pool_id,
        user_pool_id,
        cognito_user,
        cognito_password
    )

    auth = RequestsAWSV4SignerAuth(credentials, aws_region, 'aoss')

    url = urllib.parse.urljoin(aoss_endpoint, request_path)
    if verbose:
        print(f'Making request to url: {url}')

    body = json.dumps(data)
    if verbose:
        print(f'Including POST body: {body}')

    headers = {'Content-Type': 'application/json'}
    for raw_header_str in additional_headers:
        k, v = raw_header_str.split(':', maxsplit=1)
        headers.update({k, v.strip()})
    if verbose:
        print(f'Including headers: {json.dumps(headers)}')

    response = requests.post(url=url, data=body, auth=auth, headers=headers)
    output = json.dumps(response.json(), indent=2) if prettify_output else json.dumps(response.json())

    if output_filepath is not None:
        if verbose:
            print(f'Writing response content to {output_filepath}')
        with open(output_filepath, 'w+') as out_file:
            out_file.write(output)

    if not silent:
        print(output)
