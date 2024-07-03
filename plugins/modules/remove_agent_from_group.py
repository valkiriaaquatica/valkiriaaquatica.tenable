# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: remove_agent_from_group
short_description: Remove an agent from an agent group.
version_added: "0.0.1"
description:
  - This module removes an agent from the specified agent group.
  - This module is made from https://developer.tenable.com/reference/agent-groups-delete-agent docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.agent_group
  - valkiriaaquatica.tenable.agent
"""

EXAMPLES = r"""
- name: Remove agent to from aagent group
  remove_agent_from_group:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    group_id: "123456"
    agent_id: "654321"

- name: Remove an agent from an agent group using enviroment vars
  remove_agent_from_group:
    group_id: "{{ tenable_group_id }}"
    agent_id: "{{ tenable_agent_id }}"
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable api.
  returned: always when a request is made, independent if it correct or incorrect.
  type: complex
  contains:
    status_code:
      description: The HTTP status code returned by the API if an error occurred.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "agent_id")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agent-groups/{module.params['group_id']}/agents/{module.params['agent_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
