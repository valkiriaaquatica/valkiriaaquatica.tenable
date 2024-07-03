# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_scanner_details
short_description: Returns the scanner list.
version_added: "0.0.1"
description:
  - This module returns the scanner list.
  - The module is made from  https://developer.tenable.com/reference/scanners-list  docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
"""

EXAMPLES = r"""
- name: Get scanner details
  get_scanner_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scanner_id: 11111

- name: Get scanner details using enviroment keys
  get_scanner_details:
    scanner_id: 11111
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on sucess
  contains:
    data:
      description: Contains detailed information about an asset or group, including its status, ownership, and connection details.
      type: dict
      returned: always
      sample:
        creation_date: 123456
        group: true
        id: 123456
        key: "123456"
        last_connect: null
        last_modification_date: 123456
        license: null
        linked: 1
        name: "name"
        network_name: "name"
        num_scans: 0
        owner: "system"
        owner_id: 123456
        owner_name: "system"
        owner_uuid: "123456"
        pool: true
        scan_count: 0
        source: "service"
        status: "on"
        supports_remote_logs: false
        supports_remote_settings: false
        timestamp: 123456
        type: "local"
        user_permissions: 64
        uuid: "123456"
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
    argument_spec = get_spec("access_key", "secret_key", "scanner_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scanners/{module.params['scanner_id']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
