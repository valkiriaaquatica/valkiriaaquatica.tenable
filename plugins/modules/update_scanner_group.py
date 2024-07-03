# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_scanner_group
short_description: Updates a scanner group.
version_added: "0.0.1"
description:
  - This module updates the name of a scanner group.
  - You cannot use this endpoint to
    Assign a scanner group to a network object. Instead, use the assign_scanners module.
    Update scan routes configured for the scanner group. Instead, use update_scan_routes module.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/scanner-groups-edit docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Update the name of a scanner group
  update_scanner_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 12345
    name: "New Group Name"

- name: Update the name of a scanner group using enviroment creds
  update_scanner_group:
    group_id: 12345
    name: "New Group Name"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    id:
      description: The ID of the scanner group.
      type: int
    name:
      description: The new name of the scanner group.
      type: str
    creation_date:
      description: The creation date of the scanner group.
      type: int
    last_modification_date:
      description: The last modification date of the scanner group.
      type: int
    owner_id:
      description: The owner ID of the scanner group.
      type: int
    owner:
      description: The owner of the scanner group.
      type: str
    owner_uuid:
      description: The UUID of the owner.
      type: str
    default_permissions:
      description: The default permissions for the scanner group.
      type: int
    user_permissions:
      description: The user permissions for the scanner group.
      type: int
    shared:
      description: Whether the scanner group is shared.
      type: int
    scan_count:
      description: The number of scans associated with the scanner group.
      type: int
    scanner_count:
      description: The number of scanners in the scanner group.
      type: int
    uuid:
      description: The UUID of the scanner group.
      type: str
    type:
      description: The type of the scanner group.
      type: str
    network_name:
      description: The name of the network associated with the scanner group.
      type: str
    scanner_id:
      description: The ID of the scanner in the scanner group.
      type: int
    scanner_uuid:
      description: The UUID of the scanner in the scanner group.
      type: str
    owner_name:
      description: The name of the owner of the scanner group.
      type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "name")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanner-groups/{module.params['group_id']}"

    payload_keys = ["name"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
