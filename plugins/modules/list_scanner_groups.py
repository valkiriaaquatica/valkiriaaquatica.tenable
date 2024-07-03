# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scanner_groups
short_description: Lists scanner groups for your Tenable Vulnerability Management instance.
version_added: "0.0.1"
description:
  - This module lists scanner groups for your Tenable Vulnerability Management instance.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List scanner groups
  list_scanner_groups:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"

- name: List scanner groups using enviroment creds
  list_scanner_groups:
"""

RETURN = r"""
scanner_pools:
  description: A list of scanner groups.
  type: list
  elements: dict
  returned: os success
  contains:
    creation_date:
      description: The creation date of the scanner group.
      type: int
    last_modification_date:
      description: The last modification date of the scanner group.
      type: int
    owner_id:
      description: The ID of the owner of the scanner group.
      type: int
    owner:
      description: The owner of the scanner group.
      type: str
    owner_uuid:
      description: The UUID of the owner of the scanner group.
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
      description: The number of scans in the scanner group.
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
    name:
      description: The name of the scanner group.
      type: str
    network_name:
      description: The name of the network associated with the scanner group.
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
      description: The name of the owner of the scanner group.
      type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scanner-groups"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
