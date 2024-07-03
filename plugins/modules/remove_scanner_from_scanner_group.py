# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: remove_scanner_from_scanner_group
short_description: Remove a scanner from the scanner group.
version_added: "0.0.1"
description:
  - This module removes a scanner from the scanner group.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/scanner-groups-delete-scanner docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: Remove scanner from scanner group
  remove_scanner_from_scanner_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 12345
    scanner_id: 67890

- name: Remove  scanner from scanner group using enviroment creds
  remove_scanner_from_scanner_group:
    group_id: 12345
    scanner_id: 67890
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id", "scanner_id")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanner-groups/{module.params['group_id']}/scanners/{module.params['scanner_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
