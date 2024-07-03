# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: create_scanner_group
short_description: Creates a new scanner group.
version_added: "0.0.1"
description:
  - This module creates a new scanner group.
  - You cannot use this endpoint to
    Assign the new scanner group to a network object.able Vulnerability Management automatically assigns new scanner
    groups to the default network object. To assign a scanner group to a network object, use the assign_scanners module.
  - Configure scan routes for the scanner group. Instead, use the update_scan_routes module.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/scanner-groups-create .
options:
  type:
    description:
      - The type of scanner group. If omitted, the default is load_balancing.
    type: str
    choices: ["load_balancing"]
    required: false
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Create a new scanner group with default type
  create_scanner_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    name: "Example Group"
    type: "load_balancing"

- name: Create a new scanner group with specified type using environment credentials
  create_scanner_group:
    name: "Example Group"
    type: "load_balancing"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    creation_date:
      description: Creation timestamp.
      type: int
    last_modification_date:
      description: Last modification timestamp.
      type: int
    owner_id:
      description: ID of the owner.
      type: int
    owner:
      description: Name of the owner.
      type: str
    owner_uuid:
      description: UUID of the owner.
      type: str
    default_permissions:
      description: Default permissions.
      type: int
    scan_count:
      description: Number of scans.
      type: int
    uuid:
      description: UUID of the scanner group.
      type: str
    type:
      description: Type of the scanner group.
      type: str
    name:
      description: Name of the scanner group.
      type: str
    id:
      description: ID of the scanner group.
      type: int
    owner_name:
      description: Name of the owner.
      type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "name")
    specific_spec = {"type": {"required": False, "type": "str", "choices": ["load_balancing"]}}
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scanner-groups"

    payload_keys = ["name", "type"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
