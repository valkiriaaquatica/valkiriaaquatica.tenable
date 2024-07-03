# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: force_stop_scan
short_description: Force stops a scan.
version_added: "0.0.1"
description:
  - This module force stops a scan.
  - A force stop cancels all the scan's incomplete scan tasks and updates the scan status to aborted
  - Tenable Vulnerability Management processes and indexes the completed scan tasks
  - After you force stop a scan, Tenable recommends re-running the scan in its entirety to ensure total scan coverage.
  - You can use the force stop endpoint to abort a stalled scan in the stopping or publishing status.
  - This can be helpful when you need to abort a scan before a freeze window or before a subsequent scheduled scan begins.
  - You can only force stop a scan that has a status of stopping or publishing
  - The module is made from https://developer.tenable.com/reference/vm-scans-stop-force docs.
  - Requires SCAN OPERATOR [24] and CAN EXECUTE [32] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Create folder using enviroment creds
  force_stop_scan:
    scan_id: "123456"

- name: Create folder passing creds as vars
  force_stop_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
"""


RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable API.
  type: dict
  returned: on success
  contains:
    data:
      description: Specific data content of the API response that was deleted.
      type: dict
      returned: always
      sample: {
        "uuid": "template-123456"
      }
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
    endpoint = f"scans/{module.params['scan_id']}/force-stop"

    run_module(module, endpoint, method="POST")


if __name__ == "__main__":
    main()
