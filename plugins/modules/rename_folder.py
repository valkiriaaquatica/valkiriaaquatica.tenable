# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rename_folder
short_description: Renames a folder for the current user.
version_added: "0.0.1"
description:
  - This module renames a folder for the current user.
  - You cannot rename Tenable-provided scan folders or custom folder that belong to other users (even if your account has administrator privileges).
  - The module is made from https://developer.tenable.com/reference/folders-edit docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  folder_id:
    description:
      - The ID of the folder to rename.
    required: true
    type: int
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Rename agent using enviroment creds
  rename_agent:
    agent_id: "123456789"
    name: "new_name"

- name: Rename agent using creds in vars
  rename_agent:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    agent_id: "123456789"
    name: "new_name"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Data content of the response from the Tenable API.
      type: dict
      returned: always
      sample: {}
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
    argument_spec = get_spec("access_key", "secret_key", "folder_id", "name")
    argument_spec["folder_id"]["required"] = True

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"folders/{module.params['folder_id']}"
    payload_keys = ["name"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
