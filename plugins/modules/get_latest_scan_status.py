# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_latest_scan_status
short_description: Returns the latest status for a scan
version_added: "0.0.1"
description:
  - This module returns the latest status for a scan
  - For a list of possible status values, see https://developer.tenable.com/docs/scan-status-tio
  - The module is made from https://developer.tenable.com/reference/scans-get-latest-status docs.
  - Requires SCAN OPERATOR [24] and CAN VIEW [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Get latest scan status
  get_latest_scan_status:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scan_id: "123456789"

- name: Get latest scan status using enviroment creds
  get_latest_scan_status:
    scan_id: "123456789"
"""


RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains information about the progress and status of the requested operation.
      type: dict
      returned: always
      sample:
        progress: 0
        status: "paused"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "scan_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scans/{module.params['scan_id']}/latest-status"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
