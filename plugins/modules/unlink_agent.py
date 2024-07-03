# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: unlink_agent
short_description: Unlinks an agent.
version_added: "0.0.1"
description:
  - This module unlinks an agent.
  - The module is made from https://developer.tenable.com/reference/agents-delete docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.agent
"""

EXAMPLES = r"""
- name: Get information of a agent
  unlink_agent:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    agent_id: 11111

- name: Get information of a agent using enviroment keys
  unlink_agent:
    agent_id: 11111
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "agent_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scanners/null/agents/{module.params['agent_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
