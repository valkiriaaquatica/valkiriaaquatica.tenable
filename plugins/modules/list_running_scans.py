# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_running_scans
short_description: Lists scans running on the requested scanner.
version_added: "0.0.1"
description:
  - This module lists scans running on the requested scanner.
  - The module is made from https://developer.tenable.com/reference/scanners-get-scans  docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
"""

EXAMPLES = r"""
- name: List running scans on scanner
  list_running_scans:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scanner_id: 11111

- name: List running scans on scanner on enviroment keys
  list_running_scans:
    scanner_id: 11111
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    scans:
      description: List of scans.
      type: list
      elements: dict
      contains:
        scan_id:
          description: The ID of the scan.
          type: int
          sample: 36
        scanner_uuid:
          description: The UUID of the scanner.
          type: str
          sample: "00000000-0000-0000-0000-00000000000000000000000000001"
        name:
          description: The name of the scan.
          type: str
          sample: "Basic Scan"
        status:
          description: The status of the scan.
          type: str
          sample: "pending"
        id:
          description: The unique identifier of the scan.
          type: str
          sample: "007d0e76-fcec-455d-a5e2-fac16772560c"
        user:
          description: The user who initiated the scan.
          type: str
          sample: "API Demo User"
        user_uuid:
          description: The UUID of the user who initiated the scan.
          type: str
          sample: "1fb43a88-2240-4d7e-a46a-dd655fa59398"
        last_modification_date:
          description: The last modification date of the scan.
          type: int
          sample: 1545945321
        start_time:
          description: The start time of the scan.
          type: int
          sample: 1545945321
        network_id:
          description: The network ID associated with the scan.
          type: str
          sample: "6be6cbfe-2c4b-4f3c-b959-127362d2dcce"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "scanner_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scanners/{module.params['scanner_id']}/scans"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
