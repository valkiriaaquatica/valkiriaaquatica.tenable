# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: list_tags_for_an_asset
short_description: Returns the tags an asset has.
version_added: "0.0.1"
description:
  - This module returns a list of assigned tags for an asset specified by UUID.
  - Module made from https://developer.tenable.com/reference/tags-list-asset-tags docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
"""


EXAMPLES = r"""
- name: List tags for an assset using enviroment creds
  list_tags_for_an_asset:
      asset_uuid: 123456
- name: List tags for an assset passing vars
  list_tags_for_an_asset:
      access_key: "{{ tenable_access_key }}"
      secret_key: "{{ tenable_secret_key }}"
      asset_uuid: 123456
"""


RETURN = r"""
api_response:
  description: Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about tags of the asset
      type: dict
      contains:
        tags:
          description: A list of tags associated with the asset.
          type: list
          elements: dict
          contains:
            asset_uuid:
              description: UUID of the asset associated with the tag.
              type: str
              returned: always
              sample: "123456"
            category_name:
              description: Name of the category to which the tag belongs.
              type: str
              returned: always
              sample: "Department"
            category_uuid:
              description: UUID of the category to which the tag belongs.
              type: str
              returned: always
              sample: "987654"
            container_uuid:
              description: UUID of the container where the tag is stored.
              type: str
              returned: always
              sample: "123789"
            created_at:
              description: Timestamp when the tag was created.
              type: str
              returned: always
              sample: "ci"
            product:
              description: Product type associated with the tag.
              type: str
              returned: always
              sample: "IO"
            source:
              description: Source of the tag, indicating how it was created.
              type: str
              returned: always
              sample: "dynamic"
            value:
              description: Value of the tag.
              type: str
              returned: always
              sample: "value"
            value_uuid:
              description: UUID of the tag value.
              type: str
              returned: always
              sample: "123456"
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    asset_uuid = module.params["asset_uuid"]
    endpoint = f"tags/assets/{asset_uuid}/assignments"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
