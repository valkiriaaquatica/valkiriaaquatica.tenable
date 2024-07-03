# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: launch_scan
short_description: Launches a scan.
version_added: "0.0.1"
description:
  - This module launches a scan.
  - For more information of scans  https://developer.tenable.com/docs/launch-scan-tio
  - The module is made from https://developer.tenable.com/reference/scans-launch docs.
  - There is a limit of 25 active scans per container.
  - You can use use the get_scan_count endpoint to retrieve the total number of active scans in your container
  - Requires SCAN OPERATOR [24] and  CAN EXECUTE [32] user permissions as specified in the Tenable.io API documentation.
options:
  alt_targets:
    description:
      - If you include this parameter, Tenable Vulnerability Management scans these targets instead of the default.
      - Value can be an array where each index is a target, or an array with a single index of comma-separated targets.
    required: false
    type: list
    elements: str
  rollover:
    description:
      - Indicates whether or not to launch a rollover scan instead of full scan.
      - A rollover scan only runs against the targets that Tenable Vulnerability Management did not scan due to a previous scan timeout.
    required: false
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Launch scan using enviroment creds
  launch_scan:
    scan_id: "123456"
    alt_targets:
      - "1.11.11.111"
      - "2.22.22.2"
      - "3.33.3.3"

- name: Launch scan using enviroment creds
  launch_scan:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scan_id: "123456"
    alt_targets: "192.168.1.150,192.168.1.120"
    rollover: true
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: always when a request is made, independent if it is correct or incorrect.
  contains:
    data:
      description: Contains the scan UUID, a unique identifier for the scan operation performed.
      type: dict
      returned: always
      sample:
        scan_uuid: "123456789"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id")
    specific_spec = {
        "alt_targets": {"required": False, "type": "list", "elements": "str"},
        "rollover": {"required": False, "type": "bool"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/launch"

    payload_keys = ["alt_targets", "rollover"]
    payload = build_payload(module, payload_keys)
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
