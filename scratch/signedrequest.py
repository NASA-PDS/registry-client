import argparse
import json
import os.path

import boto3
import requests
from botocore.credentials import Credentials
from opensearchpy import RequestsAWSV4SignerAuth


def parse_args() -> argparse.Namespace:
    args = argparse.ArgumentParser()
    args.add_argument('path', required=True)
    args.add_argument('-d', '--data', type=json.loads, default={}, help='placeholder')
    args.add_argument('-o', '--output', type=get_checked_filepath, default=None, help='placeholder')
    args.add_argument('-H', '--header', action='append', nargs='*', help='placeholder')

    return args.parse_args()


def get_checked_filepath(raw_filepath: str) -> str:
    """Confirm that a local path is valid and writable, and return the absolute path"""
    try:
        checked_filepath = os.path.abspath(raw_filepath)
    except ValueError as err:
        raise ValueError(f'Could not resolve valid filepath from "{raw_filepath}"')

    # raise OSError if not writable
    open(checked_filepath, 'w+')

    return checked_filepath


def get_credentials_via_cognito_userpass_flow(
        region: str,
        account_id: str,
        client_id: str,
        identity_pool_id: str,
        user_pool_id: str,
        username: str,
        password: str) -> Credentials:
    # Initialize a Cognito identity provider client
    idp_client = boto3.client('cognito-idp', region_name=region)
    id_client = boto3.client('cognito-identity', region_name=region)

    # Authenticate as cognito user-pool user
    response = idp_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        },
        ClientId=client_id
    )

    access_token = response['AuthenticationResult']['AccessToken']
    refresh_token = response['AuthenticationResult']['RefreshToken']
    id_token = response['AuthenticationResult']['IdToken']

    # Authenticate as identity-pool IAM identity
    response_identity_get_id = id_client.get_id(
        AccountId=account_id,
        IdentityPoolId=identity_pool_id,
        Logins={
            f'cognito-idp.{region}.amazonaws.com/{user_pool_id}': id_token
        }
    )
    identity_id = response_identity_get_id['IdentityId']

    # Obtain credentials for IAM identity
    response = id_client.get_credentials_for_identity(
        IdentityId=identity_id,
        Logins={
            f'cognito-idp.{idp_client.meta.region_name}.amazonaws.com/{user_pool_id}': id_token
        }
    )

    aws_access_key_id = response['Credentials']['AccessKeyId']
    aws_secret_access_key = response['Credentials']['SecretKey']
    aws_session_token = response['Credentials']['SessionToken']

    return Credentials(aws_access_key_id, aws_secret_access_key, aws_session_token)


if __name__ == '__main__':
    # config = configparser.ConfigParser()
    # config.read('./config.ini')

    cognito_user = os.environ['REQUEST_SIGNER_COGNITO_USER']
    cognito_password = os.environ['REQUEST_SIGNER_COGNITO_PASSWORD']

    aws_account_id = os.environ['REQUEST_SIGNER_AWS_ACCOUNT']
    aws_region = os.environ.get('AWS_REGION', 'us-west-2')
    client_id = os.environ['REQUEST_SIGNER_CLIENT_ID']
    user_pool_id = os.environ['REQUEST_SIGNER_USER_POOL_ID']
    identity_pool_id = os.environ['REQUEST_SIGNER_IDENTITY_POOL_ID']

    aoss_endpoint = os.environ['REQUEST_SIGNER_AOSS_ENDPOINT']
    TEST_REQ_PATH = '/en-delta-registry-refs/_search'
    TEST_REQ_BODY = {
        "query": {
            "match_all": {}
        }
    }

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

    url = f'{aoss_endpoint}{TEST_REQ_PATH}'
    body = json.dumps(TEST_REQ_BODY)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url=url, data=body, auth=auth, headers=headers)

