# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: delete_scan_history
short_description: Deletes historical results from a scan.
version_added: "0.0.1"
description:
  - This module deletes historical results from a scan. Note that rollover scan data is also deleted.
  - Scan details include information about when and where the scan ran, as well as the scan results for the target hosts.
  - The module is made from https://developer.tenable.com/reference/scans-history-details
  - Requires SCAN OPERATOR [24] and CAN VIEW [16] user permissions as specified in the Tenable.io API documentation.
options:
  history_id:
    description:
      - The UUID of the historical scan result to return details about.
      - This identifier corresponds to the history.id attribute of the response message from get_scan_history module or
        the GET /scans/{scan_id}/history endpoint.
    required: true
    type: str
  scan_id:
    description:
      - The UUID of the scan whose historical results you want to delete.
    required: true
    type: str
  exclude_rollover:
    description:
      - Indicates whether or not to delete scan rollover history.
      - If true, the scan history and its associated rollover scan data are deleted.
      - If false or null and the scan has rollover data, you receive a 409 error
        "This scan contains rollover scan data. If you want to delete it and all the associated rollover scan data,
        use query parameter delete_rollovers=true."
    required: false
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Delete scan history details using enviroment creds
  delete_scan_history:
    scan_id: "123456"
    history_uuid: "23545"

- name: Get scan history  details using limit and exclude_rollover
  delete_scan_history:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
    history_uuid: "23545"
"""


RETURN = r"""
api_response:
  description: Response returned by the Tenable api.
  returned: always when a request is made, independent if it correct or incorrect.
  type: complex
  contains:
    status_code:
      description: The HTTP status code returned by the API if an error occurred.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id")
    special_args = {
        "history_id": {
            "required": True,  # different from arguments.py
            "type": "str",
        },
        "exclude_rollover": {
            "required": False,
            "type": "bool",
        },
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if module.params["exclude_rollover"]:
        endpoint = f"scans/{module.params['scan_id']}/history/{module.params['history_id']}?delete_rollovers={module.params['exclude_rollover']}"
    else:
        endpoint = f"scans/{module.params['scan_id']}/history/{module.params['history_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
