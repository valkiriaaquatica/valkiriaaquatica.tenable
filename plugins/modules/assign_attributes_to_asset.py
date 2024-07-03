# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: assign_attributes_to_asset
short_description: Assigns custom asset attributes to the specified asset.
version_added: "0.0.1"
description:
  - This module assigns custom asset attributes to the specified asset.
  - In Tenable.IO is specifed asset_id but the module changes to asset_uuid to keep the order in the collection.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - The module is made from https://developer.tenable.com/reference/io-v3-asset-attributes-assign docs.
options:
  attributes:
    description:
      - An array of custom asset attribute values to assign to the specified asset.
    type: list
    elements: dict
    required: true
    suboptions:
      id:
        description:
          - The ID of the custom asset attribute you want to assign to the asset.
        type: str
        required: true
      value:
        description:
          - The value of the custom asset attribute. For example, for a custom asset attribute named Location you could assign a value of Dallas.
        type: str
        required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
"""

EXAMPLES = r"""
- name: Assign custom asset attributes to an asset
  assign_attributes_to_asset:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_id: "12345"
    attributes:
      - id: "123456"
        value: "Dallas"

- name: Assign custom asset attributes to an asset using enviroment creds
  assign_attributes_to_asset:
    asset_id: "12345"
    attributes:
      - id: "123456"
        value: "Dallas"
      - id: "23897"
        value: "Paris"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "asset_uuid")
    specific_spec = {
        "attributes": {
            "required": True,
            "type": "list",
            "elements": "dict",
            "options": {"id": {"required": True, "type": "str"}, "value": {"required": True, "type": "str"}},
        }
    }

    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"api/v3/assets/{module.params['asset_uuid']}/attributes"
    payload_keys = ["attributes"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
