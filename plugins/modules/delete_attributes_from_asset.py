# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: delete_attributes_from_asset
short_description: Returns a list of custom asset attributes assigned to the specified asset.
version_added: "0.0.1"
description:
  - This module deletes all custom asset attributes assigned to the specified asset.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/io-v3-asset-attributes-assigned-delete docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
"""

EXAMPLES = r"""
- name: List attributes assigned to asset
  delete_attributes_from_asset:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    asset_uuid: "12345"

- name: List attributes assigned to asset using enviroment creds
  delete_attributes_from_asset:
    asset_uuid: "98746"
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
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"api/v3/assets/{module.params['asset_uuid']}/attributes"
    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
