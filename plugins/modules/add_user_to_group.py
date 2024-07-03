# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: add_user_to_group
short_description: Add a user to a group.
version_added: "0.0.1"
description:
  - This module adds a user to a specified group.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/groups-add-user docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.user
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: Add a user to a group using explicit credentials
  add_user_to_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 1234
    user_id: 5444

- name: Add a user to a group using environment credentials
  add_user_to_group:
    group_id: 1234
    user_id: 5444
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "user_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"groups/{module.params['group_id']}/users/{module.params['user_id']}"

    run_module(module, endpoint, method="POST")


if __name__ == "__main__":
    main()
