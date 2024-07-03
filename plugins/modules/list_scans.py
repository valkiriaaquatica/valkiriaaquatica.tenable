# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scans
short_description: Returns a list of scans.
version_added: "0.0.1"
description:
  - This module returns a list of scans.
  - Module made from https://developer.tenable.com/reference/scans-list  docs.
  - Requires BASIC  [16] user permissions as specified in the Tenable.io API documentation.
  - Keep in mind potential rate limits when using this endpoint.
  - To check the status of your scans, use the GET /scans/{scan_id}/latest-status endpoint.
  - Tenable recommends the GET /scans/{scan_id}/latest-status endpoint especially if you are programmatically checking the status of large numbers of scans.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.last_modification_date
  - valkiriaaquatica.tenable.folder
"""


EXAMPLES = r"""
- name: List all scans using enviroment creds
  list_scans:
  register: all_scans

- name: List scan from folder and using enviroment creds
  list_scans:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    folder_id: 123456
"""

RETURN = r"""
api_response:
  description: Detailed information returned by the API.
  type: dict
  returned: always
  contains:
    data:
      description: Contains detailed information about the response's data.
      type: dict
      contains:
        scanners:
          description: A list of scanners details retrieved from the API.
          type: list
          elements: dict
          contains:
            creation_date:
              description: The timestamp when the scanner was created.
              type: int
              returned: always
              sample: 123456
            distro:
              description: Operating system distribution of the scanner.
              type: str
              returned: always
              sample: "win-x86-64"
            engine_version:
              description: Version of the scanning engine.
              type: str
              returned: always
              sample: "1.1.1"
            group:
              description: Indicates whether the scanner is part of a group.
              type: bool
              returned: always
              sample: false
            hostname:
              description: The hostname of the scanner.
              type: str
              returned: always
              sample: "name"
            id:
              description: Unique identifier for the scanner.
              type: int
              returned: always
              sample: 317891
            ip_addresses:
              description: List of IP addresses associated with the scanner.
              type: list
              elements: str
              returned: always
              sample: ["10.200.16.23"]
            key:
              description: Unique key or identifier for the scanner.
              type: str
              returned: always
              sample: "123456"
            last_connect:
              description: The last timestamp when the scanner connected to the network.
              type: int
              returned: always
              sample: 123456
            last_modification_date:
              description: The timestamp when the scanner was last modified.
              type: int
              returned: always
              sample: 123456
            linked:
              description: Indicates if the scanner is linked with the central system.
              type: int
              returned: always
              sample: 1
            loaded_plugin_set:
              description: Identifier for the set of plugins loaded on the scanner.
              type: str
              returned: always
              sample: "123456"
            name:
              description: The name of the scanner.
              type: str
              returned: always
              sample: "name"
            network_name:
              description: The network name associated with the scanner.
              type: str
              returned: always
              sample: "Default"
            num_scans:
              description: The number of scans conducted by the scanner.
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
              sample: "123456"
            platform:
              description: The platform on which the scanner operates, e.g., WINDOWS.
              type: str
              returned: always
              sample: "WINDOWS"
            pool:
              description: Indicates if the scanner is part of a pool.
              type: bool
              returned: always
              sample: false
            remote_uuid:
              description: Remote UUID associated with the scanner.
              type: str
              returned: always
              sample: "123456"
            scan_count:
              description: The count of scans performed by the scanner.
              type: int
              returned: always
              sample: 0
            shared:
              description: Indicates if the scanner is shared among multiple users.
              type: int
              returned: always
              sample: 1
            source:
              description: The source from which the scanner was provisioned.
              type: str
              returned: always
              sample: "service"
            status:
              description: The current status of the scanner, e.g., on or off.
              type: str
              returned: always
              sample: "on"
            supports_remote_logs:
              description: Indicates whether the scanner supports remote logs.
              type: bool
              returned: always
              sample: true
            supports_remote_settings:
              description: Indicates whether the scanner supports remote settings.
              type: bool
              returned: always
              sample: true
            supports_webapp:
              description: Indicates whether the scanner supports web application scanning.
              type: bool
              returned: always
              sample: false
            timestamp:
              description: Timestamp indicating the last significant update or event for the scanner.
              type: int
              returned: always
              sample: 1714253297
            type:
              description: The type of scanner, e.g., managed or independent.
              type: str
              returned: always
              sample: "managed"
            ui_build:
              description: The build number of the user interface on the scanner.
              type: str
              returned: always
              sample: "29"
            ui_version:
              description: The version number of the user interface on the scanner.
              type: str
              returned: always
              sample: "10.7.2"
            user_permissions:
              description: Numeric value representing the permissions of the user regarding this scanner.
              type: int
              returned: always
              sample: 123456
            uuid:
              description: The UUID of the scanner.
              type: str
              returned: always
              sample: "123456"
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "folder_id", "last_modification_date")
    special_args = {
        "folder_id": {"required": False, "type": "int"},
        "last_modification_date": {"required": False, "type": "int"},
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = "scans"

    def query_params():
        return build_query_parameters(
            folder_id=module.params["folder_id"],
            last_modification_date=module.params["last_modification_date"],
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
