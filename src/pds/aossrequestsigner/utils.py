import os
import urllib.parse


def parse_path(path_or_url: str) -> str:
    parsed_input = urllib.parse.urlparse(path_or_url)
    if parsed_input.netloc != '':
        return parsed_input.path
    elif path_or_url.startswith('/'):
        return path_or_url[1:]
    else:
        raise ValueError(f'Could not parse user input (expected either <scheme>://<host>/<path> or "/<path>", got {path_or_url}')

def get_checked_filepath(raw_filepath: str) -> str:
    """Confirm that a local path is valid and writable, and return the absolute path"""
    try:
        checked_filepath = os.path.abspath(raw_filepath)
    except ValueError as err:
        raise ValueError(f'Could not resolve valid filepath from "{raw_filepath}"')

    # raise OSError if not writable
    open(checked_filepath, 'w+')

    return checked_filepath
