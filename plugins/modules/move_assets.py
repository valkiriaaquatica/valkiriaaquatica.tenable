# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: move_assets
short_description: Moves assets from the specified network to another network
version_added: "0.0.1"
description:
  - This module moves assets from the specified network to another network
  - You can use this endpoint to move assets from the default network to a user-defined network
  - You can use this endpoint to move assets from a user-defined network to the default network
  - You can use this endpoint to move assets from one user-defined network to another user-defined network
  - This request creates an asynchronous job in Tenable Vulnerability Management.
  - This module is made from https://developer.tenable.com/reference/assets-bulk-move docs.
  - Requires SCAN OPERATOR [24] user permissions as specified in the Tenable.io API documentation.
options:
  source:
    description:
      - The UUID of the network currently associated with the assets.
      - Use list_networks module to list the networks and get the uuid.
    required: true
    type: str
  destination:
    description:
      - The UUID of the network to associate with the specified assets.
      - Use list_networks module to list the networks and get the uuid.
    required: true
    type: str
  targets:
    description:
      - The IPv4 addresses of the assets to move.
      - The addresses can be represented as a comma-separated list "192.168.1.10,10.10.4.2"
      - The addresses can be represented as a CIDR "1.1.1.0/24"
      - The addresses can be represented as a range "2.2.2.2-2.2.2.200"
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""


EXAMPLES = r"""
- name: Move one asset network and enviroment creds
  move_assets:
    source: "123456"
    destinatation: "654321"
    targets: "192.168.1.120"

- name: Move a range of assets network passing variable creds
  move_assets:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    source: "123456"
    destinatation: "654321"
    targets: "10.10.10.1-10.10.10.80"

- name: Move a whole CIDR of assets
  move_assets:
    source: "123456"
    destinatation: "654321"
    targets: "10.10.10.0/24"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response moving 1 asset.
  type: dict
  returned: always
  contains:
    data:
      description: Contains the response data for the moving operation.
      type: dict
      contains:
        response:
          description: Nested response data.
          type: dict
          contains:
            data:
              description: Further nested data providing details about the asset movement.
              type: dict
              contains:
                asset_count:
                  description: The number of assets that were moved.
                  type: int
                  returned: always
                  sample: 1
    status_code:
      description: HTTP status code returned by the API after the asset movement.
      type: int
      returned: always
      sample: 202
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    # specified arguments for this module
    specific_spec = {
        "source": {"required": True, "type": "str"},
        "destination": {"required": True, "type": "str"},
        "targets": {"required": True, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "api/v2/assets/bulk-jobs/move-to-network"

    payload_keys = ["source", "destination", "targets"]
    payload = build_payload(module, payload_keys)
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
