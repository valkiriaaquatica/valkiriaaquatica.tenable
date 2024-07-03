# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scanners
short_description: Returns the scanner list.
version_added: "0.0.1"
description:
  - This module returns the scanner list.
  - Requires SCAN MANAGER [40] user permissions [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/scanners-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all scanners
  list_scanners:
    access_key: "your_access_key"
    secret_key: "your_secret_key"

- name: List all scanners using envirometn credentials
  list_scanners:
  register: all_timezones
"""

RETURN = r"""
api_response:
  description: Detailed information returned by the Tenable API concerning scanners.
  type: dict
  returned: always
  contains:
    data:
      description: Contains all relevant details about the scanners.
      type: dict
      contains:
        scanners:
          description: A list of scanner configurations.
          type: list
          elements: dict
          contains:
            creation_date:
              description: UNIX timestamp when the scanner was created.
              type: int
              returned: always
              sample: 123456
            distro:
              description: Operating system distribution of the scanner.
              type: str
              returned: always
              sample: "win-x86-64"
            engine_version:
              description: Version of the scanning engine used.
              type: str
              returned: always
              sample: "1.1.1"
            group:
              description: Indicates whether the scanner is grouped with others.
              type: bool
              returned: always
              sample: false
            hostname:
              description: Hostname of the scanner.
              type: str
              returned: always
              sample: "name"
            id:
              description: Unique identifier of the scanner.
              type: int
              returned: always
              sample: 317891
            ip_addresses:
              description: List of IP addresses assigned to the scanner.
              type: list
              elements: str
              returned: always
              sample: ["10.200.16.23"]
            key:
              description: Key associated with the scanner for API or remote access.
              type: str
              returned: always
              sample: "123456"
            last_connect:
              description: UNIX timestamp of the last connection made by the scanner.
              type: int
              returned: always
              sample: 123456
            last_modification_date:
              description: UNIX timestamp when the scanner configuration was last modified.
              type: int
              returned: always
              sample: 123456
            linked:
              description: Indicates if the scanner is linked to a central manager or cloud.
              type: int
              returned: always
              sample: 1
            loaded_plugin_set:
              description: Identifier of the plugin set loaded on the scanner.
              type: str
              returned: always
              sample: "123456"
            name:
              description: Name of the scanner.
              type: str
              returned: always
              sample: "name"
            network_name:
              description: Network name or identifier associated with the scanner.
              type: str
              returned: always
              sample: "Default"
            num_scans:
              description: Number of scans performed by the scanner.
              type: int
              returned: always
              sample: 0
            owner:
              description: Username or identifier of the owner of the scanner.
              type: str
              returned: always
              sample: "system"
            owner_id:
              description: Numeric identifier of the owner.
              type: int
              returned: always
              sample: 2297093
            owner_name:
              description: Name of the owner.
              type: str
              returned: always
              sample: "system"
            owner_uuid:
              description: UUID of the owner.
              type: str
              returned: always
              sample: "123456"
            platform:
              description: Platform of the scanner, such as WINDOWS or LINUX.
              type: str
              returned: always
              sample: "WINDOWS"
            pool:
              description: Indicates if the scanner is part of a scanner pool.
              type: bool
              returned: always
              sample: false
            remote_uuid:
              description: Remote UUID for the scanner.
              type: str
              returned: always
              sample: "123456"
            scan_count:
              description: Total number of scans initiated by this scanner.
              type: int
              returned: always
              sample: 0
            shared:
              description: Indicates if the scanner is shared with other users.
              type: int
              returned: always
              sample: 1
            source:
              description: Source of the scanner configuration, typically 'service' or 'manual'.
              type: str
              returned: always
              sample: "service"
            status:
              description: Current status of the scanner, such as 'on' or 'off'.
              type: str
              returned: always
              sample: "on"
            supports_remote_logs:
              description: Indicates if the scanner supports remote logging.
              type: bool
              returned: always
              sample: true
            supports_remote_settings:
              description: Indicates if the scanner can be configured remotely.
              type: bool
              returned: always
              sample: true
            supports_webapp:
              description: Indicates if the scanner supports web application scanning.
              type: bool
              returned: always
              sample: false
            timestamp:
              description: UNIX timestamp of the last update to the scanner's status or configuration.
              type: int
              returned: always
              sample: 1714253297
            type:
              description: Type of the scanner, such as 'managed' or 'standalone'.
              type: str
              returned: always
              sample: "managed"
            ui_build:
              description: Build number of the scanner's user interface.
              type: str
              returned: always
              sample: "29"
            ui_version:
              description: Version number of the scanner's user interface.
              type: str
              returned: always
              sample: "10.7.2"
            user_permissions:
              description: Permissions level of the user regarding this scanner.
              type: int
              returned: always
              sample: 123456
            uuid:
              description: Universal Unique Identifier of the scanner.
              type: str
              returned: always
              sample: "123456"
    status_code:
      description: HTTP status code returned by the API, indicating the result of the request.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = "scanners"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
