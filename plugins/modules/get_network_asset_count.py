# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_network_asset_count
short_description: Returns the assets in a network not seen in certain days.
version_added: "0.0.1"
description:
  - This module Returns the total number of assets in the network along with the number of assets that have not been seen for the specified number of days.
  - The module is made from https://developer.tenable.com/reference/io-networks-asset-count-details docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  num_days:
    description:
      - The number of days to get the assets.
    required: true
    type: int
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.network
"""

EXAMPLES = r"""
- name: Get network asset count using enviromend creds
  get_network_asset_count:
    network_id: "123456"
    num_days: 100

- name: Get network asset count using enviromend creds
  get_network_asset_count:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    network_id: "123456"
    num_days: 100
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "network_id")
    common_spec["network_id"]["required"] = True
    special_args = {"num_days": {"required": True, "type": "int"}}
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"networks/{module.params['network_id']}/counts/assets-not-seen-in/{module.params['num_days']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
