# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_report_status
short_description: Returns the status of the specified report export request.
version_added: "0.0.1"
description:
  - Returns the status of the specified report export request.
  - The module is made from  https://developer.tenable.com/reference/vm-reports-status docs.
  - Requires BASIC [16]  user permissions as specified in the Tenable.io API documentation.
options:
  report_uuid:
    description:
      - The UUID of the report to check the status for..
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Get report status
  get_report_status:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    report_uuid: "123456"

- name: Get report status using enviroment keys
  get_report_status:
    report_uuid: "987"
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
      returned: on success
      contains:
        status:
          description: The status of the report
          type: str
          sample: "COMPLETED"
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
    common_spec = get_spec("access_key", "secret_key")
    special_args = {
        "report_uuid": {"required": True, "type": "str"},
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"reports/export/{module.params['report_uuid']}/status"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
