# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_tag_category
short_description: Updates the specified tag category
version_added: "0.0.1"
description:
  - This module updates the specified tag category.
  - To update a category you must be an admin or have edit permissions on all tags within the category.
  - The module is made from https://developer.tenable.com/reference/tags-edit-tag-categorydocs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  description:
    description:
      - The description of the tag category.
      - Must not exceed 3,000 characters.
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.category
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Update tag category
  update_tag_category:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    category_uuid: "{{ tag_category_uuid }}"
    name: "i_am_the_new_name"
    description: "i am the new description"

- name: Update tag category using enviroment creds
  update_tag_category:
    category_uuid: "12345"
    name: "i_am_the_new_name"
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains details about the entity such as creation, update information, and identifiers.
      type: dict
      returned: always
      sample:
        created_at: "123456"
        created_by: "email@email.com"
        description: "this is the description"
        name: "name"
        product: "1"
        reserved: false
        updated_at: "123456"
        updated_by: "email@email.com"
        uuid: "123456"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "category_uuid", "name", "description")
    argument_spec["category_uuid"]["required"] = True

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = ["name", "description"]
    payload = build_payload(module, payload_keys)

    endpoint = f"tags/categories/{module.params['category_uuid']}"

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
