# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: link_agent_windows
short_description: Links a Tenable.IO agent to a windows.
version_added: "0.0.1"
description:
  - Links a Tenable.IO agent to a windows server using provided agent linking key and configuration.
  - This module utilizes PowerShell to execute the Tenable Nessus Agent 'nessuscli.exe' command to link an agent.
  - Requires PowerShell v5.1 or higher on Windows Server 2016 and higher.
options:
  linking_key:
    description:
      - The agent linking key as provided by Tenable.IO.
    required: true
    type: str
  name:
    description:
      - The name for the agent being linked.
      - It is normally use the hostname of the machine.
    required: true
    type: str
  groups:
    description:
      - The groups to which the agent should belong.
      - This is a previous agent groups that existis
      - Check list_agent_groups module for more.
    required: true
    type: str
  network:
    description:
      - The network where the agent will be connected.
      - This a network that needs to exists.
      - Check list_networks module for more.
    required: true
    type: str
  host:
    description:
      - The domain of tenable.
    required: true
    type: str
  port:
    description:
      - The port of Tenable.
    required: true
    type: int
notes:
  - This module does not support check mode.
  - Nesuscli.exe path of the module is the default C:\Program Files\Tenable\Nessus Agent\nessuscli.exe
  - Ensure that the 'nessuscli.exe' path is correct and accessible on the system where this module is run.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
"""

EXAMPLES = r"""
- name: Link Nessus Agent to Tenable.io
  link_agent_windows:
    linking_key: "{{ your_linking_key_here }}"
    name: "{{ ansible_hostname  }}"
    groups: "{{ tenable_group }}"
    network: "{{ tenable_network }}"
    host: "cloud.tenable.com"
    port: 443

- name: Link Nessus Agent to Tenable.sc
  link_agent_windows:
    linking_key: "your_linking_key_here"
    name: "my_nessus_agent"
    groups: "Linux Servers,Datacenter 2"
    network: "Your Network"
    host: "tenable.yourdomain.com"
    port: 8834
  become: true
"""

RETURN = r"""
msg:
  description: The output message of the linking command.
  type: str
  returned: always
  sample: "Agent linked successfully."
rc:
  description: The return code of the command.
  type: int
  returned: always
  sample: 0
changed:
  description: A boolean that indicates if there was a change in the state of the target.
  returned: always
  type: bool
  sample: false
"""
