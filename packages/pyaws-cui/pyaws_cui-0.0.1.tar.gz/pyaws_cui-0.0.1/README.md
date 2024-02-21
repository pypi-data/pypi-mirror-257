<div align="center">
    <img src="docs/assets/logo.png" alt="pyaws-logo-png">
</div>

<div align="center">
    <a href="https://badge.fury.io/py/pyaws_cui">
        <img src="https://badge.fury.io/py/pyaws_cui.svg" alt="pyaws-pypi-version">
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/license/j-lavender/pyaws_cui.svg" alt="pyaws-license">
    </a>
</div>

# pyaws_cui (pyaws)

A Python based Command User Interface for viewing AWS resource detail information.

### Prologue

Built using the [py_cui](https://github.com/jwlodek/py_cui) framework, with direct porting from [pyautogit](https://github.com/jwlodek/pyautogit). Many thanks to [Jakub Wlodek](https://github.com/jwlodek/) for the fantastic library and example application to work from!

This is my first attempt at a larger scale application. As such, this is obviously a work-in-progress. Feel free to contribute or provide feedback.

## Installation

To install `pyaws_cui`, use pip:

```
pip install pyaws-cui

pyaws
```

Since `py_cui` is a dependency for this application, it will be installed as well. As noted by their documentation, if the user is on a windows machine, `windows-curses`, a `curses` emulator, will also be installed.

#### Build from source:

```
git clone https://github.com/j-lavender/pyaws_cui.git
cd pyaws_cui
pip install .
```

## Usage

This application assumes the user has an active AWS account with credential profiles located in `~/.aws/credentials`. While this application uses the Boto3 library to perform AWS actions, it is assumed the user has the AWS CLI installed locally.

Ensure that AWS Credential file exists at `~/.aws/credentials` and contains at least one profile. `awscui` supports credential files containing multiple profiles.

To start, navigate to any working directory (for example, a Terraform directory associtated with a specific AWS profile), and run the application:
```
pyaws
```

### Demo

<div align="center">
    <img src="docs/assets/demo.gif" alt="pyaws-demo-gif">
</div>

<br>

When starting the application in any directory for the first time, the Account Selection screen will be shown. This provides the user with the ability to select which profile to access.

Upon selection of a profile, the Console Selection screen is shown providing the user with a list of possible consoles to view, as well as a Region selection list. _By default, first region selected is `us-east-1`._

Current Profile and Region selection is saved to `$PWD/.pyaws/metadata.json` upon exit. Whenever the application is loaded again in the same directory, the previously selected Profile and Region are used by default and the Console Select screen will be displayed.

### Helper Args

- `-h` - Show help menu.
- `-d` - Debug mode. Prints logs to `.pyaws/`.
- `-n` - Do not save metadata changes on exit (region, profile, logging).
- `-p` - Set the Default Profile on start.
- `-r` - Set the Default Region on start.

### Supported AWS Resources

- EC2
  - Instances
  - Images
  - Volumes
  - Snapshots
  - Security Groups
  - Key Pairs
  - Elastic IPs
  - Load Balancers
  - Target Groups
  - Launch Templates
  - Auto Scaling Groups
- IAM
  - Users
  - Groups
  - Roles
  - Policies
- Route53
  - Hosted Zones
- Secrets Manager
  - Multi-version support
- Systems Manager
  - Paramater Store


## Local Development

### Setup

For local development and testing, I have been using [LocalStack](https://www.localstack.cloud/) to simulate AWS resources. While not required, Using the free version of this cool can be much cheaper than creating resources in an AWS account. That said, I'd recommend using this if possible.

Ensure LocalStack CLI is installed: https://docs.localstack.cloud/getting-started/installation/  _No auth key or account required. Only simple installation necessary._

Once LocalStack is installed, make sure `~/.aws/credentials` exists, along with a LocalStack profile exists.
```
[localstack]
aws_access_key_id = test
aws_secret_access_key = 123
endpoint_url = http://localhost:4566
```

The simple bash script located in `scripts/` can be used to generate some testing resources. Use the number designation to specify how many of each resource to create (applies to specific resources).
```
./scripts/setupLocalstack.sh 2
```

### Run

Run the application similary to the process for building the application from source. It is recommended to build this in a Python Virtual Environment to provide a local editable installation in the cloned directory.

```
git clone https://github.com/j-lavender/pyaws_cui.git
cd pyaws_cui
pip install -e .
pyaws -d
```

### Generate documentation

To re-generate the auto-generated documentation, use the script located in `docs/scripts`:
```
cd docs/scripts/
./generateFromDocstrings.sh
```

## License

BSD 3-Clause License

Copyright (c) 2024, James Lavender
All rights reserved.