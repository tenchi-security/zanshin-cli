|PyPI version shields.io| |PyPI pyversions|

Zanshin CLI
===========

This Python package provides a command-line utility to interact with the
`API of the Zanshin SaaS
service <https://api.zanshin.tenchisecurity.com>`__ from `Tenchi
Security <https://www.tenchisecurity.com>`__.

It is based on the Zanshin Python SDK available on
`GitHub <https://github.com/tenchi-security/zanshin-sdk-python>`__ and
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

-  ``api_key`` (required) which contains the Zanshin API key obtained at
   the `Zanshin web
   portal <https://zanshin.tenchisecurity.com/my-profile>`__.
-  ``user_agent`` (optional) allows you to override the default
   user-agent header used by the SDK when making API requests.
-  ``api_url`` (optional) directs the SDK and CLI to use a different API
   endpoint than the default
   (`https://api.zanshin.tenchisecurity.com <https://api.zanshin.tenchisecurity.com>`__).

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
by Tenchi Security
(`https://tenchisecurity.com <https://tenchisecurity.com>`__), go to
`https://github.com/tenchi-security/zanshin-cli <https://github.com/tenchi-security/zanshin-cli>`__
for license, source code and documentation.

**Usage**:

.. code:: console

   $ zanshin [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--profile TEXT``: Configuration file section to read API key and
   configuration from [default: default]
-  ``--format [json|table|csv|html]``: Output format to use for list
   operations [default: json]
-  ``--verbose / --no-verbose``: Print more information to stderr
   [default: True]
-  ``--debug / --no-debug``: Enable debug logging in the SDK [default:
   False]
-  ``--install-completion``: Install completion for the current shell.
-  ``--show-completion``: Show completion for the current shell, to copy
   it or customize the installation.
-  ``--help``: Show this message and exit.

**Commands**:

-  ``account``: Manage the user account associated with the...
-  ``alert``: Manage and view security alerts across...
-  ``init``: Initialize or update the Zanshin CLI...
-  ``organization``: Manage organizations the logged-in user has...
-  ``summary``: Generate aggregated data summaries and...
-  ``version``: Display the current versions of the Zanshin...

``zanshin account``
-------------------

Manage the user account associated with the current API key.

**Usage**:

.. code:: console

   $ zanshin account [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``api_key``: Manage API keys associated with the logged-in...
-  ``invites``: Manage pending invitations for the logged-in...
-  ``me``: Show details of the user account associated...

``zanshin account api_key``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage API keys associated with the logged-in user account.

**Usage**:

.. code:: console

   $ zanshin account api_key [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``create``: Create a new API key for the logged-in user...
-  ``delete``: Delete a specific API key by its UUID.
-  ``list``: List all API keys belonging to the currently...

``zanshin account api_key create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new API key for the logged-in user to interact with the Zanshin
API.

**Usage**:

.. code:: console

   $ zanshin account api_key create [OPTIONS] NAME

**Arguments**:

-  ``NAME``: Name of the new API key [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account api_key delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete a specific API key by its UUID. The key must belong to the
logged-in user.

**Usage**:

.. code:: console

   $ zanshin account api_key delete [OPTIONS] API_KEY_ID

**Arguments**:

-  ``API_KEY_ID``: UUID of the API key to delete [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account api_key list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all API keys belonging to the currently logged-in user.

**Usage**:

.. code:: console

   $ zanshin account api_key list [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account invites``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage pending invitations for the logged-in user.

**Usage**:

.. code:: console

   $ zanshin account invites [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``accept``: Accept a specific invitation.
-  ``get``: Get details of a specific invitation...
-  ``list``: List all pending invitations for the...

``zanshin account invites accept``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Accept a specific invitation. The invite must belong to the logged-in
user.

**Usage**:

.. code:: console

   $ zanshin account invites accept [OPTIONS] INVITE_ID

**Arguments**:

-  ``INVITE_ID``: UUID of the invite [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account invites get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get details of a specific invitation belonging to the logged-in user.

**Usage**:

.. code:: console

   $ zanshin account invites get [OPTIONS] INVITE_ID

**Arguments**:

-  ``INVITE_ID``: UUID of the invite [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account invites list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all pending invitations for the currently logged-in user.

**Usage**:

.. code:: console

   $ zanshin account invites list [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account me``
~~~~~~~~~~~~~~~~~~~~~~

Show details of the user account associated with the currently
configured API key.

**Usage**:

.. code:: console

   $ zanshin account me [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin alert``
-----------------

Manage and view security alerts across organizations.

**Usage**:

.. code:: console

   $ zanshin alert [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``batch_update_state``: Update the state of multiple alerts in a...
-  ``generate_alert_category_report``: Generate an alert category report
   for an...
-  ``get``: Return details about a specified alert, with...
-  ``list``: List alerts from a given organization,...
-  ``list_following``: List following alerts from an organization,...
-  ``list_grouped``: List grouped alerts from an organization,...
-  ``list_grouped_following``: List grouped following alerts from an...
-  ``list_history``: List the history of alerts from an...
-  ``list_history_following``: List the history of following alerts from
   an...
-  ``update``: Update a specific alert's state, labels, and...

``zanshin alert batch_update_state``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update the state of multiple alerts in a batch, with dry-run support and
extensive filtering options.

**Usage**:

.. code:: console

   $ zanshin alert batch_update_state [OPTIONS] ORGANIZATION_ID STATE:[OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED] COMMENT DRY_RUN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization that owns the alerts
   [required]
-  ``STATE:[OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
   New state to set for the alerts [required]
-  ``COMMENT``: Comment explaining this batch update [required]
-  ``DRY_RUN``: If true, performs a simulation without making actual
   changes [required]

**Options**:

-  ``--scan-target-ids UUID``: List of UUIDs representing the scan
   targets to filter by
-  ``--alert-ids TEXT``: List of alert IDs to update
-  ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
   List of existing alert states to filter alerts by
-  ``--rules TEXT``: List of rules to filter alerts by
-  ``--severities TEXT``: List of severities to filter alerts by (e.g.,
   'low', 'medium', 'high')
-  ``--include-empty-scan-target-tags``: Whether to include alerts with
   scan targets that have no associated tags
-  ``--help``: Show this message and exit.

``zanshin alert generate_alert_category_report``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate an alert category report for an organization's followings,
grouped by tag and severity.

**Usage**:

.. code:: console

   $ zanshin alert generate_alert_category_report [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only list alerts from the specified following organizations
-  ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
   with the specified severities [default: CRITICAL, HIGH]
-  ``--help``: Show this message and exit.

``zanshin alert get``
~~~~~~~~~~~~~~~~~~~~~

Return details about a specified alert, with options to view its history
or associated comments.

**Usage**:

.. code:: console

   $ zanshin alert get [OPTIONS] ALERT_ID

**Arguments**:

-  ``ALERT_ID``: UUID of the alert to look up [required]

**Options**:

-  ``--list-history / --no-list-history``: History of this alert
   [default: False]
-  ``--list-comments / --no-list-comments``: Comments of this alert
   [default: False]
-  ``--help``: Show this message and exit.

``zanshin alert list``
~~~~~~~~~~~~~~~~~~~~~~

List alerts from a given organization, supporting advanced filtering,
text search, pagination, and comment fetching.

**Usage**:

.. code:: console

   $ zanshin alert list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-ids UUID``: Only list alerts from the specified scan
   targets
-  ``--scan-target-tags TEXT``: Only lists alerts from the specified
   tags
-  ``--include-empty-scan-target-tags / --no-include-empty-scan-target-tags``:
   Include alerts from scan targets without tags
-  ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
   Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
   RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
-  ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
   with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
   INFO]
-  ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
   [default: en-US]
-  ``--created-at-start TEXT``: Date created starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--created-at-end TEXT``: Date created ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-start TEXT``: Date updated starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-end TEXT``: Date updated ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--search TEXT``: Text to search for in the alerts [default: ]
-  ``--sort [ASC|DESC]``: Sort order
-  ``--rules TEXT``: Only list alerts in the specified rules
-  ``--opened-at-start TEXT``: Date opened starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--opened-at-end TEXT``: Date opened ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-start TEXT``: Date resolved starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-end TEXT``: Date resolved ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--cursor TEXT``: Cursor for pagination
-  ``--order [scanTargetId|resource|rule|severity|state|openedAt|resolvedAt|createdAt|updatedAt]``:
   Field to sort results on [default: severity]
-  ``--comments``: Retrieve alerts with their comments [default: False]
-  ``--help``: Show this message and exit.

``zanshin alert list_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List following alerts from an organization, supporting advanced
filtering, search, pagination, and comments.

**Usage**:

.. code:: console

   $ zanshin alert list_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only list alerts from the specified following organizations
-  ``--following-tags TEXT``: Only lists alerts from the specified tags
-  ``--include-empty-following-tags / --no-include-empty-following-tags``:
   Include alerts from following organizations without tags
-  ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
   Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
   RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
-  ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
   with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
   INFO]
-  ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
   [default: en-US]
-  ``--created-at-start TEXT``: Date created starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--created-at-end TEXT``: Date created ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-start TEXT``: Date updated starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-end TEXT``: Date updated ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--search TEXT``: Text to search for in the alerts [default: ]
-  ``--sort [ASC|DESC]``: Sort order
-  ``--rules TEXT``: Only list alerts in the specified rules
-  ``--opened-at-start TEXT``: Date opened starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--opened-at-end TEXT``: Date opened ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-start TEXT``: Date resolved starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-end TEXT``: Date resolved ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--cursor TEXT``: Cursor for pagination
-  ``--order [scanTargetId|resource|rule|severity|state|openedAt|resolvedAt|createdAt|updatedAt]``:
   Field to sort results on [default: severity]
-  ``--comments``: Retrieve alerts with their comments [default: False]
-  ``--help``: Show this message and exit.

``zanshin alert list_grouped``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List grouped alerts from an organization, supporting advanced filtering,
text search, and pagination.

**Usage**:

.. code:: console

   $ zanshin alert list_grouped [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-ids UUID``: Only list alerts from the specified scan
   targets
-  ``--scan-target-tags TEXT``: Only lists alerts from the specified
   tags
-  ``--include-empty-scan-target-tags / --no-include-empty-scan-target-tags``:
   Include alerts from scan targets without tags
-  ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
   Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
   RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
-  ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
   with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
   INFO]
-  ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
   [default: en-US]
-  ``--created-at-start TEXT``: Date created starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--created-at-end TEXT``: Date created ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-start TEXT``: Date updated starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-end TEXT``: Date updated ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--search TEXT``: Text to search for in the alerts [default: ]
-  ``--sort [ASC|DESC]``: Sort order
-  ``--rules TEXT``: Only list alerts in the specified rules
-  ``--opened-at-start TEXT``: Date opened starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--opened-at-end TEXT``: Date opened ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-start TEXT``: Date resolved starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-end TEXT``: Date resolved ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--cursor TEXT``: Cursor for pagination
-  ``--order [severity|rule|total]``: Field to sort results on [default:
   severity]
-  ``--help``: Show this message and exit.

``zanshin alert list_grouped_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List grouped following alerts from an organization, supporting advanced
filtering, search, and pagination.

**Usage**:

.. code:: console

   $ zanshin alert list_grouped_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only list alerts from the specified following organizations
-  ``--following-tags TEXT``: Only lists alerts from the specified tags
-  ``--include-empty-following-tags / --no-include-empty-following-tags``:
   Include alerts from following organizations without tags
-  ``--states [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE|CLOSED]``:
   Only list alerts in the specified states [default: OPEN, IN_PROGRESS,
   RISK_ACCEPTED, MITIGATING_CONTROL, FALSE_POSITIVE]
-  ``--severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts
   with the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW,
   INFO]
-  ``--lang [pt-BR|en-US]``: Show alert titles in the specified language
   [default: en-US]
-  ``--created-at-start TEXT``: Date created starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--created-at-end TEXT``: Date created ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-start TEXT``: Date updated starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--updated-at-end TEXT``: Date updated ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--search TEXT``: Text to search for in the alerts [default: ]
-  ``--sort [ASC|DESC]``: Sort order
-  ``--rules TEXT``: Only list alerts in the specified rules
-  ``--opened-at-start TEXT``: Date opened starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--opened-at-end TEXT``: Date opened ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-start TEXT``: Date resolved starts at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--resolved-at-end TEXT``: Date resolved ends at (format
   YYYY-MM-DDTHH:MM:SS)
-  ``--cursor TEXT``: Cursor for pagination
-  ``--order [severity|rule|total]``: Field to sort results on [default:
   severity]
-  ``--help``: Show this message and exit.

``zanshin alert list_history``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the history of alerts from an organization, with an optional scan
target filter and result persistence.

**Usage**:

.. code:: console

   $ zanshin alert list_history [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-id UUID``: Only list alerts from the specified scan
   targets
-  ``--cursor TEXT``: Cursor for pagination
-  ``--persist / --no-persist``: Persist [default: False]
-  ``--help``: Show this message and exit.

``zanshin alert list_history_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the history of following alerts from an organization, with optional
ID filters and result persistence.

**Usage**:

.. code:: console

   $ zanshin alert list_history_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only list alerts from the specified following organizations
-  ``--cursor TEXT``: Cursor for pagination
-  ``--persist / --no-persist``: Persist [default: False]
-  ``--help``: Show this message and exit.

``zanshin alert update``
~~~~~~~~~~~~~~~~~~~~~~~~

Update a specific alert's state, labels, and add optional comments for
certain state transitions.

**Usage**:

.. code:: console

   $ zanshin alert update [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID ALERT_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization that owns the alert
   [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target associated with the alert
   [required]
-  ``ALERT_ID``: UUID of the alert [required]

**Options**:

-  ``--state [OPEN|IN_PROGRESS|RISK_ACCEPTED|MITIGATING_CONTROL|FALSE_POSITIVE]``:
   New alert state
-  ``--labels TEXT``: Custom label(s) for the alert
-  ``--comment TEXT``: A comment when setting the alert state to
   RISK_ACCEPTED, FALSE_POSITIVE, MITIGATING_CONTROL
-  ``--help``: Show this message and exit.

``zanshin init``
----------------

Initialize or update the Zanshin CLI configuration file with an API
profile.

**Usage**:

.. code:: console

   $ zanshin init [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization``
------------------------

Manage organizations the logged-in user has access to.

**Usage**:

.. code:: console

   $ zanshin organization [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``create``: Create a new organization with the specified...
-  ``delete``: Delete a specific organization by its UUID.
-  ``follower``: Manage followers of an organization.
-  ``following``: Manage relationships with following...
-  ``get``: Get details of a specific organization by its...
-  ``list``: List the organizations the logged-in user has...
-  ``member``: Manage members within an organization.
-  ``scan-target-groups``: Manage scan target groups within an...
-  ``scan_target``: Manage scan targets within an organization.
-  ``update``: Update an organization's details, such as...

``zanshin organization create``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new organization with the specified name.

**Usage**:

.. code:: console

   $ zanshin organization create [OPTIONS] NAME

**Arguments**:

-  ``NAME``: Name of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization delete``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Delete a specific organization by its UUID.

**Usage**:

.. code:: console

   $ zanshin organization delete [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage followers of an organization.

**Usage**:

.. code:: console

   $ zanshin organization follower [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: List the followers of an organization the...
-  ``request``: Manage incoming requests to follow an...
-  ``stop``: Stop a specific follower from following the...

``zanshin organization follower list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the followers of an organization the user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization follower list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage incoming requests to follow an organization.

**Usage**:

.. code:: console

   $ zanshin organization follower request [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``create``: Create a follower request for a specific...
-  ``delete``: Delete a specific organization follower...
-  ``get``: Get details of a specific organization...
-  ``list``: List the follower requests of an organization...

``zanshin organization follower request create``
''''''''''''''''''''''''''''''''''''''''''''''''

Create a follower request for a specific organization using a token.

**Usage**:

.. code:: console

   $ zanshin organization follower request create [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``TOKEN``: Token of the follower request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request delete``
''''''''''''''''''''''''''''''''''''''''''''''''

Delete a specific organization follower request using its token.

**Usage**:

.. code:: console

   $ zanshin organization follower request delete [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``TOKEN``: Token of the follower request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request get``
'''''''''''''''''''''''''''''''''''''''''''''

Get details of a specific organization follower request using its token.

**Usage**:

.. code:: console

   $ zanshin organization follower request get [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``TOKEN``: Token of the follower request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request list``
''''''''''''''''''''''''''''''''''''''''''''''

List the follower requests of an organization the user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization follower request list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stop a specific follower from following the given organization.

**Usage**:

.. code:: console

   $ zanshin organization follower stop [OPTIONS] ORGANIZATION_ID ORGANIZATION_FOLLOWER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_FOLLOWER_ID``: UUID of the organization follower
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage relationships with following organizations.

**Usage**:

.. code:: console

   $ zanshin organization following [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: List the followings of an organization the...
-  ``request``: Manage outgoing requests to follow other...
-  ``stop``: Stop the organization from following another...

``zanshin organization following list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the followings of an organization the user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization following list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage outgoing requests to follow other organizations.

**Usage**:

.. code:: console

   $ zanshin organization following request [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``accept``: Accept a pending request to follow another...
-  ``decline``: Decline a pending request to follow another...
-  ``get``: Get details of a specific request received by...
-  ``list``: List the following requests of an...

``zanshin organization following request accept``
'''''''''''''''''''''''''''''''''''''''''''''''''

Accept a pending request to follow another organization.

**Usage**:

.. code:: console

   $ zanshin organization following request accept [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request decline``
''''''''''''''''''''''''''''''''''''''''''''''''''

Decline a pending request to follow another organization.

**Usage**:

.. code:: console

   $ zanshin organization following request decline [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request get``
''''''''''''''''''''''''''''''''''''''''''''''

Get details of a specific request received by an organization to follow
another.

**Usage**:

.. code:: console

   $ zanshin organization following request get [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request list``
'''''''''''''''''''''''''''''''''''''''''''''''

List the following requests of an organization the user has direct
access to.

**Usage**:

.. code:: console

   $ zanshin organization following request list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stop the organization from following another specific organization.

**Usage**:

.. code:: console

   $ zanshin organization following stop [OPTIONS] ORGANIZATION_ID ORGANIZATION_FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_FOLLOWING_ID``: UUID of the organization following
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization get``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get details of a specific organization by its UUID.

**Usage**:

.. code:: console

   $ zanshin organization get [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization list``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the organizations the logged-in user has direct access to as a
member.

**Usage**:

.. code:: console

   $ zanshin organization list [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage members within an organization.

**Usage**:

.. code:: console

   $ zanshin organization member [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``delete``: Remove a specific member from an...
-  ``get``: Get details of a specific member within an...
-  ``invite``: Manage member invitations for an...
-  ``list``: List the members of an organization the user...
-  ``update``: Update the role of a specific member within...

``zanshin organization member delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Remove a specific member from an organization.

**Usage**:

.. code:: console

   $ zanshin organization member delete [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_ID``: UUID of the organization member
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get details of a specific member within an organization.

**Usage**:

.. code:: console

   $ zanshin organization member get [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_ID``: UUID of the organization member
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage member invitations for an organization.

**Usage**:

.. code:: console

   $ zanshin organization member invite [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``create``: Send an invitation for a new user to join the...
-  ``delete``: Cancel a pending member invitation using the...
-  ``get``: Get details of a specific pending member...
-  ``list``: List all pending member invitations for an...
-  ``resend``: Resend an existing member invitation to the...

``zanshin organization member invite create``
'''''''''''''''''''''''''''''''''''''''''''''

Send an invitation for a new user to join the organization via email.

**Usage**:

.. code:: console

   $ zanshin organization member invite create [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the invited user
   [required]

**Options**:

-  ``--organization-member-invite-role [ADMIN]``: Role of the
   organization member [default: ADMIN]
-  ``--help``: Show this message and exit.

``zanshin organization member invite delete``
'''''''''''''''''''''''''''''''''''''''''''''

Cancel a pending member invitation using the invited email.

**Usage**:

.. code:: console

   $ zanshin organization member invite delete [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the invited user
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite get``
''''''''''''''''''''''''''''''''''''''''''

Get details of a specific pending member invitation using the invited
email.

**Usage**:

.. code:: console

   $ zanshin organization member invite get [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the invited user
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite list``
'''''''''''''''''''''''''''''''''''''''''''

List all pending member invitations for an organization the user has
access to.

**Usage**:

.. code:: console

   $ zanshin organization member invite list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite resend``
'''''''''''''''''''''''''''''''''''''''''''''

Resend an existing member invitation to the specified email address.

**Usage**:

.. code:: console

   $ zanshin organization member invite resend [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the invited user
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the members of an organization the user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization member list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the role of a specific member within an organization.

**Usage**:

.. code:: console

   $ zanshin organization member update [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_ID``: UUID of the organization member
   [required]

**Options**:

-  ``--role [ADMIN]``: Role of the organization member [default: ADMIN]
-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage scan target groups within an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``compartments``: List all Oracle Cloud (OCI) compartments...
-  ``create``: Create a new scan target group for an...
-  ``create-by-compartments``: Create scan targets from listed
   compartments...
-  ``delete``: Delete a specific scan target group from an...
-  ``get``: Get details of a specific scan target group...
-  ``insert``: Insert Oracle Cloud (OCI) credentials into an...
-  ``list``: List all scan target groups belonging to a...
-  ``oauth_link``: Retrieve an OAuth link to authorize Zanshin...
-  ``scan-targets``: List all scan targets belonging to a specific...
-  ``script``: Retrieve the script download URL for a...
-  ``update``: Update the name of a specific scan target...

``zanshin organization scan-target-groups compartments``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all Oracle Cloud (OCI) compartments associated with a specific scan
target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups compartments [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new scan target group for an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups create [OPTIONS] ORGANIZATION_ID KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK] NAME

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
   kind of the scan target group. Should be 'ORACLE' (Oracle Cloud
   Infrastructure (OCI)), 'BITBUCKET' (Bitbucket Cloud), or 'GITLAB'
   (GitLab.com) [required]
-  ``NAME``: name of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups create-by-compartments``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create scan targets from listed compartments within a specific scan
target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups create-by-compartments [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID NAME OCID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]
-  ``NAME``: Compartment name [required]
-  ``OCID``: Oracle Cloud Infrastructure (OCI) Compartment ID [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete a specific scan target group from an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups delete [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get details of a specific scan target group by its UUID.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups insert``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Insert Oracle Cloud (OCI) credentials into an existing scan target
group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups insert [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID REGION TENANCY_ID USER_ID KEY_FINGERPRINT

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]
-  ``REGION``: Oracle Cloud Infrastructure (OCI) region [required]
-  ``TENANCY_ID``: Oracle Cloud Infrastructure (OCI) tenancy ID
   [required]
-  ``USER_ID``: Oracle Cloud Infrastructure (OCI) user ID [required]
-  ``KEY_FINGERPRINT``: Oracle Cloud Infrastructure (OCI) API key
   fingerprint used for authentication [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all scan target groups belonging to a specific organization.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups oauth_link``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve an OAuth link to authorize Zanshin to access the scan target
group environment.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups oauth_link [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups scan-targets``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List all scan targets belonging to a specific scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups scan-targets [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups script``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve the script download URL for a specific scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups script [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan-target-groups update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the name of a specific scan target group.

**Usage**:

.. code:: console

   $ zanshin organization scan-target-groups update [OPTIONS] ORGANIZATION_ID SCAN_TARGET_GROUP_ID NAME

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_GROUP_ID``: UUID of the scan target group [required]
-  ``NAME``: new name of the scan target group [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage scan targets within an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``check``: Check the status and connectivity of a...
-  ``create``: Create a new scan target within a specific...
-  ``delete``: Delete a specific scan target from an...
-  ``get``: Get details of a specific scan target within...
-  ``list``: List the scan targets of an organization the...
-  ``oauth_link``: Retrieve an OAuth link to authorize Zanshin...
-  ``onboard_aws``: Create and onboard a new AWS scan target.
-  ``onboard_aws_organization``: Onboard multiple AWS Organization
   accounts as...
-  ``scan``: Manage and trigger scans for specific scan...
-  ``update``: Update the name or schedule of a specific...

``zanshin organization scan_target check``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the status and connectivity of a specific scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new scan target within a specific organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target create [OPTIONS] ORGANIZATION_ID KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK] NAME CREDENTIAL [SCHEDULE]

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``KIND:[AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
   kind of the scan target [required]
-  ``NAME``: name of the scan target [required]
-  ``CREDENTIAL``: credential of the scan target [required]
-  ``[SCHEDULE]``: schedule of the scan target [default: {"frequency":
   "1d", "timeOfDay": "NIGHT"}]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete a specific scan target from an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target delete [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get details of a specific scan target within an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the scan targets of an organization the user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization scan_target list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target oauth_link``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieve an OAuth link to authorize Zanshin to access the scan target
environment.

**Usage**:

.. code:: console

   $ zanshin organization scan_target oauth_link [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target onboard_aws``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create and onboard a new AWS scan target. Requires boto3 and specific
AWS IAM privileges. See docs:
`https://github.com/tenchi-security/zanshin-sdk-python/blob/main/zanshinsdk/docs/README.md <https://github.com/tenchi-security/zanshin-sdk-python/blob/main/zanshinsdk/docs/README.md>`__.

**Usage**:

.. code:: console

   $ zanshin organization scan_target onboard_aws [OPTIONS] REGION ORGANIZATION_ID NAME CREDENTIAL [SCHEDULE]

**Arguments**:

-  ``REGION``: Amazon Web Services (AWS) Region to deploy CloudFormation
   [required]
-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``NAME``: name of the scan target [required]
-  ``CREDENTIAL``: credential of the scan target [required]
-  ``[SCHEDULE]``: schedule of the scan target [default: {"frequency":
   "1d", "timeOfDay": "NIGHT"}]

**Options**:

-  ``--boto3-profile TEXT``: Boto3 profile name to use for Onboard
   Amazon Web Services (AWS) Account
-  ``--help``: Show this message and exit.

``zanshin organization scan_target onboard_aws_organization``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Onboard multiple AWS Organization accounts as new Zanshin scan targets.
Requires boto3 and AWS IAM privileges. See docs:
`https://github.com/tenchi-security/zanshin-cli/blob/main/src/lib/docs/README.md <https://github.com/tenchi-security/zanshin-cli/blob/main/src/lib/docs/README.md>`__.

**Usage**:

.. code:: console

   $ zanshin organization scan_target onboard_aws_organization [OPTIONS] REGION ORGANIZATION_ID [SCHEDULE]

**Arguments**:

-  ``REGION``: Amazon Web Services (AWS) Region to deploy CloudFormation
   [required]
-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``[SCHEDULE]``: schedule of the scan target [default: {"frequency":
   "1d", "timeOfDay": "NIGHT"}]

**Options**:

-  ``--target-accounts [ALL|MASTER|MEMBERS|NONE]``: choose which
   accounts to onboard
-  ``--exclude-account TEXT``: ID, Name, E-mail or ARN of Amazon Web
   Services (AWS) Account not to be onboarded
-  ``--boto3-profile TEXT``: Boto3 profile name to use for Onboard
   Amazon Web Services (AWS) Account
-  ``--aws-role-name TEXT``: Name of Amazon Web Services (AWS) role that
   allow access from Management Account to Member accounts [default:
   OrganizationAccountAccessRole]
-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage and trigger scans for specific scan targets.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``get``: Get details of a specific scan performed on a...
-  ``list``: List all scans performed on a specific scan...
-  ``start``: Start a new scan on the specified scan...
-  ``stop``: Stop a currently running scan on the...

``zanshin organization scan_target scan get``
'''''''''''''''''''''''''''''''''''''''''''''

Get details of a specific scan performed on a scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID SCAN_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]
-  ``SCAN_ID``: UUID of the scan [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan list``
''''''''''''''''''''''''''''''''''''''''''''''

List all scans performed on a specific scan target within an
organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan list [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan start``
'''''''''''''''''''''''''''''''''''''''''''''''

Start a new scan on the specified scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan start [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--force / --no-force``: Whether to force running a scan target that
   has state INVALID_CREDENTIAL or NEW [default: False]
-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan stop``
''''''''''''''''''''''''''''''''''''''''''''''

Stop a currently running scan on the specified scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan stop [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the name or schedule of a specific scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target update [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID [NAME] [SCHEDULE]

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]
-  ``[NAME]``: name of the scan target
-  ``[SCHEDULE]``: schedule of the scan target

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization update``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update an organization's details, such as name, picture or contact
email.

**Usage**:

.. code:: console

   $ zanshin organization update [OPTIONS] ORGANIZATION_ID [NAME] [PICTURE] [EMAIL]

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``[NAME]``: Name of the organization
-  ``[PICTURE]``: Picture of the organization
-  ``[EMAIL]``: Contact e-mail of the organization

**Options**:

-  ``--help``: Show this message and exit.

``zanshin summary``
-------------------

Generate aggregated data summaries and reports.

**Usage**:

.. code:: console

   $ zanshin summary [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``scan_targets_detail``: Generate a detailed summary of the...
-  ``scan_targets_following``: Generate a summary of scan targets for
   the...

``zanshin summary scan_targets_detail``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a detailed summary of the organization's scan targets, with
optional filtering.

**Usage**:

.. code:: console

   $ zanshin summary scan_targets_detail [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-ids UUID``: Only summarize scan targets from the
   specified scan target ids
-  ``--scan-target-tags TEXT``: Only summarize scan targets from the
   specified scan target tags
-  ``--scan-target-kinds [AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
   Only summarize scan targets from the specified kinds
-  ``--alert-severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only
   summarize alerts with the specified severities
-  ``--help``: Show this message and exit.

``zanshin summary scan_targets_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a summary of scan targets for the organization's followings,
with optional filtering.

**Usage**:

.. code:: console

   $ zanshin summary scan_targets_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only summarize scan targets from the
   specified following ids
-  ``--following-tags TEXT``: Only summarize scan targets from the
   specified following tags
-  ``--scan-target-kinds [AWS|AZURE|GCP|BITBUCKET|DOMAIN|GITHUB|GITLAB|GWORKSPACE|HUAWEI|JIRA|MS365|ORACLE|SALESFORCE|SLACK|ZENDESK]``:
   Only summarize scan targets from the specified kinds
-  ``--alert-severities [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only
   summarize alerts with the specified severities
-  ``--include-empty-following-tags / --no-include-empty-following-tags``:
   Include alerts from scan targets without tags
-  ``--help``: Show this message and exit.

``zanshin version``
-------------------

Display the current versions of the Zanshin CLI, SDK, and Python.

**Usage**:

.. code:: console

   $ zanshin version [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
