# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: enable_schedule
short_description: Enables or disables a scan schedule.
version_added: "0.0.1"
description:
  - This module enables or disables a scan schedule.
  - The module is made from https://developer.tenable.com/reference/scans-schedule  docs.
  - Requires SCAN OPERATOR [24] and CAN EXECUTE [32] user permissions as specified in the Tenable.io API documentation.
options:
  enabled:
    description:
      - Enables or disables the scan schedule.
    required: true
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Enable the scan schedule using enviroment creds
  enable_schedule:
    scan_id: "123456"
    enabled: true

- name: Disable the scan schedule
  enable_schedule:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "{{ scan_id_creation }}"
    enabled: false
"""


RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable API.
  type: dict
  returned: always when a request is made, independent if it is correct or incorrect.
  contains:
    data:
      description: Specific data content of the API response, including detailed settings and configurations of the scan.
      type: dict
      returned: always
      sample:
        agent_scan_launch_type: "scheduled"
        control: true
        enabled: true
        rrules: "FREQ=WEEKLY"
        schedule_uuid: "123456"
        starttime: "12346"
        tag_type: "main"
        timezone: "Europe/Madrid"
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
    specific_spec = {"enabled": {"required": True, "type": "bool"}}
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/schedule"

    payload_keys = ["enabled"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
