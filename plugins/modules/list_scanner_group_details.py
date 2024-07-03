# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scanner_group_details
short_description: Returns details for the specified scanner group.
version_added: "0.0.1"
description:
  - This module returns details for the specified scanner group.
  - Note This endpoint does not return details about scan routes configured for the scanner group.
   For scan routes, use the GET /scanner-groups/group_id/routes endpoint instead.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/scanner-groups-details  docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: Get details of a scanner group
  list_scanner_group_details:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 12345

- name: Get details of a scanner group using environment credentials
  list_scanner_group_details:
    group_id: 12345
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    creation_date:
      description: The creation date of the scanner group.
      type: int
    last_modification_date:
      description: The last modification date of the scanner group.
      type: int
    owner_id:
      description: The ID of the owner.
      type: int
    owner:
      description: The name of the owner.
      type: str
    owner_uuid:
      description: The UUID of the owner.
      type: str
    default_permissions:
      description: The default permissions of the scanner group.
      type: int
    user_permissions:
      description: The user permissions of the scanner group.
      type: int
    shared:
      description: Indicates if the scanner group is shared.
      type: int
    scan_count:
      description: The number of scans.
      type: int
    scanner_count:
      description: The number of scanners in the group.
      type: int
    uuid:
      description: The UUID of the scanner group.
      type: str
    type:
      description: The type of the scanner group.
      type: str
    name:
      description: The name of the scanner group.
      type: str
    network_name:
      description: The name of the network.
      type: str
    id:
      description: The ID of the scanner group.
      type: int
    scanner_id:
      description: The ID of the scanner.
      type: int
    scanner_uuid:
      description: The UUID of the scanner.
      type: str
    owner_name:
      description: The name of the owner.
      type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanner-groups/{module.params['group_id']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
