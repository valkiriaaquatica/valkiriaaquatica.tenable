# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: delete_group
short_description: Delete a group.
version_added: "0.0.1"
description:
  - This module deletes a group in Tenable.io.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/groups-delete docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: Delete a group
  delete_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 1233

- name: Delete a group using enviroment creds
  delete_group:
    group_id: 1233
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
    argument_spec = get_spec("access_key", "secret_key", "group_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"groups/{module.params['group_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
