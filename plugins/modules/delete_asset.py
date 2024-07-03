# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: delete_asset
short_description: Deletes the specified asset.
version_added: "0.0.1"
description:
  - This module fetches detailed information about a specific asset.
  - When you delete an asset, Tenable Vulnerability Management deletes vulnerability data associated with the asset.
  - Deleting an asset does not immediately subtract the asset from your licensed assets count.
  - Deleted assets continue to be included in the count until they automatically age out as inactive.
  - The module is made from https://developer.tenable.com/reference/workbenches-assets-delete docs.
  - For information and best practices for retrieving vulnerability see https://developer.tenable.com/docs/retrieve-vulnerability-data-from-tenableio
  - For information and best practices for retrieving assets see https://developer.tenable.com/docs/retrieve-asset-data-from-tenableio
  - Note This endpoint is not intended for large or frequent exports of vulnerability or assets data.
  - Requires SCAN OPERATOR [24] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
"""

EXAMPLES = r"""
- name: Delete an asset
  delete_asset:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    asset_uuid: 11111

- name: Delete an asset using enviroment creds
  delete_asset:
    asset_uuid: 11111
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

    endpoint = f"workbenches/assets/{module.params['asset_uuid']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
