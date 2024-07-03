# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scanners_within_scanner_group
short_description: Lists scanners associated with the scanner group.
version_added: "0.0.1"
description:
  - This module lists scanners associated with the scanner group.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/scanner-groups-list-scanners .
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: List scanners within a scanner group
  list_scanners_within_scanner_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 12345

- name: List scanners within a scanner group using enviroment creds
  list_scanners_within_scanner_group:
    group_id: 12345
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    scanners:
      description: List of scanners in the scanner group.
      type: list
      elements: dict
      contains:
        creation_date:
          description: The creation date of the scanner.
          type: int
        group:
          description: Indicates if the scanner is part of a group.
          type: bool
        id:
          description: The ID of the scanner.
          type: int
        key:
          description: The key of the scanner.
          type: str
        last_connect:
          description: The last connection date of the scanner.
          type: int
        last_modification_date:
          description: The last modification date of the scanner.
          type: int
        license:
          description: License information of the scanner.
          type: dict
        linked:
          description: Indicates if the scanner is linked.
          type: int
        name:
          description: The name of the scanner.
          type: str
        num_scans:
          description: The number of scans run by the scanner.
          type: int
        owner:
          description: The owner of the scanner.
          type: str
        owner_id:
          description: The ID of the owner.
          type: int
        owner_name:
          description: The name of the owner.
          type: str
        owner_uuid:
          description: The UUID of the owner.
          type: str
        pool:
          description: Indicates if the scanner is a pool.
          type: bool
        scan_count:
          description: The count of scans performed.
          type: int
        source:
          description: The source of the scanner.
          type: str
        status:
          description: The status of the scanner.
          type: str
        timestamp:
          description: The timestamp of the scanner.
          type: int
        type:
          description: The type of the scanner.
          type: str
        uuid:
          description: The UUID of the scanner.
          type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanner-groups/{module.params['group_id']}/scanners"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
