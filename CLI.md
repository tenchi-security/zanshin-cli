# `zanshin`

**Usage**:

```console
$ zanshin [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `init`: Update settings on configuration file.
* `me`: Show details about the owner of the API key...
* `organization`: Operations on organizations the API key owner...
* `version`: Display the program and Python versions in...

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

* `--profile TEXT`: Configuration file section to use for credentials and other settings  [default: default]
* `--help`: Show this message and exit.

## `zanshin organization`

Operations on organizations the API key owner has direct access to.

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

* `ORGANIZATION_ID`: UUID of the organization to list alerts from.  [required]

**Options**:

* `--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|RESOLVED|CLOSED]`: Only list alerts in the specified states.  [default: OPEN, ACTIVE, IN_PROGRESS, RISK_ACCEPTED, RESOLVED]
* `--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]`: Only list alerts with the specified severities.  [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
* `--profile TEXT`: Configuration file section to use for credentials and other settings  [default: default]
* `--format [json|table|csv|html]`: Format to use for the output.  [default: json]
* `--help`: Show this message and exit.

### `zanshin organization list`

Lists the organizations this user has direct access to as a member.

**Usage**:

```console
$ zanshin organization list [OPTIONS]
```

**Options**:

* `--profile TEXT`: Configuration file section to use for credentials and other settings  [default: default]
* `--format [json|table|csv|html]`: Format to use for the output.  [default: json]
* `--help`: Show this message and exit.

### `zanshin organization scan_target`

Operations on scan targets from organizations the API key owner has direct access to.

**Usage**:

```console
$ zanshin organization scan_target [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `check`: Check an scan_target status from an...
* `list`: Lists the scan targets from an organization...
* `scan`: Start an Scan in a specific scan_target from...

#### `zanshin organization scan_target check`

Check an scan_target status from an organization.

**Usage**:

```console
$ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization to list alerts from.  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to start scan.  [required]

**Options**:

* `--profile TEXT`: Configuration file section to use for credentials and other settings  [default: default]
* `--help`: Show this message and exit.

#### `zanshin organization scan_target list`

Lists the scan targets from an organization that user has access to as a member.

**Usage**:

```console
$ zanshin organization scan_target list [OPTIONS] ORGANIZATION_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organizations whose scan targets should be listed.  [required]

**Options**:

* `--profile TEXT`: Configuration file section to use for credentials and other settings  [default: default]
* `--format [json|table|csv|html]`: Format to use for the output.  [default: json]
* `--help`: Show this message and exit.

#### `zanshin organization scan_target scan`

Start an Scan in a specific scan_target from an organization.

**Usage**:

```console
$ zanshin organization scan_target scan [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID
```

**Arguments**:

* `ORGANIZATION_ID`: UUID of the organization to list alerts from.  [required]
* `SCAN_TARGET_ID`: UUID of the scan target to start scan.  [required]

**Options**:

* `--profile TEXT`: Configuration file section to use for credentials and other settings  [default: default]
* `--help`: Show this message and exit.

## `zanshin version`

Display the program and Python versions in use.

**Usage**:

```console
$ zanshin version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
