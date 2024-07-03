# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_scan_details
short_description: Returns scan results for a specific scan
version_added: "0.0.1"
description:
  - This module returns scan results for a specific scan
  - If you submit a request without query parameters, Tenable Vulnerability Management returns results from the latest run of the specified scan
  - The module is made from  https://developer.tenable.com/reference/scans-details docs.
  - Requires SCAN MANAGER [24]  and CAN VIEW [16] user permissions as specified in the Tenable.io API documentation.
options:
  history_id:
    description:
      - The unique identifier of the historical data.
      - Use https://developer.tenable.com/reference/scans-history to get the id or use the get_scan_history module.
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Get scan details
  get_scan_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scanner_id: 11111

- name: Get scan details using enviroment keys
  get_scan_details:
    scanner_id: 11111
    history_id: "12345"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "scan_id", "history_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scans/{module.params['scan_id']}"

    def query_params():
        return build_query_parameters(
            history_id=module.params["history_id"],
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
