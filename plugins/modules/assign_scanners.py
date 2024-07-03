# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: assign_scanners
short_description: Associates a scanner or scanner group with a network object.
version_added: "0.0.1"
description:
  - This module associates a scanner or scanner group with a network object.
  - Use this endpoint to
    Assign a scanner or scanner group to a custom network object.
    Return a scanner or scanner group to the default network object.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/networks-assign-scanner  docs.
options:
  scanner_uuid:
    description:
      - The UUID of the scanner or scanner group you want to assign to the network object.
    type: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.network
"""

EXAMPLES = r"""
- name: Assign a scanner to a network object
  assign_scanners:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    network_id: "12345"
    scanner_uuid: "9874"

- name: Assign a scanner group to a network object using environment credentials
  assign_scanners:
    network_id: "12345"
    scanner_uuid: "9874"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_repeated_special_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {"scanner_uuid": {"required": True, "type": "str"}}
    special_spec = get_repeated_special_spec("network_id")

    argument_spec = {**common_spec, **specific_spec, **special_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"networks/{module.params['network_id']}/scanners/{module.params['scanner_uuid']}"

    run_module(module, endpoint, method="POST")


if __name__ == "__main__":
    main()
