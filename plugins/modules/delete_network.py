# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: delete_network
short_description: Deletes the specified network object
version_added: "0.0.1"
description:
  - This module deletes the specified network object
  - Before you delete a network object, consider moving assets to a different network using the bulk asset move_assets module.
  - You can view deleted network objects using the includeDeleted in the list_networks module.
  - The module is made from https://developer.tenable.com/reference/networks-delete docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  network_id:
    description:
      - The id of the network to delete.
      - Use the list_networks module to get the id.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Delete exclusion
  delete_network:
    network_id: 12345

- name: Delete exclusion
  delete_network:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    network_id: 12345
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable api.
  returned: always when a request is made, independent if it correct or incorrect.
  type: complex
  contains:
    status_code:
      description: The HTTP status code returned by the API if an error occurred.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "network_id")
    argument_spec["network_id"]["required"] = True

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"networks/{module.params['network_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
