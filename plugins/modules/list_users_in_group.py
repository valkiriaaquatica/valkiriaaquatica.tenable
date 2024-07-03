# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_users_in_group
short_description: Return the group user list.
version_added: "0.0.1"
description:
  - This module returns the list of users in a specified group in Tenable.io.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/groups-list-users docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: List users in a group using explicit credentials
  list_users_in_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 1233

- name: List users in a group using environment creds
  list_users_in_group:
    group_id: 1233
"""

RETURN = r"""
api_response:
  description: Response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    users:
      description: List of users in the group.
      type: list
      elements: dict
      contains:
        id:
          description: Unique ID of the user.
          type: int
        user_name:
          description: Username of the user.
          type: str
        username:
          description: Username of the user.
          type: str
        email:
          description: Email of the user.
          type: str
        name:
          description: Name of the user.
          type: str
        type:
          description: Type of the user.
          type: str
        permissions:
          description: Permissions assigned to the user.
          type: int
        last_login_attempt:
          description: Timestamp of the last login attempt.
          type: int
        login_fail_count:
          description: Number of login failures.
          type: int
        login_fail_total:
          description: Total number of login failures.
          type: int
        enabled:
          description: Whether the user is enabled or not.
          type: bool
        uuid:
          description: UUID of the user.
          type: str
        container_uuid:
          description: Container UUID of the user.
          type: str
        uuid_id:
          description: UUID ID of the user.
          type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"groups/{module.params['group_id']}/users"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
