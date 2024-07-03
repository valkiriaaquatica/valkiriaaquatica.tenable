# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_scan_status
short_description: Changes the status of a scan.
version_added: "0.0.1"
description:
  - This module changes the status of a scan.
  - For a list of possible status values, see https://developer.tenable.com/docs/scan-status-tio .
  - To update a category you must be an admin or have edit permissions on all tags within the category.
  - The module is made from https://developer.tenable.com/reference/scans-read-status.
  - RequiresSCAN OPERATOR [24] and CAN VIEW [16] user permissions as specified in the Tenable.io API documentation.
options:
  read:
    description:
      - If true, the scan has been read.
    required: true
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Update scan status to scan read
  update_scan_status:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
    read: true

- name: Update scan status to scan not read using enviroment creds
  update_scan_status:
    scan_id: "123456"
    read: false
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id")
    special_args = {
        "read": {
            "required": True,
            "type": "bool",
        },
    }
    argument_spec = {**common_spec, **special_args}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = ["read"]
    payload = build_payload(module, payload_keys)

    endpoint = f"scans/{module.params['scan_id']}/status"

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
