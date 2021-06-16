[![PyPI version shields.io](https://img.shields.io/pypi/v/zanshincli.svg)](https://pypi.python.org/pypi/zanshincli/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/zanshincli.svg)](https://pypi.python.org/pypi/zanshincli/)

# Zanshin CLI

This Python package provides a command-line utility to interact with the [API of the Zanshin SaaS service](https://api.zanshin.tenchisecurity.com) from [Tenchi Security](https://www.tenchisecurity.com).

Is it based on the Zanshin Python SDK available on [Github](https://github.com/tenchi-security/zanshin-sdk-python) and [PyPI](https://pypi.python.org/pypi/zanshinsdk/).

If you are a Zanshin customer and have any questions regarding the use of the service, its API or this command-line utility, please get in touch via e-mail at support {at} tenchisecurity {dot} com or via the support widget on the [Zanshin Portal](https://zanshin.tenchisecurity.com).

## Configuration File

The way the SDK and CLI handles credentials is by using a configuration file in the format created by the Python [RawConfigParser](https://docs.python.org/3/library/configparser.html#configparser.RawConfigParser) class. 

The file is located at `~/.tenchi/config`, where `~` is the [current user's home directory](https://docs.python.org/3/library/pathlib.html#pathlib.Path.home).

Each section is treated as a configuration profile, and the SDK and CLI will look for a section called `default` if another is not explicitly selected. 

These are the supported options:

* `api_key` (required) which contains the Zanshin API key obtained at the [Zanshin web portal](https://zanshin.tenchisecurity.com/my-profile).
* `user_agent` (optional) allows you to override the default user-agent header used by the SDK when making API requests.
* `api_url` (optional) directs the SDK and CLI to use a different API endpoint than the default (https://api.zanshin.tenchisecurity.com).

You can populate the file with the `zanshin init` command of the CLI tool. This is what a minimal configuration file would look like:
```ini
[default]
api_key = abcdefghijklmnopqrstuvxyz
```

## Using the CLI Utility

This package installs a command-line utility called `zanshin` built with the great [Typer](https://typer.tiangolo.com/) package.

You can obtain help by using the `--help` option.

Keep in mind that when options are present that expect multiple values, these need to be provided as multiple options. For example if you wanted to list an organization's alerts filtering by the OPEN and RISK_ACCEPTED states, this is the command you would use:
```shell
$ zanshin organization alerts d48edaa6-871a-4082-a196-4daab372d4a1 --state OPEN --state RISK_ACCEPTED
```

## Command Reference
