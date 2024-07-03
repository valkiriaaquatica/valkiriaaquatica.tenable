# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_network
short_description: Created a network.
version_added: "0.0.1"
description:
  - This module creates a network object that you associate with scanners and scanner groups.
  - The module is made from https://developer.tenable.com/reference/networks-create docs.
  - Requires ADMINISTRATOR [64] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.network_params
"""

EXAMPLES = r"""
- name: Create a network using enviroment creds
  create_network:
    name: "name"
    description: "this is the descritpion"
    assets_ttl_days: 50

- name: Create a network using enviroment creds
  create_network:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    name: "name"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains all relevant details about the network or asset.
      type: dict
      contains:
        assets_ttl_days:
          description: The time-to-live (TTL) in days for assets within this network.
          type: int
          returned: always
          sample: 1
        created:
          description: UNIX timestamp when the network was created.
          type: int
          returned: always
          sample: 123456
        created_by:
          description: User identifier of who created the network.
          type: str
          returned: always
          sample: "123456"
        created_in_seconds:
          description: Creation time in seconds.
          type: int
          returned: always
          sample: 123456
        description:
          description: Description of the network.
          type: str
          returned: always
          sample: "this is the description"
        is_default:
          description: Indicates whether this network is the default network.
          type: bool
          returned: always
          sample: false
        modified:
          description: UNIX timestamp when the network was last modified.
          type: int
          returned: always
          sample: 123456
        modified_by:
          description: User identifier of who last modified the network.
          type: str
          returned: always
          sample: "123456"
        modified_in_seconds:
          description: Modification time in seconds.
          type: int
          returned: always
          sample: 123456
        name:
          description: Name of the network.
          type: str
          returned: always
          sample: "ansible_collection_test_network"
        owner_uuid:
          description: UUID of the owner of the network.
          type: str
          returned: always
          sample: "123456"
        scanner_count:
          description: Number of scanners associated with this network.
          type: int
          returned: always
          sample: 0
        uuid:
          description: UUID of the network.
          type: str
          returned: always
          sample: "123456"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "name", "description", "assets_ttl_days")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = ["name", "description", "assets_ttl_days"]
    payload = build_payload(module, payload_keys)

    endpoint = "networks"

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
