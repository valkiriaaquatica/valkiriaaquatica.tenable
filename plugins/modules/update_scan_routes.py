# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_scan_routes
short_description: Updates the scan routes for a specified scanner group.
version_added: "0.0.1"
description:
  - This module updates the hostnames, hostname wildcards, IP addresses, and IP address ranges that
    Tenable Vulnerability Management matches against targets in auto-routed scans.
  -  For more information about supported route formats,
   see https://developer.tenable.com/docs/manage-scan-routing-tio#section-supported-scan-routing-target-formats
  - Requires SCAN MANAGER [40] user permissions and CAN EDIT [64] scan permissions as specified
    in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/io-scanner-groups-update-routes docs.
options:
  routes:
    description:
      - A list of zero or more hostnames, hostname wildcards, IP addresses, CIDR addresses, or IP ranges.
      - For more information about supported route formats,
        see  https://developer.tenable.com/docs/manage-scan-routing-tio#section-supported-scan-routing-target-formats
    type: list
    elements: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: Update scan routes for a scanner group
  update_scan_routes:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 12345
    routes:
      - "example.com"
      - "192.0.2.0/24"
      - "host.domain.com"

- name: Update scan routes using environment credentials
  update_scan_routes:
    group_id: 12345
    routes:
      - "example.com"
      - "192.0.2.0/24"
      - "host.domain.com"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "group_id")
    specific_spec = {"routes": {"required": True, "type": "list", "elements": "str"}}
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanner-groups/{module.params['group_id']}/routes"
    payload_keys = ["routes"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
