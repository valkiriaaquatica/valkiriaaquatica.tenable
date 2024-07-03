# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_agent_group_name
short_description: Changes the name of the agent group.
version_added: "0.0.1"
description:
  - This module changes the name of the agent group.
  - This module is made from https://developer.tenable.com/reference/agent-groups-configure docs.
  - Requires  SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
  - valkiriaaquatica.tenable.name
"""


EXAMPLES = r"""
- name: Update the name of an agent with enviroment creds
  update_agent_group_name:
    group_id: 123456
    name: new_name

- name: Update the name of an agent passing credentials
  update_agent_group_name:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 123456
    name: new_name
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  returned: on sucess.
  type: dict
  contains:
    data:
      description: Contains various details about the entity, such as agent count, creation and modification details, and ownership.
      type: dict
      returned: always
      sample:
        agents_count: 1
        container_uuid: "123456"
        created: 123456
        created_in_seconds: 123456
        id: 166090
        modified: 123456
        modified_in_seconds: 123456
        name: "name"
        owner_uuid: "123456"
        shared: 1
        user_permissions: 1
        uuid: "123456"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "name")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scanners/null/agent-groups/{module.params['group_id']}"
    payload_keys = ["name"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
