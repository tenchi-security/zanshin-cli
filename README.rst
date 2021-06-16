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

**Usage**:

.. code:: console

   $ zanshin [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--install-completion``: Install completion for the current shell.
-  ``--show-completion``: Show completion for the current shell, to copy
   it or customize the installation.
-  ``--help``: Show this message and exit.

**Commands**:

-  ``init``: Update settings on configuration file.
-  ``me``: Show details about the owner of the API key...
-  ``organization``: Operations on organizations the API key owner...
-  ``version``: Display the program and Python versions in...

``zanshin init``
----------------

Update settings on configuration file.

**Usage**:

.. code:: console

   $ zanshin init [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``zanshin me``
--------------

Show details about the owner of the API key being used.

**Usage**:

.. code:: console

   $ zanshin me [OPTIONS]

**Options**:

-  ``--profile TEXT``: Configuration file section to use for credentials
   and other settings [default: default]
-  ``--help``: Show this message and exit.

``zanshin organization``
------------------------

Operations on organizations the API key owner has direct access to.

**Usage**:

.. code:: console

   $ zanshin organization [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``alerts``: List alerts from a given organization, with...
-  ``list``: Lists the organizations this user has direct...
-  ``scan_target``: Operations on scan targets from organizations...

``zanshin organization alerts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List alerts from a given organization, with optional filters by scan
target, state or severity.

**Usage**:

.. code:: console

   $ zanshin organization alerts [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization to list alerts from.
   [required]

**Options**:

-  ``--state [OPEN|ACTIVE|IN_PROGRESS|RISK_ACCEPTED|RESOLVED|CLOSED]``:
   Only list alerts in the specified states. [default: OPEN, ACTIVE,
   IN_PROGRESS, RISK_ACCEPTED, RESOLVED]
-  ``--severity [CRITICAL|HIGH|MEDIUM|LOW|INFO]``: Only list alerts with
   the specified severities. [default: CRITICAL, HIGH, MEDIUM, LOW,
   INFO]
-  ``--profile TEXT``: Configuration file section to use for credentials
   and other settings [default: default]
-  ``--format [json|table|csv|html]``: Format to use for the output.
   [default: json]
-  ``--help``: Show this message and exit.

``zanshin organization list``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists the organizations this user has direct access to as a member.

**Usage**:

.. code:: console

   $ zanshin organization list [OPTIONS]

**Options**:

-  ``--profile TEXT``: Configuration file section to use for credentials
   and other settings [default: default]
-  ``--format [json|table|csv|html]``: Format to use for the output.
   [default: json]
-  ``--help``: Show this message and exit.

``zanshin organization scan_target``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Operations on scan targets from organizations the API key owner has
direct access to.

**Usage**:

.. code:: console

   $ zanshin organization scan_target [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``check``: Check an scan_target status from an...
-  ``list``: Lists the scan targets from an organization...
-  ``scan``: Start an Scan in a specific scan_target from...

``zanshin organization scan_target check``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check an scan_target status from an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target check [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization to list alerts from.
   [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target to start scan. [required]

**Options**:

-  ``--profile TEXT``: Configuration file section to use for credentials
   and other settings [default: default]
-  ``--help``: Show this message and exit.

``zanshin organization scan_target list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists the scan targets from an organization that user has access to as a
member.

**Usage**:

.. code:: console

   $ zanshin organization scan_target list [OPTIONS] ORGANIZATION_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organizations whose scan targets
   should be listed. [required]

**Options**:

-  ``--profile TEXT``: Configuration file section to use for credentials
   and other settings [default: default]
-  ``--format [json|table|csv|html]``: Format to use for the output.
   [default: json]
-  ``--help``: Show this message and exit.

``zanshin organization scan_target scan``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Start an Scan in a specific scan_target from an organization.

**Usage**:

.. code:: console

   $ zanshin organization scan_target scan [OPTIONS] ORGANIZATION_ID SCAN_TARGET_ID

**Arguments**:

-  ``ORGANIZATION_ID``: UUID of the organization to list alerts from.
   [required]
-  ``SCAN_TARGET_ID``: UUID of the scan target to start scan. [required]

**Options**:

-  ``--profile TEXT``: Configuration file section to use for credentials
   and other settings [default: default]
-  ``--help``: Show this message and exit.

``zanshin version``
-------------------

Display the program and Python versions in use.

**Usage**:

.. code:: console

   $ zanshin version [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/zanshincli.svg
   :target: https://pypi.python.org/pypi/zanshincli/
