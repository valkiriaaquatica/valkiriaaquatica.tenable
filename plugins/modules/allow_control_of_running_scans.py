# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

# in docs is the id of the scan is set to scan_uuid (idk why) it changes from other agent docs where is scan_id
# to maintain the consistency the scan_uuid of docs is set to scan_id

DOCUMENTATION = r"""
---
module: allow_control_of_running_scans
short_description: Allows control of scans that are currently running on a scanner.
version_added: "0.0.1"
description:
  - This module allows control of scans that are currently running on a scanner.
  - Note You cannot use this endpoint to update the credential type.
  - Requires SCAN MANAGER [40] credential permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/scanners-control-scans docs.
options:
  action:
    description:
      - An action to perform on a scan. Valid values are stop, pause, and resume.
    type: str
    required: true
    choices: ["stop", "pause", "resume"]
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Resumes scans in a specified scanner
  allow_control_of_running_scans:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scanner_id: 123456
    scan_id: 987
    action: "resume"

- name: Stops scans in a specified scanner using environment creds
  allow_control_of_running_scans:
    scanner_id: 123456
    scan_id: 987
    action: "stop"
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scanner_id", "scan_id")
    specific_spec = {"action": {"required": True, "type": "str", "choices": ["stop", "pause", "resume"]}}
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/{module.params['scanner_id']}/scans/{module.params['scan_id']}"

    payload_keys = ["action"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
