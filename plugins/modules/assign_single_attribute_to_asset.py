# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: assign_single_attribute_to_asset
short_description: Assigns a single custom asset attribute to the specified asset.
version_added: "0.0.1"
description:
  - This module assigns a single custom asset attribute to the specified asset.
  - Module made from https://developer.tenable.com/reference/io-v3-asset-attributes-single-update docs.
  - Requires BASIC  [16] user permissions
options:
  value:
    description:
      - The value of the custom asset attribute.
      - For example, for a custom asset attribute named Location you could assign a value of Dallas.
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
  - valkiriaaquatica.tenable.attributes
"""

EXAMPLES = r"""
- name: Update tag value
  assign_single_attribute_to_asset:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_uuid: "123456"
    attribute_id: "987465"
    value: "this_is_the_new_value"

- name: Update tag value with envirometn creds and new filters
  assign_single_attribute_to_asset:
    asset_uuid: "123456"
    attribute_id: "9874"
    value: "this_is_the_new_value"
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid", "attribute_id", "value")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = ["value"]
    payload = build_payload(module, payload_keys)

    endpoint = f"api/v3/assets/{module.params['asset_uuid']}/attributes/{module.params['attribute_id']}"

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
