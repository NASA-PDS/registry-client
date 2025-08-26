
# PDS Registry Client

This is a prototype implementation of a request-signing utility for use with serverless OpenSearch (AOSS).  It is
(currently) intended to provide a curl-like interface for querying PDS Registry's AOSS instance using a Cognito user
identity.

Additional functionality may be built out in the future.

## Prerequisites

- Personal user/pass credentials for a Cognito user authorized for Registry AOSS
- Python >=3.13
- Environment variables (contact developer for values)
  ```bash
    export REQUEST_SIGNER_AWS_ACCOUNT=''
    export REQUEST_SIGNER_AWS_REGION=''
    export REQUEST_SIGNER_CLIENT_ID=''
    export REQUEST_SIGNER_USER_POOL_ID=''
    export REQUEST_SIGNER_IDENTITY_POOL_ID=''
    export REQUEST_SIGNER_AOSS_ENDPOINT=''
    export REQUEST_SIGNER_COGNITO_USER=''
    export REQUEST_SIGNER_COGNITO_PASSWORD=''
  ```

## Developer Quickstart

1. Clone the repository
    ```
   git clone https://github.com/NASA-PDS/registry-client.git
   cd registry-client
    ```


2. Create a virtual environment
    ```
    python -m venv venv
    source ./venv/bin/activate
    ```

3. Install the tool to the virtual environment
    ```
    pip install --editable '.[dev]'
    ```

4. Run the tool directly
    ```
    registry-client --help
    ```

## Code of Conduct

All users and developers of the NASA-PDS software are expected to abide by our [Code of Conduct](https://github.com/NASA-PDS/.github/blob/main/CODE_OF_CONDUCT.md). Please read this to ensure you understand the expectations of our community.


## Development

To develop this project, use your favorite text editor, or an integrated development environment with Python support, such as [PyCharm](https://www.jetbrains.com/pycharm/).


### Contributing

For information on how to contribute to NASA-PDS codebases please take a look at our [Contributing guidelines](https://github.com/NASA-PDS/.github/blob/main/CONTRIBUTING.md).


### Installation

Install in editable mode and with extra developer dependencies into your virtual environment of choice:

    pip install --editable '.[dev]'

Make a baseline for any secrets (email addresses, passwords, API keys, etc.) in the repository:

    detect-secrets scan . \
        --all-files \
        --disable-plugin AbsolutePathDetectorExperimental \
        --exclude-files '\.secrets..*' \
        --exclude-files '\.git.*' \
        --exclude-files '\.mypy_cache' \
        --exclude-files '\.pytest_cache' \
        --exclude-files '\.tox' \
        --exclude-files '\.venv' \
        --exclude-files 'venv' \
        --exclude-files 'dist' \
        --exclude-files 'build' \
        --exclude-files '.*\.egg-info' > .secrets.baseline

Review the secrets to determine which should be allowed and which are false positives:

    detect-secrets audit .secrets.baseline

Please remove any secrets that should not be seen by the public. You can then add the baseline file to the commit:

    git add .secrets.baseline

Then, configure the `pre-commit` hooks:

    pre-commit install
    pre-commit install -t pre-push
    pre-commit install -t prepare-commit-msg
    pre-commit install -t commit-msg

These hooks then will check for any future commits that might contain secrets. They also check code formatting, PEP8 compliance, type hints, etc.

👉 **Note:** A one time setup is required both to support `detect-secrets` and in your global Git configuration. See [the wiki entry on Secrets](https://github.com/NASA-PDS/nasa-pds.github.io/wiki/Git-and-Github-Guide#detect-secrets) to learn how.


### Packaging

To isolate and be able to re-produce the environment for this package, you should use a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html). To do so, run:

    python -m venv venv

Then activate the environment (as shown above) which will set your shell's `$PATH` so that `python3` and `pip` are run out of it rather than the system's Python.

If you have `tox` installed and would like it to create your environment and install dependencies for you run:

    tox --devenv <name you'd like for env> -e dev

Or simply:

    tox

Dependencies for development are specified as the `dev` `extras_require` in `setup.cfg`. For the packaging details, see https://packaging.python.org/tutorials/packaging-projects/ as a reference.


### Tooling

The `dev` `extras_require` included in the template repo installs `flake8` (plus some plugins) and `mypy` along with default configuration for all of them. You can run all of these (and more!) with:

    tox -e lint


### Code Style

So that your code is readable, you should comply with the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/). Our code style is automatically enforced in via [black](https://pypi.org/project/black/) and [flake8](https://flake8.pycqa.org/en/latest/). See the [Tooling section](#-tooling) for information on invoking the linting pipeline.
