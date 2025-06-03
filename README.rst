|PyPI version shields.io| |PyPI pyversions|

Zanshin CLI
===========

This Python package provides a command-line utility to interact with the
`API of the Zanshin SaaS
service <https://api.zanshin.tenchisecurity.com>`__ from `Tenchi
Security <https://www.tenchisecurity.com>`__.

Is it based on the Zanshin Python SDK available on
`Github <https://github.com/tenchi-security/zanshin-sdk-python>`__ and
`PyPI <https://pypi.python.org/pypi/zanshinsdk/>`__.

If you are a Zanshin customer and have any questions regarding the use
of the service, its API or this command-line utility, please get in
touch via e-mail at support {at} tenchisecurity {dot} com or via the
support widget on the `Zanshin
Portal <https://zanshin.tenchisecurity.com>`__.

Installation
------------

We recommend the CLI is installed using
`pipx <https://pypa.github.io/pipx/installation/>`__, using the command:

.. code:: shell

   pipx install zanshincli

When a new version is available, you can upgrade it with:

.. code:: shell

   pipx upgrade zanshincli

Configuration File
------------------

The way the SDK and CLI handles credentials is by using a configuration
file in the format created by the Python
`RawConfigParser <https://docs.python.org/3/library/configparser.html#configparser.RawConfigParser>`__
class.

The file is located at ``~/.tenchi/config``, where ``~`` is the `current
user's home
directory <https://docs.python.org/3/library/pathlib.html#pathlib.Path.home>`__.

Each section is treated as a configuration profile, and the SDK and CLI
will look for a section called ``default`` if another is not explicitly
selected.

These are the supported options:

- ``api_key`` (required) which contains the Zanshin API key obtained at
  the `Zanshin web
  portal <https://zanshin.tenchisecurity.com/my-profile>`__.
- ``user_agent`` (optional) allows you to override the default
  user-agent header used by the SDK when making API requests.
