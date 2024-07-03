# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: add_or_remove_asset_tags
short_description: Adds or removes tags to/from assets.
version_added: "0.0.1"
description:
  - This module adds or removes tags to/from assets.
  - Adds a tag value to asset.
  - This module is made from https://developer.tenable.com/reference/tags-assign-asset-tags docs.
  - Requires BASIC  [16] user permissions as specified in the Tenable.io API documentation.
options:
  action:
    description:
      - Specifies whether to add or remove tags.
    type: str
    required: true
    choices:
      - add
      - remove
  assets:
    description:
      - An array of asset UUIDs to which the tags should be added or from which tags should be removed.
      - For more information on determining values for this array https://developer.tenable.com/docs/determine-tag-identifiers-tio
    type: list
    elements: str
    required: true
  tags:
    description:
      - A list of tag value UUIDs to be assigned or removed.
      - For more information on determining values for this array https://developer.tenable.com/docs/determine-tag-identifiers-tio
    type: list
    elements: str
    required: true
author:
  - Fernando Mendieta Ovejero (@fernandomendietaovejero)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Add the tag to an asset
  add_or_remove_asset_tags:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    action: add
    assets: "123456789"
    tags: "first_tag_uuid,second_tag_uuid"

- name: Remove a tag using enviroment creds
  add_or_remove_asset_tags:
    action: remove
    assets: "{{ asset }}"
    tags: "{{ tag }}"
  register: remove_tag_to_asset

- name: Add the tag to several assets
  add_or_remove_asset_tags:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    action: add
    assets: "first_asset,second_asset"
    tags: "new_tag"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    data:
      description: Contains specific data about the operation.
      type: dict
      returned: always
      contains:
        job_uuid:
          description: Unique identifier for the job created.
          type: str
          returned: always
          sample: "123456789"
    status_code:
      description: HTTP status code returned by the Tenable.io API.
      type: int
      returned: always
      sample: 200
    changed:
      description: Indicates if any change was made by the operation.
      type: bool
      returned: always
      sample: true
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    # no other module has this arguments
    specific_spec = {
        "action": {"required": True, "type": "str", "choices": ["add", "remove"]},
        "assets": {"required": True, "type": "list", "elements": "str"},
        "tags": {"required": True, "type": "list", "elements": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )
    payload_keys = ["action", "assets", "tags"]
    payload = build_payload(module, payload_keys)
    endpoint = "tags/assets/assignments"
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
