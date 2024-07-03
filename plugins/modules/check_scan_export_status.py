# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: check_scan_export_status
short_description: Check the file status of an exported scan.
version_added: "0.0.1"
description:
  - This module check the file status of an exported scan.
  - When an export has been requested, it is necessary to poll this endpoint until a "ready" status
    is returned, at which point the file is complete and can be downloaded using the export download endpoint
  - Requires SCAN OPERATOR [24] user permissions and CAN VIEW [16] scan permissions user permissions as specified in the Tenable.io API documentation.
  - The module is made from https://developer.tenable.com/reference/scans-export-status docs.
options:
  file_id:
    description:
      - The ID of the file to poll (included in response from /scans/{scan_id}/export).
    type: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Check scan export statu using enviroment creds
  check_scan_export_status:
    scan_id: "1234"
    file_id: "24332r34-csv"

- name: Check scan export status using enviroment creds
  check_scan_export_status:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "1234"
    file_id: "24332r34-csv"
"""

RETURN = r"""
api_response:
  description: The full API response from Tenable.
  returned: success
  type: dict
  contains:
    data:
      description: The actual data returned from the API.
      type: dict
      contains:
        status:
          description: The status of the export job.
          type: str
    status_code:
      description: The HTTP status code returned by the API.
      type: int
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id")
    specific_spec = {"file_id": {"required": True, "type": "str"}}
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scans/{module.params['scan_id']}/export/{module.params['file_id']}/status"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
