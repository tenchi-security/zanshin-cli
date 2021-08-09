# `zanshin`

Command-line utility to interact with the Zanshin SaaS service offered by Tenchi Security
(https://tenchisecurity.com), go to https://github.com/tenchi-security/zanshin-cli for license, source code and
documentation

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

* `alert_summary`: Lists alerts of organizations that the API...
* `alerts`: Lists alerts of organizations that the API...
* `list`: Lists other organizations that a specified...
* `requests`: Operations on requests submitted by third...
* `stop`: Stops one organization from following another

### `zanshin following alert_summary`

Lists alerts of organizations that the API key owner is following

**Usage**:

```console
$ zanshin following alert_summary [OPTIONS]
```

**Options**:

* `--following-id UUID`: Only summarize alerts from the specified followed organizations
* `--help`: Show this message and exit.

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

* `alert_summary`: List alerts from a given organization, with...
* `alerts`: List alerts from a given organization, with...
* `list`: Lists the organizations this user has direct...
* `scan_summary`: List statistical summaries of changes brought...
* `scan_target`: Operations on scan targets from organizations...

### `zanshin organization alert_summary`

List alerts from a given organization, with an optional filter by scan target.

**Usage**:

```console
$ zanshin organization alert_summary [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization  [required]

**Options**:

* `--scan-target-id UUID`: Only summarize alerts from the specified scan targets, defaults to all.
* `--help`: Show this message and exit.

### `zanshin organization alerts`

List alerts from a given organization, with optional filters by scan target, state or severity.

**Usage**:

```console
$ zanshin organization alerts [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization  [required]

**Options**:

* `--scan-target-id UUID`: Only list alerts from the specified scan targets.
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

### `zanshin organization scan_summary`

List statistical summaries of changes brought by scans from a given organization, with optional filters by scan target.

**Usage**:

```console
$ zanshin organization scan_summary [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization  [required]

**Options**:

* `--scan-target-id UUID`: Only summarize scans from the specified scan targets, defaults to all.
* `--days INTEGER RANGE`: [default: 7]
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

* `alert_summary`: List statistical summaries of changes brought...
* `alerts`: List alerts from a given scan target, with...
* `check`: Checks if a scan target is correctly...
* `list`: Lists the scan targets (i.e.
* `scan`: Starts an ad-hoc scan of a specified scan...
* `scan_summary`: Show summary of scans from a given scan...

#### `zanshin organization scan_target alert_summary`

List statistical summaries of changes brought by scans from a given scan target.

**Usage**:

```console
$ zanshin organization scan_target alert_summary [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the scan target's organization  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to summarize alerts from  [required]

**Options**:

* `--help`: Show this message and exit.

#### `zanshin organization scan_target alerts`

List alerts from a given scan target, with optional filters by state or severity.

**Usage**:

```console
$ zanshin organization scan_target alerts [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the scan target's organization  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to list alerts from  [required]

**Options**:

* `--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|RESOLVED|CLOSED]`: Only list alerts in the specified states.  [default: OPEN, ACTIVE, IN_PROGRESS, RISK_ACCEPTED, RESOLVED]
* `--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]`: Only list alerts with the specified severities  [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
* `--help`: Show this message and exit.

#### `zanshin organization scan_target check`

Checks if a scan target is correctly configured

**Usage**:

```console
$ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the scan target's organization  [required]
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

* `ORGANIZATION_ID`: UUID of the scan target's organization  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to start scan  [required]

**Options**:

* `--help`: Show this message and exit.

#### `zanshin organization scan_target scan_summary`

Show summary of scans from a given scan target.

**Usage**:

```console
$ zanshin organization scan_target scan_summary [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the scan target's organization  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to summarize alerts from  [required]

**Options**:

* `--days INTEGER RANGE`: [default: 7]
* `--help`: Show this message and exit.

## `zanshin version`

Display the program and Python versions in use.

**Usage**:

```console
$ zanshin version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
