# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_scan_history
short_description: Returns a list of objects.
version_added: "0.0.1"
description:
  - This module returns a list of objects, each of which represent an individual run of the specified scan.
  - You can only resume a scan that has a status of paused.
  - The module is made from https://developer.tenable.com/reference/scans-history
  - Requires SCAN OPERATOR [24] and CAN VIEW  [16] user permissions as specified in the Tenable.io API documentation.
options:
  exclude_rollover:
    description:
      - Indicates whether or not to exclude rollover scans from the scan history.
      - If no value is provided for this parameter, Tenable Vulnerability Management uses the default value false
    required: false
    type: bool
    default: False
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
  - valkiriaaquatica.tenable.generics

"""

EXAMPLES = r"""
- name: Get scan history using enviroment creds
  get_scan_history:
    scan_id: "123456"

- name: Get scan history  using limit and exclude_rollover
  get_scan_history:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
    limit: 1
    exclude_rollover: true
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
        history:
          description: List of scan history objects.
          type: list
          returned: always
          contains:
            id:
              description: Unique identifier for the scan history.
              type: int
              sample: 25655263
            is_archived:
              description: Indicates if the scan history is archived.
              type: bool
              sample: false
            reindexing:
              description: Reindexing information.
              type: dict
              sample: null
            reporting_mode:
              description: Reporting mode of the scan.
              type: str
              sample: "baseline"
            scan_uuid:
              description: UUID of the scan.
              type: str
              sample: "122323"
            status:
              description: Status of the scan.
              type: str
              sample: "aborted"
            targets:
              description: Target information of the scan.
              type: dict
              contains:
                custom:
                  description: Indicates if custom targets were used.
                  type: bool
                  sample: false
                default:
                  description: Default target information.
                  type: dict
                  sample: null
            time_end:
              description: End time of the scan.
              type: int
              sample: 1715800542
            time_start:
              description: Start time of the scan.
              type: int
              sample: 1715800525
            visibility:
              description: Visibility of the scan.
              type: str
              sample: "public"
        pagination:
          description: Pagination information for the scan history.
          type: dict
          contains:
            sort:
              description: Sorting information.
              type: list
              contains:
                name:
                  description: Name of the field used for sorting.
                  type: str
                  sample: "start_date"
                order:
                  description: Order of sorting.
                  type: str
                  sample: "DESC"
            total:
              description: Total number of scan history objects.
              type: int
              sample: 2
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
    common_spec = get_spec("access_key", "secret_key", "scan_id", "limit", "offset", "sort")
    # exclude_rollover  exclusive for this module
    special_args = {
        "exclude_rollover": {
            "required": False,
            "type": "bool",
            "default": False,
        },
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scans/{module.params['scan_id']}/history?exclude_rollover={module.params['exclude_rollover']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
