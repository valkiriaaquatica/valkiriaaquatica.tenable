# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_attribute
short_description: Updates the specified custom asset attribute.
version_added: "0.0.1"
description:
  - This module Updates the specified custom asset attribute.
  - Note You can only update non-key attributes like description.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/io-v3-asset-attributes-update docs.
options:
  description:
    description:
      - The new or updated description for the custom asset attribute.
      - Currently, description is the only non-primary key attribute that can be updated.
      - If the name field needs a new value, then you should create a new custom asset attribute via the POST /api/v3/assets/attributes endpoint.
    type: str
    required: false
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.attributes
"""

EXAMPLES = r"""
- name: Update the description of a custom asset attribute
  update_attribute:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    attribute_id: "123"
    description: "Updated description of the attribute"

- name: Update the description of a attribute using enviroment creds
  update_attribute:
    attribute_id: "123"
    description: "Updated description of the attribute"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "attribute_id", "description")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"api/v3/assets/attributes/{module.params['attribute_id']}"
    payload_keys = ["description"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
