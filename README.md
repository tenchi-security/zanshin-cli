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
# `zanshin`

Command-line utility to interact with the Zanshin SaaS service offered by Tenchi Security, go to
https://github.com/tenchi-security/zanshin-cli for license, source code and documentation

**Usage**:

```console
$ zanshin [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--profile TEXT`: Configuration file section to read API key and configutation from  [default: default]
* `--format [json|table|csv|html]`: Output format to use for list operations  [default: json]
* `--verbose / --no-verbose`: Print timiing and other information to stderr  [default: True]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `alert`: Returns details about a specified alert
* `following`: Operations on organizations that are being...
* `init`: Update settings on configuration file.
* `me`: Show details about the owner of the API key...
* `organization`: Operations on organizations the API key owner...
* `version`: Display the program and Python versions in...

## `zanshin alert`

Returns details about a specified alert

**Usage**:

```console
$ zanshin alert [OPTIONS] ALERT_ID
```

**Arguments**:

* `ALERT_ID`: UUID of the alert to look up  [required]

**Options**:

* `--help`: Show this message and exit.

## `zanshin following`

Operations on organizations that are being followed by one of the organizations the API key owner is a member of

**Usage**:

```console
$ zanshin following [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `alerts`: Lists alerts of organizations that the API...
* `list`: Lists other organizations that a specified...
* `requests`: Operations on requests submitted by third...
* `stop`: Stops one organization from following another

### `zanshin following alerts`

Lists alerts of organizations that the API key owner is following

**Usage**:

```console
$ zanshin following alerts [OPTIONS]
```

**Options**:

* `--following-id UUID`: Only list alerts from the specified followed organizations
* `--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|RESOLVED|CLOSED]`: Only list alerts in the specified states.  [default: OPEN, ACTIVE, IN_PROGRESS, RISK_ACCEPTED, RESOLVED]
* `--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]`: Only list alerts with the specified severities  [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
* `--help`: Show this message and exit.

### `zanshin following list`

Lists other organizations that a specified organization is following

**Usage**:

```console
$ zanshin following list [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization  [required]

**Options**:

* `--help`: Show this message and exit.

### `zanshin following requests`

Operations on requests submitted by third parties to be followed by one of the organizations the API key owner is a member of

**Usage**:

```console
$ zanshin following requests [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `accept`: Accepts a request to follow another...
* `decline`: Declines a request to follow another...
* `list`: Lists all of the requests from organizations...

#### `zanshin following requests accept`

Accepts a request to follow another organization

**Usage**:

```console
$ zanshin following requests accept [OPTIONS] ORGANIZATION_ID FOLLOWING_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization that received the request  [required]
* `FOLLOWING_ID`: UUID of the organization that requested to be followed  [required]

**Options**:

* `--help`: Show this message and exit.

#### `zanshin following requests decline`

Declines a request to follow another organization

**Usage**:

```console
$ zanshin following requests decline [OPTIONS] ORGANIZATION_ID FOLLOWING_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization that received the request  [required]
* `FOLLOWING_ID`: UUID of the organization that requested to be followed  [required]

**Options**:

* `--help`: Show this message and exit.

#### `zanshin following requests list`

Lists all of the requests from organizations that want to be followed by a specified organization that the API key
owner is a member of

**Usage**:

```console
$ zanshin following requests list [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization that received the request  [required]

**Options**:

* `--help`: Show this message and exit.

### `zanshin following stop`

Stops one organization from following another

**Usage**:

```console
$ zanshin following stop [OPTIONS] ORGANIZATION_ID FOLLOWING_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the follower organization (which the API key owner must be a member of)  [required]
* `FOLLOWING_ID`: UUID of the followed organization  [required]

**Options**:

* `--help`: Show this message and exit.

## `zanshin init`

Update settings on configuration file.

**Usage**:

```console
$ zanshin init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `zanshin me`

Show details about the owner of the API key being used.

**Usage**:

```console
$ zanshin me [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `zanshin organization`

Operations on organizations the API key owner has direct access to

**Usage**:

```console
$ zanshin organization [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `alerts`: List alerts from a given organization, with...
* `list`: Lists the organizations this user has direct...
* `scan_target`: Operations on scan targets from organizations...

### `zanshin organization alerts`

List alerts from a given organization, with optional filters by scan target, state or severity.

**Usage**:

```console
$ zanshin organization alerts [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization  [required]

**Options**:

* `--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|RESOLVED|CLOSED]`: Only list alerts in the specified states.  [default: OPEN, ACTIVE, IN_PROGRESS, RISK_ACCEPTED, RESOLVED]
* `--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]`: Only list alerts with the specified severities  [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
* `--help`: Show this message and exit.

### `zanshin organization list`

Lists the organizations this user has direct access to as a member.

**Usage**:

```console
$ zanshin organization list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `zanshin organization scan_target`

Operations on scan targets from organizations the API key owner has direct access to

**Usage**:

```console
$ zanshin organization scan_target [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `check`: Checks if a scan target is correctly...
* `list`: Lists the scan targets (i.e.
* `scan`: Starts an ad-hoc scan of a specified scan...

#### `zanshin organization scan_target check`

Checks if a scan target is correctly configured

**Usage**:

```console
$ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization to list alerts from  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to start scan  [required]

**Options**:

* `--help`: Show this message and exit.

#### `zanshin organization scan_target list`

Lists the scan targets (i.e. linked cloud accounts) from an organization that user has access to as a member.

**Usage**:

```console
$ zanshin organization scan_target list [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organizations whose scan targets should be listed  [required]

**Options**:

* `--help`: Show this message and exit.

#### `zanshin organization scan_target scan`

Starts an ad-hoc scan of a specified scan target

**Usage**:

```console
$ zanshin organization scan_target scan [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization to list alerts from  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to start scan  [required]

**Options**:

* `--help`: Show this message and exit.

## `zanshin version`

Display the program and Python versions in use.

**Usage**:

```console
$ zanshin version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
