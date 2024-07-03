# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_scan_progress
short_description: Returns the progress for the specified scan.
version_added: "0.0.1"
description:
  - This module returns the progress for the specified scan.
  - Note If you submit a request without query parameters, Tenable Vulnerability Management
    returns the progress from the latest run of the specified scan.
  - If you submit a request using the history_id or history_uuid query parameters to specify
    a historical run of the scan, Tenable Vulnerability Management returns the progress
    for the specified historical run.
  - The module is made from https://developer.tenable.com/reference/io-vm-scans-progress-get .
  - Requires SCAN OPERATOR [24] and CAN VIEW  [16] user permissions as specified in the Tenable.io API documentation.
options:
  history_uuid:
    description:
      - The UUID of the historical scan result to return details about.
      - This identifier corresponds to the history.scan_uuid attribute of the response message from get_scan_history moddule or
        the GET /scans/{scan_id}/history endpoint.
    required: false
    type: str
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
- name: Get scan progress using enviroment creds
  get_scan_progress:
    scan_id: "123456"

- name: Get scan progress using history_id
  get_scan_progress:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
    history_id: 123

- name: Get scan progress using history_uuid
  get_scan_progress:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
    history_uuid: "12345"
"""


RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id", "history_id")
    special_args = {
        "history_uuid": {
            "required": False,
            "type": "str",
        },
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/progress"
    query_params = []

    if module.params.get("history_id"):
        query_params.append(f"history_id={module.params['history_id']}")
    if module.params.get("history_uuid"):
        query_params.append(f"history_uuid={module.params['history_uuid']}")

    if query_params:
        endpoint += "?" + "&".join(query_params)
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
