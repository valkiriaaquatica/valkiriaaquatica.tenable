# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_attribute
short_description: Creates a new custom asset attribute.
version_added: "0.0.1"
description:
  - This module creates a new custom asset attribute in Tenable.io.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - The module is made from https://developer.tenable.com/reference/io-v3-asset-attributes-create docs.
options:
  attributes:
    description:
      - An array of new custom asset attributes.
    type: list
    elements: dict
    required: true
    suboptions:
      name:
        description:
          - The name of the custom asset attribute that you want to create. For example, Location.
        type: str
        required: false
      description:
        description:
          - A description of the custom asset attribute.
        type: str
        required: false
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Create two attributes
  create_attribute:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    attributes:
      - name: "Location"
        description: "The geographical location of the asset"
      - name: "Department"
        description: "The department to which the asset belongs"

- name: Create two attributes using enviroment creds
  create_attribute:
    attributes:
      - name: "Office"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {
        "attributes": {
            "required": True,
            "type": "list",
            "elements": "dict",
            "options": {"name": {"required": False, "type": "str"}, "description": {"required": False, "type": "str"}},
        }
    }

    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "api/v3/assets/attributes"
    payload_keys = ["attributes"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
