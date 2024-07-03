# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: unlink_agent_windows
short_description: Unlinks a Tenable.IO agent from a Windows machine.
version_added: "0.0.1"
description:
  - Unlinks a Tenable.IO agent from a Windows server.
  - This module utilizes PowerShell to execute the Tenable Nessus Agent 'nessuscli.exe' command to unlink an agent.
  - Requires PowerShell v5.1 or higher on Windows Server 2016 and higher.
options: {}
notes:
  - This module does not support check mode.
  - Nessuscli.exe path of the module is the default C:\Program Files\Tenable\Nessus Agent\nessuscli.exe
  - Ensure that the 'nessuscli.exe' path is correct and accessible on the system where this module is run.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
"""

EXAMPLES = r"""
- name: Unlink Nessus Agent from Tenable.io
  unlink_agent_windows:
"""

RETURN = r"""
msg:
  description: The output message of the unlink command.
  type: str
  returned: always
  sample: "Agent unlinked successfully."
"""
