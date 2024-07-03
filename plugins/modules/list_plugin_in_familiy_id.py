# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_plugin_in_familiy_id
short_description: Returns the list of plugins for the specified family ID.
version_added: "0.0.1"
description:
  - This module  returns the list of plugins for the specified family ID.
  - The module is made from https://developer.tenable.com/reference/io-plugins-family-details-idt  docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  id:
    description:
      - The ID of the plugin family you want to retrieve the list of plugins for.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""


EXAMPLES = r"""
- name: List plugin in family
  list_plugin_in_familiy_id:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    id: 123456

- name: List plugns in family using enviroment creds
  list_plugin_families:
    id: 123456
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: always
  contains:
    data:
      description: Contains data about a specific plugins.
      type: dict
      contains:
        id:
          description: Unique identifier of the plugin.
          type: int
          returned: always
          sample: 1
        name:
          description: Name of the category or group, describing the type of plugin.
          type: str
          returned: always
          sample: "Windows : Problems"
        plugins:
          description: A list of plugins within the specified category.
          type: list
          elements: dict
          contains:
            id:
              description: Unique identifier for the plugin.
              type: int
              returned: always
              sample: 1
            name:
              description: Name of the plugin.
              type: str
              returned: always
              sample: "windows_name"
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    special_args = {"id": {"required": True, "type": "str"}}
    argument_spec = {**common_spec, **special_args}  # unique for this module
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"plugins/families/{module.params['id']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
