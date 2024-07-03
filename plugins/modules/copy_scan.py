# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: copy_scan
short_description: Copies the specified scan.
version_added: "0.0.1"
description:
  - This module copies the specified scan.
  - Module made from https://developer.tenable.com/reference/scans-copy docs.
  - Requires SCAN OPERATOR [24] user permissions and CAN EDIT [64] scan permissions
options:
  name:
    description:
      - The name of the object.
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
  - valkiriaaquatica.tenable.folder
"""

EXAMPLES = r"""
- name: Copy scan using enviroment creds
  copy_scan:
    scan_id: "12345"
    folder_id: "67890"
    name: "new scan"

- name: Copy scan
  copy_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "12345"
    folder_id: "67890"
    name: "new scan"
"""

RETURN = r"""
api_response:
  description: The full API response from Tenable.
  returned: success
  type: dict
  contains:
    data:
      description: The actual data returned from the API.
      type: dict
      contains:
        control:
          description: Indicates control status.
          type: bool
          sample: true
        creation_date:
          description: Creation date of the object.
          type: str
          sample: null
        enabled:
          description: Indicates if the object is enabled.
          type: int
          sample: 1
        id:
          description: ID of the object.
          type: int
          sample: 2282
        last_modification_date:
          description: Last modification date of the object.
          type: str
          sample: null
        name:
          description: Name of the object.
          type: str
          sample: "copy_sca_update_anisble"
        owner:
          description: Owner of the object.
          type: str
          sample: null
        read:
          description: Indicates if the object is read.
          type: bool
          sample: false
        rrules:
          description: Recurrence rules.
          type: str
          sample: "FREQ=WEEKLY;INTERVAL=4;BYDAY=SU"
        shared:
          description: Indicates if the object is shared.
          type: bool
          sample: false
        starttime:
          description: Start time of the object.
          type: str
          sample: "20240405T100000"
        status:
          description: Status of the object.
          type: str
          sample: "empty"
        timezone:
          description: Timezone of the object.
          type: str
          sample: "Europe/Madrid"
        user_permissions:
          description: User permissions for the object.
          type: str
          sample: null
        uuid:
          description: UUID of the object.
          type: str
          sample: "1111122269a"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_repeated_special_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id", "folder_id")
    special_spec = get_repeated_special_spec("name")
    argument_spec = {**common_spec, **special_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/copy"
    payload_keys = ["folder_id", "name"]
    payload = build_payload(module, payload_keys)
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
