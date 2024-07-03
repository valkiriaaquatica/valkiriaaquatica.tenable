# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_assignable_scanners
short_description: Lists all scanners and scanner groups not yet assigned to a custom network object.
version_added: "0.0.1"
description:
  - This module lists all scanners and scanner groups not yet assigned to a custom network object.
  - The module is made from https://developer.tenable.com/reference/networks-list-assignable-scannersdocs.
  - Requires ADMINISTRATOR   [64] user permissions as specified in the Tenable.io API documentation.
options:
  network_id:
    description:
      - The UUID of the default network object.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List assignable scanners from a network using enviroment creds
  list_assignable_scanners:
    network_id: "012345"

- name: List assignable scanners from a network using enviroment creds
  list_assignable_scanners:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    network_id: "012345"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response.
  returned: always
  type: dict
  contains:
    data:
      description: Contains the actual data of the response.
      type: dict
      contains:
        scanners:
          description: A list of scanner details retrieved from the API.
          type: list
          elements: dict
          contains:
            creation_date:
              description: The timestamp when the scanner was created.
              type: int
              returned: always
              sample: 12345
            group:
              description: Indicates whether the scanner is part of a group.
              type: bool
              returned: always
              sample: true
            id:
              description: Unique identifier for the scanner.
              type: int
              returned: always
              sample: 12345
            key:
              description: The key associated with the scanner.
              type: str
              returned: always
              sample: "12345"
            last_connect:
              description: The last connection timestamp of the scanner, null if never connected.
              type: int
              returned: when available
            last_modification_date:
              description: The timestamp when the scanner was last modified.
              type: int
              returned: always
              sample: 12345
            linked:
              description: Indicates whether the scanner is linked (1) or not (0).
              type: int
              returned: always
              sample: 1
            name:
              description: The name of the scanner.
              type: str
              returned: always
              sample: "EU Frankfurt Cloud Scanners"
            num_scans:
              description: The number of scans conducted by this scanner.
              type: int
              returned: always
              sample: 0
            owner:
              description: The system account that owns the scanner.
              type: str
              returned: always
              sample: "system"
            owner_id:
              description: The system-generated ID of the owner.
              type: int
              returned: always
              sample: 2297093
            owner_name:
              description: The name of the owner.
              type: str
              returned: always
              sample: "system"
            owner_uuid:
              description: The UUID of the owner.
              type: str
              returned: always
              sample: "12345"
            pool:
              description: Indicates if the scanner is part of a pool.
              type: bool
              returned: always
              sample: true
            scan_count:
              description: The count of scans assigned to this scanner.
              type: int
              returned: always
              sample: 0
            source:
              description: The source of the scanner, e.g., 'service'.
              type: str
              returned: always
              sample: "service"
            status:
              description: The operational status of the scanner.
              type: str
              returned: always
              sample: "on"
            supports_remote_logs:
              description: Indicates if the scanner supports remote logs.
              type: bool
              returned: always
              sample: false
            supports_remote_settings:
              description: Indicates if the scanner supports remote settings adjustments.
              type: bool
              returned: always
              sample: false
            timestamp:
              description: The timestamp of the last significant update to the scanner's settings.
              type: int
              returned: always
              sample: 12345
            type:
              description: The type of scanner, e.g., 'local'.
              type: str
              returned: always
              sample: "local"
            uuid:
              description: The UUID of the scanner.
              type: str
              returned: always
              sample: "12345"
    status_code:
      description: HTTP status code returned by the Tenable.io API.
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
        "network_id": {"required": True, "type": "str"},  # it exsits in arguments but is not required and here it is
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"networks/{module.params['network_id']}/assignable-scanners"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
