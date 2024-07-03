# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_scan_history_details
short_description: Returns the details of a previous run of the specified scan.
version_added: "0.0.1"
description:
  - This module returns the details of a previous run of the specified scan.
  -  Scan details include information about when and where the scan ran, as well as the scan results for the target hosts.
  - The module is made from https://developer.tenable.com/reference/scans-history-details
  - Requires SCAN OPERATOR [24] and CAN VIEW  [16] user permissions as specified in the Tenable.io API documentation.
options:
  history_uuid:
    description:
      - The UUID of the historical scan result to return details about.
      - This identifier corresponds to the history.scan_uuid attribute of the response message from get_scan_history moddule or
         the GET /scans/{scan_id}/history endpoint.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Get scan history details using enviroment creds
  get_scan_history_details:
    scan_id: "123456"
    history_uuid: "23545"

- name: Get scan history  details using limit and exclude_rollover
  get_scan_history_details:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
    history_uuid: "23545"
"""


RETURN = r"""
api_response:
  description: Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Data content of the response from the Tenable API.
      type: dict
      returned: always
      contains:
        is_archived:
          description: Indicates if the scan is archived.
          type: bool
          sample: true
        name:
          description: Name of the scan.
          type: str
          sample: "name"
        object_id:
          description: Unique identifier for the scan object.
          type: int
          sample: 24858000
        owner:
          description: Owner of the scan.
          type: str
          sample: ""
        owner_id:
          description: Unique identifier for the owner.
          type: int
          sample: 2308677
        owner_uuid:
          description: UUID of the owner.
          type: str
          sample: "6c9a7bf3-d5d5-4bb7-a756-02a388c309cf"
        reindexing:
          description: Reindexing information.
          type: dict
          sample: null
        reporting_mode:
          description: Reporting mode of the scan.
          type: str
          sample: null
        scan_end:
          description: End time of the scan.
          type: int
          sample: 1710511883
        scan_start:
          description: Start time of the scan.
          type: int
          sample: 1710506677
        scan_type:
          description: Type of the scan.
          type: str
          sample: "agent"
        schedule_uuid:
          description: UUID of the scan schedule.
          type: str
          sample: "1111"
        status:
          description: Status of the scan.
          type: str
          sample: "completed"
        targets:
          description: Targets of the scan.
          type: str
          sample: "127.0.0.1"
        uuid:
          description: UUID of the scan.
          type: str
          sample: "11111"
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
    common_spec = get_spec("access_key", "secret_key", "scan_id")
    special_args = {
        "history_uuid": {
            "required": True,
            "type": "str",
        },
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/history/{module.params['history_uuid']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
