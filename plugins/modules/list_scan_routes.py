# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scan_routes
short_description: List scan routes within a scanner group.
version_added: "0.0.1"
description:
  - This module lists the hostnames, wildcards, IP addresses, and IP address ranges that Tenable Vulnerability
    Management matches against targets in auto-routed scans.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module was made with https://developer.tenable.com/reference/io-scanner-groups-list-routes docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: List scan routes within a scanner group
  list_scan_routes:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 124
  register: scan_routes_response

- name: List scan routes within a scanner group with envirment creds
  list_scan_routes:
    group_id: 124
  register: scan_routes_response
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: os success
  contains:
    routes:
      description: List of scan routes.
      type: list
      elements: dict
      contains:
        route:
          description: The route (hostname, IP address, CIDR, etc.)
          type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "group_id")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanner-groups/{module.params['group_id']}/routes"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