- ``api_url`` (optional) directs the SDK and CLI to use a different API
  endpoint than the default (https://api.zanshin.tenchisecurity.com).

You can populate the file with the ``zanshin init`` command of the CLI
tool. This is what a minimal configuration file would look like:

.. code:: ini

   [default]
   api_key = abcdefghijklmnopqrstuvxyz

Using the CLI Utility
---------------------

This package installs a command-line utility called ``zanshin`` built
with the great `Typer <https://typer.tiangolo.com/>`__ package.

You can obtain help by using the ``--help`` option.

Keep in mind that when options are present that expect multiple values,
these need to be provided as multiple options. For example if you wanted
to list an organization's alerts filtering by the OPEN and RISK_ACCEPTED
states, this is the command you would use:

.. code:: shell

   $ zanshin organization alerts d48edaa6-871a-4082-a196-4daab372d4a1 --state OPEN --state RISK_ACCEPTED

Command Reference
-----------------

``zanshin``
===========

Command-line utility to interact with the Zanshin SaaS service offered
by Tenchi Security (https://tenchisecurity.com), go to
https://github.com/tenchi-security/zanshin-cli for license, source code
and documentation

**Usage**:

.. code:: console

   $ zanshin [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--profile TEXT``: Configuration file section to read API keyand
  configuration from [default: default]
- ``--format [json|table|csv|html]``: Output format to use for list
  operations [default: OutputFormat.JSON]
- ``--verbose / --no-verbose``: Print more information to stderr
  [default: True]
- ``--debug / --no-debug``: Enable debug logging in the SDK [default:
  False]
- ``--install-completion``: Install completion for the current shell.
- ``--show-completion``: Show completion for the current shell, to copy
  it or customize the installation.
- ``--help``: Show this message and exit.

**Commands**:

- ``account``: Operations on user the API key owner has...
- ``alert``: Operations on alerts the API key owner has...
- ``init``: Update settings on configuration file.
- ``organization``: Operations on organizations the API key owner...
- ``summary``: Operations on summaries the API key owner has...
- ``version``: Display the program and Python versions in...

``zanshin account``
-------------------

Operations on user the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin account [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``api_key``: Operations on API keys from account the API...
- ``invites``: Operations on invites from account the API...
- ``me``: Returns the details of the user account that...

``zanshin account api_key``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on API keys from account the API key owner has direct access
to

**Usage**:

.. code:: console

   $ zanshin account api_key [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``create``: Creates a new API key for the current logged...
- ``delete``: Deletes a given API key by its id, it will...
- ``list``: Iterates over the API keys of current logged...

``zanshin account api_key create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates a new API key for the current logged user, API Keys can be used
to interact with the zanshin api directly a behalf of that user.

**Usage**:

.. code:: console

   $ zanshin account api_key create [OPTIONS] NAME

**Arguments**:

- ``NAME``: Name of the new API key [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin account api_key delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deletes a given API key by its id, it will only work if the informed ID
belongs to the current logged user.

**Usage**:

.. code:: console

   $ zanshin account api_key delete [OPTIONS] API_KEY_ID

**Arguments**:

- ``API_KEY_ID``: UUID of the invite to delete [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin account api_key list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterates over the API keys of current logged user.

**Usage**:

.. code:: console

   $ zanshin account api_key list [OPTIONS]

**Options**:

- ``--help``: Show this message and exit.

``zanshin account invites``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on invites from account the API key owner has direct access
to

**Usage**:

.. code:: console

   $ zanshin account invites [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``accept``: Accepts an invitation with the informed ID,...
- ``get``: Gets a specific invitation details, it only...
- ``list``: Iterates over the invites of current logged...

``zanshin account invites accept``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Accepts an invitation with the informed ID, it only works if the user
accepting the invitation is the user that received the invitation.

**Usage**:

.. code:: console

   $ zanshin account invites accept [OPTIONS] INVITE_ID

**Arguments**:

- ``INVITE_ID``: UUID of the invite [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin account invites get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gets a specific invitation details, it only works if the invitation was
made for the current logged user.

**Usage**:

.. code:: console

   $ zanshin account invites get [OPTIONS] INVITE_ID

**Arguments**:

- ``INVITE_ID``: UUID of the invite [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin account invites list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterates over the invites of current logged user.

**Usage**:

.. code:: console

   $ zanshin account invites list [OPTIONS]

**Options**:

- ``--help``: Show this message and exit.

``zanshin account me``
~~~~~~~~~~~~~~~~~~~~~~

Returns the details of the user account that owns the API key used by
this Connection instance

**Usage**:

.. code:: console

   $ zanshin account me [OPTIONS]

**Options**:

- ``--help``: Show this message and exit.

``zanshin alert``
-----------------

Operations on alerts the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin alert [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``batch_update_state``: Updates the state of multiple alerts in a...
- ``generate_alert_category_report``
- ``get``: Returns details about a specified alert
- ``list``: List alerts from a given organization, with...
- ``list_following``: List following alerts from a given...
- ``list_grouped``: List grouped alerts from a given...
- ``list_grouped_following``: List grouped following alerts from a
  given...
- ``list_history``: List alerts from a given organization, with...
- ``list_history_following``: List alerts from a given organization,
  with...
- ``update``: Updates the alert.

``zanshin alert batch_update_state``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates the state of multiple alerts in a batch.

**Usage**:

.. code:: console

   $ zanshin alert batch_update_state [OPTIONS] ORGANIZATION_ID STATE:[OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED] COMMENT DRY_RUN

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization that owns the alerts
  [required]
- ``STATE:[OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
  New state to set for the alerts [required]
- ``COMMENT``: Comment explaining this batch update [required]
- ``DRY_RUN``: If true, performs a simulation without making actual
  changes [required]

**Options**:

- ``--scan-target-ids UUID``: List of UUIDs representing the scan
  targets to filter by
- ``--alert-ids TEXT``: List of alert IDs to update
- ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
  List of existing alert states to filter alerts by
- ``--rules TEXT``: List of rules to filter alerts by
- ``--severities TEXT``: List of severities to filter alerts by (e.g.,
  'low', 'medium', 'high')
- ``--include-empty-scan-target-tags``: Whether to include alerts with
  scan targets that have no associated tags
- ``--help``: Show this message and exit.

``zanshin alert generate_alert_category_report``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Usage**:

.. code:: console

   $ zanshin alert generate_alert_category_report [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--following-ids UUID``: Only list alerts from the specified scan
  targets
- ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
  with the specified severities [default: AlertSeverity.CRITICAL,
  AlertSeverity.HIGH]
- ``--help``: Show this message and exit.

``zanshin alert get``
~~~~~~~~~~~~~~~~~~~~~

Returns details about a specified alert

**Usage**:

.. code:: console

   $ zanshin alert get [OPTIONS] ALERT_ID

**Arguments**:

- ``ALERT_ID``: UUID of the alert to look up [required]

**Options**:

- ``--list-history / --no-list-history``: History of this alert
  [default: False]
- ``--list-comments / --no-list-comments``: Comments of this alert
  [default: False]
- ``--help``: Show this message and exit.

``zanshin alert list``
~~~~~~~~~~~~~~~~~~~~~~

List alerts from a given organization, with optional filters by scan
target, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--scan-target-ids UUID``: Only list alerts from the specified scan
  targets
- ``--scan-target-tags TEXT``: Only lists alerts from the specified tags
- ``--include-empty-scan-target-tags / --no-include-empty-scan-target-tags``:
  Include alerts from scan targets without tags
- ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
  Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
  RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
- ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
  with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
  INFO]
- ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
  [default: en-US]
- ``--created-at-start TEXT``: Date created starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--created-at-end TEXT``: Date created ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-start TEXT``: Date updated starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-end TEXT``: Date updated ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--search TEXT``: Text to search for in the alerts [default: ]
- ``--sort [ASC|DESC]``: Sort order
- ``--rules TEXT``: Only list alerts in the specified rules
- ``--opened-at-start TEXT``: Date opened starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--opened-at-end TEXT``: Date opened ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-start TEXT``: Date resolved starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-end TEXT``: Date resolved ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--cursor TEXT``: Cursor for pagination
- ``--order [scanTargetId|resource|rule|severity|state|openedAt|resolvedAt|createdAt|updatedAt]``:
  Field to sort results on [default: AlertsOrderOpts.SEVERITY]
- ``--comments``: Retrieve alerts with their comments [default: False]
- ``--help``: Show this message and exit.

``zanshin alert list_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List following alerts from a given organization, with optional filters
by following ids, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert list_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--following-ids UUID``: Only list alerts from the specified scan
  targets
- ``--following-tags UUID``: Only lists alerts from the specified tags
- ``--include-empty-following-tags / --no-include-empty-following-tags``:
  Include alerts from scan targets without tags
- ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
  Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
  RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
- ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
  with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
  INFO]
- ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
  [default: en-US]
- ``--created-at-start TEXT``: Date created starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--created-at-end TEXT``: Date created ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-start TEXT``: Date updated starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-end TEXT``: Date updated ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--search TEXT``: Text to search for in the alerts [default: ]
- ``--sort [ASC|DESC]``: Sort order
- ``--rules TEXT``: Only list alerts in the specified rules
- ``--opened-at-start TEXT``: Date opened starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--opened-at-end TEXT``: Date opened ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-start TEXT``: Date resolved starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-end TEXT``: Date resolved ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--cursor TEXT``: Cursor for pagination
- ``--order [scanTargetId|resource|rule|severity|state|openedAt|resolvedAt|createdAt|updatedAt]``:
  Field to sort results on [default: AlertsOrderOpts.SEVERITY]
- ``--comments``: Retrieve alerts with their comments [default: False]
- ``--help``: Show this message and exit.

``zanshin alert list_grouped``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List grouped alerts from a given organization, with optional filters by
scan target, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert list_grouped [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--scan-target-ids UUID``: Only list alerts from the specified scan
  targets
- ``--scan-target-tags TEXT``: Only lists alerts from the specified tags
- ``--include-empty-scan-target-tags / --no-include-empty-scan-target-tags``:
  Include alerts from scan targets without tags
- ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
  Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
  RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
- ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
  with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
  INFO]
- ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
  [default: en-US]
- ``--created-at-start TEXT``: Date created starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--created-at-end TEXT``: Date created ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-start TEXT``: Date updated starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-end TEXT``: Date updated ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--search TEXT``: Text to search for in the alerts [default: ]
- ``--sort [ASC|DESC]``: Sort order
- ``--rules TEXT``: Only list alerts in the specified rules
- ``--opened-at-start TEXT``: Date opened starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--opened-at-end TEXT``: Date opened ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-start TEXT``: Date resolved starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-end TEXT``: Date resolved ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--cursor TEXT``: Cursor for pagination
- ``--order [severity|rule|total]``: Field to sort results on [default:
  GroupedAlertOrderOpts.SEVERITY]
- ``--help``: Show this message and exit.

``zanshin alert list_grouped_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List grouped following alerts from a given organization, with optional
filters by scan target, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert list_grouped_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--following-ids UUID``: Only list alerts from the specified scan
  targets
- ``--following-tags UUID``: Only lists alerts from the specified tags
- ``--include-empty-following-tags / --no-include-empty-following-tags``:
  Include alerts from scan targets without tags
- ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
  Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
  RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
- ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
  with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
  INFO]
- ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
  [default: en-US]
- ``--created-at-start TEXT``: Date created starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--created-at-end TEXT``: Date created ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-start TEXT``: Date updated starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--updated-at-end TEXT``: Date updated ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--search TEXT``: Text to search for in the alerts [default: ]
- ``--sort [ASC|DESC]``: Sort order
- ``--rules TEXT``: Only list alerts in the specified rules
- ``--opened-at-start TEXT``: Date opened starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--opened-at-end TEXT``: Date opened ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-start TEXT``: Date resolved starts at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--resolved-at-end TEXT``: Date resolved ends at (format
  YYYY-MM-DDTHH:MM:SS)
- ``--cursor TEXT``: Cursor for pagination
- ``--order [severity|rule|total]``: Field to sort results on [default:
  GroupedAlertOrderOpts.SEVERITY]
- ``--help``: Show this message and exit.

``zanshin alert list_history``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List alerts from a given organization, with optional filters by scan
target, state or severity

**Usage**:

.. code:: console

   $ zanshin alert list_history [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--scan-target-id UUID``: Only list alerts from the specified scan
  targets
- ``--cursor TEXT``: Cursor for pagination
- ``--persist / --no-persist``: Persist [default: False]
- ``--help``: Show this message and exit.

``zanshin alert list_history_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List alerts from a given organization, with optional filters by scan
target, state or severity

**Usage**:

.. code:: console

   $ zanshin alert list_history_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--following-ids UUID``: Only list alerts from the specified scan
  targets
- ``--cursor TEXT``: Cursor for pagination
- ``--persist / --no-persist``: Persist [default: False]
- ``--help``: Show this message and exit.

``zanshin alert update``
~~~~~~~~~~~~~~~~~~~~~~~~

Updates the alert.

**Usage**:

.. code:: console

   $ zanshin alert update [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID ALERT_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization that owns the alert
  [required]
- ``SCAN_TARGET_ID``: UUID of the scan target associated with the alert
  [required]
- ``ALERT_ID``: UUID of the alert [required]

**Options**:

- ``--state [OPEN|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE]``:
  New alert state
- ``--labels TEXT``: Custom label(s) for the alert
- ``--comment TEXT``: A comment when setting the alert state to
  RISK_ACCEPTED, FALSE_POSITIVE, MITIGATING_CONTROL
- ``--help``: Show this message and exit.

``zanshin init``
----------------

Update settings on configuration file.

**Usage**:

.. code:: console

   $ zanshin init [OPTIONS]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization``
------------------------

Operations on organizations the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin organization [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``create``: Creates an organization.
- ``delete``: Deletes an organization given its ID.
- ``follower``: Operations on followers of organization the...
- ``following``: Operations on following of organization the...
- ``get``: Gets an organization given its ID.
- ``list``: Lists the organizations this user has direct...
- ``member``: Operations on members of organization the API...
- ``scan-target-groups``: Operations on organizations scan target...
- ``scan_target``: Operations on scan targets from organizations...
- ``update``: Gets an organization given its ID.

``zanshin organization create``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates an organization.

**Usage**:

.. code:: console

   $ zanshin organization create [OPTIONS] NAME

**Arguments**:

- ``NAME``: Name of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization delete``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deletes an organization given its ID.

**Usage**:

.. code:: console

   $ zanshin organization delete [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization follower``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on followers of organization the API key owner has direct
access to

**Usage**:

.. code:: console

   $ zanshin organization follower [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``list``: Lists the followers of organization this user...
- ``request``: Operations on follower requests of...
- ``stop``: Stops one organization follower of another.

``zanshin organization follower list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the followers of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization follower list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization follower request``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on follower requests of organization the API key owner has
directaccess to

**Usage**:

.. code:: console

   $ zanshin organization follower request [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``create``: Create organization follower request.
- ``delete``: Delete organization follower request.
- ``get``: Get organization follower request.
- ``list``: Lists the follower requests of organization...

``zanshin organization follower request create``
''''''''''''''''''''''''''''''''''''''''''''''''

Create organization follower request.

**Usage**:

.. code:: console

   $ zanshin organization follower request create [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``TOKEN``: Token of the follower request [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization follower request delete``
''''''''''''''''''''''''''''''''''''''''''''''''

Delete organization follower request.

**Usage**:

.. code:: console

   $ zanshin organization follower request delete [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``TOKEN``: Token of the follower request [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization follower request get``
'''''''''''''''''''''''''''''''''''''''''''''

Get organization follower request.

**Usage**:

.. code:: console

   $ zanshin organization follower request get [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``TOKEN``: Token of the follower request [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization follower request list``
''''''''''''''''''''''''''''''''''''''''''''''

Lists the follower requests of organization this user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization follower request list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization follower stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops one organization follower of another.

**Usage**:

.. code:: console

   $ zanshin organization follower stop [OPTIONS] ORGANIZATION_ID ORGANIZATION_FOLLOWER_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_FOLLOWER_ID``: UUID of the organization follower
  [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on following of organization the API key owner has direct
access to

**Usage**:

.. code:: console

   $ zanshin organization following [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``list``: Lists the following of organization this user...
- ``request``: Operations on following requests of...
- ``stop``: Stops one organization following of another.

``zanshin organization following list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the following of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization following list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization following request``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on following requests of organization the API key owner
hasdirect access to

**Usage**:

.. code:: console

   $ zanshin organization following request [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``accept``: Accepts a request to follow another...
- ``decline``: Declines a request to follow another...
- ``get``: Returns a request received by an organization...
- ``list``: Lists the following requests of organization...

``zanshin organization following request accept``
'''''''''''''''''''''''''''''''''''''''''''''''''

Accepts a request to follow another organization.

**Usage**:

.. code:: console

   $ zanshin organization following request accept [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization following request decline``
''''''''''''''''''''''''''''''''''''''''''''''''''

Declines a request to follow another organization.

**Usage**:

.. code:: console

   $ zanshin organization following request decline [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization following request get``
''''''''''''''''''''''''''''''''''''''''''''''

Returns a request received by an organization to follow another.

**Usage**:

.. code:: console

   $ zanshin organization following request get [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization following request list``
'''''''''''''''''''''''''''''''''''''''''''''''

Lists the following requests of organization this user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization following request list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization following stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops one organization following of another.

**Usage**:

.. code:: console

   $ zanshin organization following stop [OPTIONS] ORGANIZATION_ID ORGANIZATION_FOLLOWING_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_FOLLOWING_ID``: UUID of the organization following
  [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization get``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gets an organization given its ID.

**Usage**:

.. code:: console

   $ zanshin organization get [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization list``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists the organizations this user has direct access to as a member.

**Usage**:

.. code:: console

   $ zanshin organization list [OPTIONS]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on members of organization the API key owner has direct
access to

**Usage**:

.. code:: console

   $ zanshin organization member [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``delete``: Delete organization member.
- ``get``: Get organization member.
- ``invite``: Operations on member invites of organization...
- ``list``: Lists the members of organization this user...
- ``update``: Update organization member.

``zanshin organization member delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete organization member.

**Usage**:

.. code:: console

   $ zanshin organization member delete [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_ID``: UUID of the organization member [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get organization member.

**Usage**:

.. code:: console

   $ zanshin organization member get [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_ID``: UUID of the organization member [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member invite``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on member invites of organization the API key owner has
directaccess to

**Usage**:

.. code:: console

   $ zanshin organization member invite [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``create``: Create organization member invite.
- ``delete``: Delete organization member invite.
- ``get``: Get organization member invite.
- ``list``: Lists the member invites of organization this...
- ``resend``: Resend organization member invitation.

``zanshin organization member invite create``
'''''''''''''''''''''''''''''''''''''''''''''

Create organization member invite.

**Usage**:

.. code:: console

   $ zanshin organization member invite create [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
  member [required]

**Options**:

- ``--organization-member-invite-role [ADMIN]``: Role of the
  organization member [default: ADMIN]
- ``--help``: Show this message and exit.

``zanshin organization member invite delete``
'''''''''''''''''''''''''''''''''''''''''''''

Delete organization member invite.

**Usage**:

.. code:: console

   $ zanshin organization member invite delete [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
  member [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member invite get``
''''''''''''''''''''''''''''''''''''''''''

Get organization member invite.

**Usage**:

.. code:: console

   $ zanshin organization member invite get [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
  member invite [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member invite list``
'''''''''''''''''''''''''''''''''''''''''''

Lists the member invites of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization member invite list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member invite resend``
'''''''''''''''''''''''''''''''''''''''''''''

Resend organization member invitation.

**Usage**:

.. code:: console

   $ zanshin organization member invite resend [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
  member [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the members of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization member list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization member update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update organization member.

**Usage**:

.. code:: console

   $ zanshin organization member update [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``ORGANIZATION_MEMBER_ID``: UUID of the organization member [required]

**Options**:

- ``--role [ADMIN]``: Role of the organization member [default: ADMIN]
- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on organizations scan target groups the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``compartments``: Iterates over the compartments of a scan...
- ``create``: Creates a scan target group for the...
- ``create-by-compartments``: Creates Scan Targets from previous
  listed...
- ``delete``: Deletes the scan target group of the...
- ``get``: Gets details of the scan target group given...
- ``insert``: Inserts an already created scan target group.
- ``list``: Lists the scan target groups of the user's...
- ``oauth_link``: Retrieve a link to allow the user to...
- ``scan-targets``: Gets all scan targets from a specific scan...
- ``script``: Gets download URL of the scan target group.
- ``update``: Updates a scan target group.

``zanshin organization scan-target-groups compartments``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterates over the compartments of a scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups compartments [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates a scan target group for the organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups create [OPTIONS] ORGANIZATION_ID KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK] NAME

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
  kind of the scan target group. Should be 'ORACLE', 'BITBUCKET' or
  'GITLAB' [required]
- ``NAME``: name of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups create-by-compartments``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates Scan Targets from previous listed compartments inside the scan
target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups create-by-compartments [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID NAME OCID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]
- ``NAME``: Compartment name [required]
- ``OCID``: Oracle Compartment Id [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deletes the scan target group of the organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups delete [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gets details of the scan target group given its ID.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups insert``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inserts an already created scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups insert [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID REGION TENANCY_ID USER_ID KEY_FINGERPRINT

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]
- ``REGION``: Oracle cloud region [required]
- ``TENANCY_ID``: Oracle tenancyId [required]
- ``USER_ID``: Oracle userId [required]
- ``KEY_FINGERPRINT``: Oracle Fingerprint used for authentication
  [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the scan target groups of the user's organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups oauth_link``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve a link to allow the user to authorize zanshin to read info from
their scan target group environment.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups oauth_link [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups scan-targets``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gets all scan targets from a specific scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups scan-targets [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups script``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gets download URL of the scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups script [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan-target-groups update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Updates a scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups update [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID NAME

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]
- ``NAME``: new name of the scan target group [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on scan targets from organizations the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization scan_target [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``check``: Check scan target.
- ``create``: Create a new scan target in organization.
- ``delete``: Delete scan target of organization.
- ``get``: Get scan target of organization.
- ``list``: Lists the scan targets of organization this...
- ``oauth_link``: Retrieve a link to allow the user to...
- ``onboard_aws``: Create a new scan target in organization and...
- ``onboard_aws_organization``: For each of selected accounts in AWS...
- ``scan``: Operations on scan targets from organizations...
- ``update``: Update scan target of organization.

``zanshin organization scan_target check``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new scan target in organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target create [OPTIONS] ORGANIZATION_ID KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK] NAME CREDENTIAL [SCHEDULE]

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
  kind of the scan target [required]
- ``NAME``: name of the scan target [required]
- ``CREDENTIAL``: credential of the scan target [required]
- ``[SCHEDULE]``: schedule of the scan target [default: {"frequency":
  "1d", "timeOfDay": "NIGHT"}]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete scan target of organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target delete [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get scan target of organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the scan targets of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization scan_target list [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target oauth_link``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve a link to allow the user to authorize zanshin to read info from
their scan target environment.

**Usage**:

.. code:: console

   $ zanshin organization scan_target oauth_link [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target onboard_aws``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new scan target in organization and perform onboard. Requires
boto3 and correct AWS IAM Privileges. Checkout the required AWS IAM
privileges here
https://github.com/tenchi-security/zanshin-sdk-python/blob/main/zanshinsdk/docs/README.md

**Usage**:

.. code:: console

   $ zanshin organization scan_target onboard_aws [OPTIONS] REGION ORGANIZATION_ID NAME CREDENTIAL [SCHEDULE]

**Arguments**:

- ``REGION``: AWS Region to deploy CloudFormation [required]
- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``NAME``: name of the scan target [required]
- ``CREDENTIAL``: credential of the scan target [required]
- ``[SCHEDULE]``: schedule of the scan target [default: {"frequency":
  "1d", "timeOfDay": "NIGHT"}]

**Options**:

- ``--boto3-profile TEXT``: Boto3 profile name to use for Onboard AWS
  Account
- ``--help``: Show this message and exit.

``zanshin organization scan_target onboard_aws_organization``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each of selected accounts in AWS Organization, creates a new Scan
Target in informed zanshin organization and performs onboarding.
Requires boto3 and correct AWS IAM Privileges. Checkout the required AWS
IAM privileges at
https://github.com/tenchi-security/zanshin-cli/blob/main/src/lib/docs/README.md

**Usage**:

.. code:: console

   $ zanshin organization scan_target onboard_aws_organization [OPTIONS] REGION ORGANIZATION_ID [SCHEDULE]

**Arguments**:

- ``REGION``: AWS Region to deploy CloudFormation [required]
- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``[SCHEDULE]``: schedule of the scan target [default: {"frequency":
  "1d", "timeOfDay": "NIGHT"}]

**Options**:

- ``--target-accounts [ALL|MASTER|MEMBERS|NONE]``: choose which accounts
  to onboard
- ``--exclude-account TEXT``: ID, Name, E-mail or ARN of AWS Account not
  to be onboarded
- ``--boto3-profile TEXT``: Boto3 profile name to use for Onboard AWS
  Account
- ``--aws-role-name TEXT``: Name of AWS role that allow access from
  Management Account to Member accounts [default:
  OrganizationAccountAccessRole]
- ``--help``: Show this message and exit.

``zanshin organization scan_target scan``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on scan targets from organizations the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``get``: Get scan of scan target.
- ``list``: Lists the scan target scans of organization...
- ``start``: Starts a scan on the specified scan target.
- ``stop``: Stop a scan on the specified scan target.

``zanshin organization scan_target scan get``
'''''''''''''''''''''''''''''''''''''''''''''

Get scan of scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID SCAN_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]
- ``SCAN_ID``: UUID of the scan [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target scan list``
''''''''''''''''''''''''''''''''''''''''''''''

Lists the scan target scans of organization this user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan list [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target scan start``
'''''''''''''''''''''''''''''''''''''''''''''''

Starts a scan on the specified scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan start [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--force / --no-force``: Whether to force running a scan target that
  has state INVALID_CREDENTIAL or NEW [default: False]
- ``--help``: Show this message and exit.

``zanshin organization scan_target scan stop``
''''''''''''''''''''''''''''''''''''''''''''''

Stop a scan on the specified scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan stop [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization scan_target update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update scan target of organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target update [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID [NAME] [SCHEDULE]

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``SCAN_TARGET_ID``: UUID of the scan target [required]
- ``[NAME]``: name of the scan target
- ``[SCHEDULE]``: schedule of the scan target

**Options**:

- ``--help``: Show this message and exit.

``zanshin organization update``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gets an organization given its ID.

**Usage**:

.. code:: console

   $ zanshin organization update [OPTIONS] ORGANIZATION_ID [NAME] [PICTURE] [EMAIL]

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]
- ``[NAME]``: Name of the organization
- ``[PICTURE]``: Picture of the organization
- ``[EMAIL]``: Contact e-mail of the organization

**Options**:

- ``--help``: Show this message and exit.

``zanshin summary``
-------------------

Operations on summaries the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin summary [OPTIONS] COMMAND [ARGS]...

**Options**:

- ``--help``: Show this message and exit.

**Commands**:

- ``scan_targets_detail``
- ``scan_targets_following``

``zanshin summary scan_targets_detail``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Usage**:

.. code:: console

   $ zanshin summary scan_targets_detail [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--scan-target-ids UUID``: Only summarize scan targets from the
  specified scan target ids
- ``--scan-target-tags TEXT``: Only summarize scan targets from the
  specified scan target tags
- ``--scan-target-kinds [AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
  Only summarize scan targets from the specified kinds
- ``--alert-severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only summarize
  alerts with the specified severities
- ``--help``: Show this message and exit.

``zanshin summary scan_targets_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Usage**:

.. code:: console

   $ zanshin summary scan_targets_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

- ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

- ``--following-ids UUID``: Only summarize scan targets from the
  specified following ids
- ``--following-tags TEXT``: Only summarize scan targets from the
  specified following tags
- ``--scan-target-kinds [AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
  Only summarize scan targets from the specified kinds
- ``--alert-severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only summarize
  alerts with the specified severities
- ``--include-empty-following-tags / --no-include-empty-following-tags``:
  Include alerts from scan targets without tags
- ``--help``: Show this message and exit.

``zanshin version``
-------------------

Display the program and Python versions in use.

**Usage**:

.. code:: console

   $ zanshin version [OPTIONS]

**Options**:

- ``--help``: Show this message and exit.

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
