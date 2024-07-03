# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: add_agent_to_group
short_description: Adds an agent to the agent group.
version_added: "0.0.1"
description:
  - This module adds an agent to the agent group.
  - You can use the get_agent_group_details module to verify that the agent was added to the specified agent group.
  - This module is made from https://developer.tenable.com/reference/agent-groups-add-agent  docs.
  - Requires  SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  group_id:
    description:
      - The ID of the agent group.
    required: true
    type: str
  agent_id:
    description:
      - The ID of the agent to add.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Add agent to a existing agent group
  add_agent_to_group:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    group_id: "123456"
    agent_id: "654321"

- name: Add an agent to a group using enviroment creds
  add_agent_to_group:
    group_id: "{{ tenable_group_id }}"
    agent_id: "{{ tenable_agent_id }}"
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "agent_id")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agent-groups/{module.params['group_id']}/agents/{module.params['agent_id']}"

    run_module(module, endpoint, method="PUT")


if __name__ == "__main__":
    main()
