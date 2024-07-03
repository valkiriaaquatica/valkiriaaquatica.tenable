# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_plugin_families
short_description: Returns the list of plugin families.
version_added: "0.0.1"
description:
  - This module  returns the list of plugin families.
  - The module is made from https://developer.tenable.com/reference/io-plugins-families-list  docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  all:
    description:
      - Specifies whether to return all plugin families.
      - If true, the plugin families hidden in Tenable Vulnerability Management UI, for example, Port Scanners, are included in the list.
    required: true
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all plugin families
  list_plugin_families:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    all: true

- name: List not all plugin families using enviroment creds
  list_plugin_families:
    all: false
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: always
  contains:
    data:
      description: Contains data about different families of plugins or tools.
      type: dict
      contains:
        families:
          description: A list of family details retrieved from the API.
          type: list
          elements: dict
          contains:
            count:
              description: The number of plugins or items within this family.
              type: int
              returned: always
              sample: 1
            id:
              description: Unique identifier for the family.
              type: int
              returned: always
              sample: 1
            name:
              description: Name of the family, describing the category or type.
              type: str
              returned: always
              sample: "Windows : User management"
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
    special_args = {"all": {"required": True, "type": "bool"}}  # unique for this module
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"plugins/families?all=/{module.params['all']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
