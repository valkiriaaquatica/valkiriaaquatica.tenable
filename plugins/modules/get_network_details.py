# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_network_details
short_description: Retrieve detailed information of a network using its network_uuid.
version_added: "0.0.1"
description:
  - This module fetches detailed information about a specific network.
  - The module is made from https://developer.tenable.com/reference/networks-details docs.
  - Requires ADMINSITRATOR [64] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.network
"""

EXAMPLES = r"""
- name: Get information of a netowrk
  get_network_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    network_id: 11111

- name: Get information of a netowrk using enviroment keys
  get_network_details:
    network_id: 11111
"""

RETURN = r"""
api_response:
  description: Detailed information about the network.
  type: dict
  returned: always
  contains:
    data:
      description: Contains key information about the network including creation and modification details.
      type: dict
      returned: always
      sample:
        created: 1689849698540
        created_by: "fdfsd-c9e7-4e1d-sdfef-sfrfds"
        created_in_seconds: 1689849698
        is_default: false
        modified: 1689849698540
        modified_by: "SFREVFGF6"
        modified_in_seconds: 1689849698
        name: "network_name"
        owner_uuid: "CRFRE"
        scanner_count: 0
        uuid: "ssdfef-4f59-efgerg-b193-frtgtr"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_repeated_special_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    special_spec = get_repeated_special_spec("network_id")

    argument_spec = {**argument_spec, **special_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    run_module(module, "networks", module.params["network_id"], method="GET")


if __name__ == "__main__":
    main()
