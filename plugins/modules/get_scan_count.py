# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_scan_count
short_description: Returns scan results for a specific scan
version_added: "0.0.1"
description:
  - Returns the total number of scans in your container.
  - You can use the active query parameter to return only the number of active scans.
  - The module is made from  https://developer.tenable.com/reference/io-scans-count  docs.
  - Requires BASIC [16] and CAN VIEW [16] user permissions as specified in the Tenable.io API documentation.
options:
  active:
    description:
      - The unique identifier of the historical data
      - If true, only active scans are counted.
      - If false, all active and inactive scans are counted.
      - If this parameter is omitted, Tenable Vulnerability Management defaults to false.
    required: false
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Get scan count
  get_scan_count:
    access_key: "your_access_key"
    secret_key: "your_secret_key"

- name: Get scan count of active scans using enviroment keys
  get_scan_count:
    active: true
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    special_args = {
        "active": {"required": False, "type": "bool", "default": None},
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if module.params["active"] is not None:
        endpoint = f"scans/count?active={module.params['active']}"
    else:
        endpoint = "scans/count"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
