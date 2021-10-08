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
for license, source code and documentation

**Usage**:

.. code:: console

   $ zanshin [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--profile TEXT``: Configuration file section to read API key and
   configutation from [default: default]
-  ``--format [json|table|csv|html]``: Output format to use for list
   operations [default: json]
-  ``--verbose / --no-verbose``: Print timiing and other information to
   stderr [default: True]
-  ``--install-completion``: Install completion for the current shell.
-  ``--show-completion``: Show completion for the current shell, to copy
   it or customize the installation.
-  ``--help``: Show this message and exit.

**Commands**:

-  ``init``: Update settings on configuration file.
-  ``version``: Display the program and Python versions in...
-  ``account``: Operations on user the API key owner has...
-  ``organization``: Operations on organizations the API key owner...
-  ``alert``: Operations on alerts the API key owner has...
-  ``summary``: Operations on summaries the API key owner has...

``zanshin init``
----------------

Update settings on configuration file.

**Usage**:

.. code:: console

   $ zanshin init [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin version``
-------------------

Display the program and Python versions in use.

**Usage**:

.. code:: console

   $ zanshin version [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account``
-------------------

Operations on user the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin account [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``me``: Returns the details of the user account that...
-  ``invites``: Operations on invites from account the API...
-  ``api_key``: Operations on API keys from account the API...

``zanshin account me``
~~~~~~~~~~~~~~~~~~~~~~

Returns the details of the user account that owns the API key used by
this Connection instance as per

**Usage**:

.. code:: console

   $ zanshin account me [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account invites``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on invites from account the API key owner has direct access
to

**Usage**:

.. code:: console

   $ zanshin account invites [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Iterates over the invites of current logged...
-  ``get``: Gets an specific invitation details, it only...
-  ``accept``: Accepts an inivitation with the informed ID,...

``zanshin account invites list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterates over the invites of current logged user.

**Usage**:

.. code:: console

   $ zanshin account invites list [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account invites get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gets an specific invitation details, it only works if the invitation was
made for the current logged user.

**Usage**:

.. code:: console

   $ zanshin account invites get [OPTIONS] INVITE_ID

**Arguments**:

-  ``INVITE_ID``: UUID of the invite [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account invites accept``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Accepts an inivitation with the informed ID, it only works if the user
accepting the invitation is the user that received the invitation.

**Usage**:

.. code:: console

   $ zanshin account invites accept [OPTIONS] INVITE_ID

**Arguments**:

-  ``INVITE_ID``: UUID of the invite [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account api_key``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on API keys from account the API key owner has direct access
to

**Usage**:

.. code:: console

   $ zanshin account api_key [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Iterates over the API keys of current logged...
-  ``create``: Creates a new API key for the current logged...
-  ``delete``: Deletes a given API key by its id, it will...

``zanshin account api_key list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterates over the API keys of current logged user.

**Usage**:

.. code:: console

   $ zanshin account api_key list [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account api_key create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates a new API key for the current logged user, API Keys can be used
to interact with the zanshin api directly on behalf of that user.

**Usage**:

.. code:: console

   $ zanshin account api_key create [OPTIONS] NAME

**Arguments**:

-  ``NAME``: Name of the new API key [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin account api_key delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deletes a given API key by its id, it will only work if the informed ID
belongs to the current logged user.

**Usage**:

.. code:: console

   $ zanshin account api_key delete [OPTIONS] API_KEY_ID

**Arguments**:

-  ``API_KEY_ID``: UUID of the invite to delete [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization``
------------------------

Operations on organizations the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin organization [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the organizations this user has direct...
-  ``get``: Gets an organization given its ID.
-  ``update``: Gets an organization given its ID.
-  ``member``: Operations on members of organization the API...
-  ``follower``: Operations on followers of organization the...
-  ``following``: Operations on following of organization the...
-  ``scan_target``: Operations on scan targets from organizations...

``zanshin organization list``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists the organizations this user has direct access to as a member.

**Usage**:

.. code:: console

   $ zanshin organization list [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization get``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gets an organization given its ID.

**Usage**:

.. code:: console

   $ zanshin organization get [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization update``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gets an organization given its ID.

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

``zanshin organization member``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on members of organization the API key owner has direct
access to

**Usage**:

.. code:: console

   $ zanshin organization member [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the members of organization this user...
-  ``get``: Get organization member.
-  ``update``: Update organization member.
-  ``delete``: Delete organization member.
-  ``invite``: Operations on member invites of organization...

``zanshin organization member list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the members of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization member list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get organization member.

**Usage**:

.. code:: console

   $ zanshin organization member get [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_ID``: UUID of the organization member
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update organization member.

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

``zanshin organization member delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete organization member.

**Usage**:

.. code:: console

   $ zanshin organization member delete [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_ID``: UUID of the organization member
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on member invites of organization the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization member invite [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the member invites of organization this...
-  ``create``: Create organization member invite.
-  ``get``: Get organization member invite.
-  ``delete``: Delete organization member invite.
-  ``resend``: Resend organization member invitation.

``zanshin organization member invite list``
'''''''''''''''''''''''''''''''''''''''''''

Lists the member invites of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization member invite list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite create``
'''''''''''''''''''''''''''''''''''''''''''''

Create organization member invite.

**Usage**:

.. code:: console

   $ zanshin organization member invite create [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
   member [required]

**Options**:

-  ``--organization-member-invite-role [ADMIN]``: Role of the
   organization member [default: ADMIN]
-  ``--help``: Show this message and exit.

``zanshin organization member invite get``
''''''''''''''''''''''''''''''''''''''''''

Get organization member invite.

**Usage**:

.. code:: console

   $ zanshin organization member invite get [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
   member invite [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite delete``
'''''''''''''''''''''''''''''''''''''''''''''

Delete organization member invite.

**Usage**:

.. code:: console

   $ zanshin organization member invite delete [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
   member [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization member invite resend``
'''''''''''''''''''''''''''''''''''''''''''''

Resend organization member invitation.

**Usage**:

.. code:: console

   $ zanshin organization member invite resend [OPTIONS] ORGANIZATION_ID ORGANIZATION_MEMBER_INVITE_EMAIL

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_MEMBER_INVITE_EMAIL``: E-mail of the organization
   member [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on followers of organization the API key owner has direct
access to

**Usage**:

.. code:: console

   $ zanshin organization follower [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the followers of organization this user...
-  ``stop``: Stops one organization follower of another.
-  ``request``: Operations on follower requests of...

``zanshin organization follower list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the followers of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization follower list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops one organization follower of another.

**Usage**:

.. code:: console

   $ zanshin organization follower stop [OPTIONS] ORGANIZATION_ID ORGANIZATION_FOLLOWER_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_FOLLOWER_ID``: UUID of the organization follower
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on follower requests of organization the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization follower request [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the follower requests of organization...
-  ``create``: Create organization follower request.
-  ``get``: Get organization follower request.
-  ``delete``: Delete organization follower request.

``zanshin organization follower request list``
''''''''''''''''''''''''''''''''''''''''''''''

Lists the follower requests of organization this user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization follower request list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request create``
''''''''''''''''''''''''''''''''''''''''''''''''

Create organization follower request.

**Usage**:

.. code:: console

   $ zanshin organization follower request create [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``TOKEN``: Token of the follower request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request get``
'''''''''''''''''''''''''''''''''''''''''''''

Get organization follower request.

**Usage**:

.. code:: console

   $ zanshin organization follower request get [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``TOKEN``: Token of the follower request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization follower request delete``
''''''''''''''''''''''''''''''''''''''''''''''''

Delete organization follower request.

**Usage**:

.. code:: console

   $ zanshin organization follower request delete [OPTIONS] ORGANIZATION_ID TOKEN

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``TOKEN``: Token of the follower request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on following of organization the API key owner has direct
access to

**Usage**:

.. code:: console

   $ zanshin organization following [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the following of organization this user...
-  ``stop``: Stops one organization following of another.
-  ``request``: Operations on following requests of...

``zanshin organization following list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the following of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization following list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops one organization following of another.

**Usage**:

.. code:: console

   $ zanshin organization following stop [OPTIONS] ORGANIZATION_ID ORGANIZATION_FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``ORGANIZATION_FOLLOWING_ID``: UUID of the organization following
   [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on following requests of organization the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization following request [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the following requests of organization...
-  ``get``: Returns a request received by an organization...
-  ``accept``: Accepts a request to follow another...
-  ``decline``: Declines a request to follow another...

``zanshin organization following request list``
'''''''''''''''''''''''''''''''''''''''''''''''

Lists the following requests of organization this user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization following request list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request get``
''''''''''''''''''''''''''''''''''''''''''''''

Returns a request received by an organization to follow another.

**Usage**:

.. code:: console

   $ zanshin organization following request get [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization following request accept``
'''''''''''''''''''''''''''''''''''''''''''''''''

Accepts a request to follow another organization.

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

Declines a request to follow another organization.

**Usage**:

.. code:: console

   $ zanshin organization following request decline [OPTIONS] ORGANIZATION_ID FOLLOWING_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``FOLLOWING_ID``: UUID of the following request [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on scan targets from organizations the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization scan_target [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: Lists the scan targets of organization this...
-  ``create``: Create a new scan target in organization.
-  ``get``: Get scan target of organization.
-  ``update``: Update scan target of organization.
-  ``delete``: Delete scan target of organization.
-  ``check``: Check scan target.
-  ``scan``: Operations on scan targets from organizations...

``zanshin organization scan_target list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the scan targets of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization scan_target list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new scan target in organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target create [OPTIONS] ORGANIZATION_ID KIND:[AWS|GCP|AZURE] NAME CREDENTIAL [SCHEDULE]

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``KIND:[AWS|GCP|AZURE]``: kind of the scan target [required]
-  ``NAME``: name of the scan target [required]
-  ``CREDENTIAL``: credential of the scan target [required]
-  ``[SCHEDULE]``: schedule of the scan target [default: 0 0 \* \* \*]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get scan target of organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target update``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update scan target of organization.

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

``zanshin organization scan_target delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete scan target of organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target delete [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target check``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operations on scan targets from organizations the API key owner has
direct access to

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``start``: Starts a scan on the specified scan target.
-  ``list``: Lists the scan target scans of organization...
-  ``get``: Get scan of scan target.

``zanshin organization scan_target scan start``
'''''''''''''''''''''''''''''''''''''''''''''''

Starts a scan on the specified scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan start [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan list``
''''''''''''''''''''''''''''''''''''''''''''''

Lists the scan target scans of organization this user has direct access
to.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan list [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan get``
'''''''''''''''''''''''''''''''''''''''''''''

Get scan of scan target.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan get [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID SCAN_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target [required]
-  ``SCAN_ID``: UUID of the scan [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin alert``
-----------------

Operations on alerts the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin alert [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list``: List alerts from a given organization, with...
-  ``list_following``: List following alerts from a given...
-  ``grouped_list``: List grouped alerts from a given...
-  ``grouped_list_following``: List grouped following alerts from a
   given...
-  ``get``: Returns details about a specified alert
-  ``list_history``: Lists the alert history of organization this...
-  ``list_comment``: Lists the alert comments of organization this...

``zanshin alert list``
~~~~~~~~~~~~~~~~~~~~~~

List alerts from a given organization, with optional filters by scan
target, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-id UUID``: Only list alerts from the specified scan
   targets.
-  ``--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|SOLVED|CLOSED]``:
   Only list alerts in the specified states. [default: OPEN, ACTIVE,
   IN_PROGRESS, RISK_ACCEPTED, SOLVED]
-  ``--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts with
   the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
-  ``--help``: Show this message and exit.

``zanshin alert list_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List following alerts from a given organization, with optional filters
by following ids, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert list_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only list alerts from the specified scan
   targets.
-  ``--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|SOLVED|CLOSED]``:
   Only list alerts in the specified states. [default: OPEN, ACTIVE,
   IN_PROGRESS, RISK_ACCEPTED, SOLVED]
-  ``--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts with
   the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
-  ``--help``: Show this message and exit.

``zanshin alert grouped_list``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List grouped alerts from a given organization, with optional filters by
scan target, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert grouped_list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-id UUID``: Only list alerts from the specified scan
   targets.
-  ``--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|SOLVED|CLOSED]``:
   Only list alerts in the specified states. [default: OPEN, ACTIVE,
   IN_PROGRESS, RISK_ACCEPTED, SOLVED]
-  ``--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts with
   the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
-  ``--help``: Show this message and exit.

``zanshin alert grouped_list_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List grouped following alerts from a given organization, with optional
filters by scan target, state or severity.

**Usage**:

.. code:: console

   $ zanshin alert grouped_list_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only list alerts from the specified scan
   targets.
-  ``--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|SOLVED|CLOSED]``:
   Only list alerts in the specified states. [default: OPEN, ACTIVE,
   IN_PROGRESS, RISK_ACCEPTED, SOLVED]
-  ``--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts with
   the specified severities [default: CRITICAL, HIGH, MEDIUM, LOW, INFO]
-  ``--help``: Show this message and exit.

``zanshin alert get``
~~~~~~~~~~~~~~~~~~~~~

Returns details about a specified alert

**Usage**:

.. code:: console

   $ zanshin alert get [OPTIONS] ALERT_ID

**Arguments**:

-  ``ALERT_ID``: UUID of the alert to look up [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin alert list_history``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists the alert history of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin alert list_history [OPTIONS] ALERT_ID

**Arguments**:

-  ``ALERT_ID``: UUID of the alert to look up [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin alert list_comment``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists the alert comments of organization this user has direct access to.

**Usage**:

.. code:: console

   $ zanshin alert list_comment [OPTIONS] ALERT_ID

**Arguments**:

-  ``ALERT_ID``: UUID of the alert to look up [required]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin summary``
-------------------

Operations on summaries the API key owner has direct access to

**Usage**:

.. code:: console

   $ zanshin summary [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``alert``: Gets a summary of the current state of alerts...
-  ``alert_following``: Gets a summary of the current state of alerts...
-  ``scan``: Returns summaries of scan results over a...
-  ``scan_following``: Returns summaries of scan results over a...

``zanshin summary alert``
~~~~~~~~~~~~~~~~~~~~~~~~~

Gets a summary of the current state of alerts for an organization, both
in total and broken down by scan target.

**Usage**:

.. code:: console

   $ zanshin summary alert [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-id UUID``: Only summarize alerts from the specified
   scan targets, defaults to all.
-  ``--help``: Show this message and exit.

``zanshin summary alert_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gets a summary of the current state of alerts for followed
organizations.

**Usage**:

.. code:: console

   $ zanshin summary alert_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only summarize alerts from the specified
   following, defaults to all.
-  ``--help``: Show this message and exit.

``zanshin summary scan``
~~~~~~~~~~~~~~~~~~~~~~~~

Returns summaries of scan results over a period of time, summarizing
number of alerts that changed states.

**Usage**:

.. code:: console

   $ zanshin summary scan [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--scan-target-ids UUID``: Only summarize alerts from the specified
   scan targets, defaults to all.
-  ``--days INTEGER``: Number of days to go back in time in historical
   search [default: 7]
-  ``--help``: Show this message and exit.

``zanshin summary scan_following``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns summaries of scan results over a period of time, summarizing
number of alerts that changed states.

**Usage**:

.. code:: console

   $ zanshin summary scan_following [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization [required]

**Options**:

-  ``--following-ids UUID``: Only summarize alerts from the specified
   following, defaults to all.
-  ``--days INTEGER``: Number of days to go back in time in historical
   search [default: 7]
-  ``--help``: Show this message and exit.

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
