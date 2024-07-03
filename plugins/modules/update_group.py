# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_group
short_description: Edit a group.
version_added: "0.0.1"
description:
  - This module edits a group in Tenable.io.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - This module is made with https://developer.tenable.com/reference/groups-edit docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Update the name of a group
  update_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 1233
    name: "New Group Name"

- name: Update the name of a group using enviroment creds
  update_group:
    group_id: 1233
    name: "New Group Name"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    uuid:
      description: The unique identifier for the group.
      type: str
    name:
      description: The name of the group.
      type: str
    permissions:
      description: The permissions of the group.
      type: int
    container_uuid:
      description: The UUID of the container.
      type: str
    user_count:
      description: The number of users in the group.
      type: int
    id:
      description: The ID of the group.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "name")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"groups/{module.params['group_id']}"

    payload_keys = ["name"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
