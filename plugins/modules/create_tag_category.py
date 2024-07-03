# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_tag_category
short_description: Deletes the specified category and any associated tag values
version_added: "0.0.1"
description:
  - This module  Deletes the specified category and any associated tag values
  - Deleting an asset tag category automatically deletes all tag values associated with that category
    and removes the tags from any assets where the tags were assigned
  - To delete a category you must be an admin or have edit permissions on all tags within the category.
  - The module is made from https://developer.tenable.com/reference/tags-delete-tag-category docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  description:
    description:
      - The description of the tag category.
      - Must not exceed 3000 characters.
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Create tag ceategory
  create_tag_category:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    name: "name"
    description: "i am the description"

- name: Create tag ceategory using enviroment creds
  create_tag_category:
    name: "name"
"""

RETURN = r"""
api_response:
  description: Detailed information about the API response.
  returned: always
  type: complex
  contains:
    data:
      description: Data returned by the API, if any.
      type: dict
      returned: on success
      contains:
        created_at:
          description: Timestamp when the tag category was created.
          type: str
          returned: always
          sample: "123456"
        created_by:
          description: Email of the user who created the tag category.
          type: str
          returned: always
          sample: "email@email.com"
        description:
          description: Description of the tag category.
          type: str
          returned: always
          sample: "this is the description"
        name:
          description: Name of the tag category.
          type: str
          returned: always
          sample: "name"
        product:
          description: Product associated with the tag category.
          type: str
          returned: always
          sample: "1"
        reserved:
          description: Indicates if the category is reserved.
          type: bool
          returned: always
          sample: false
        updated_at:
          description: Timestamp when the tag category was last updated.
          type: str
          returned: always
          sample: "123456"
        updated_by:
          description: Email of the user who last updated the tag category.
          type: str
          returned: always
          sample: "email@email.com"
        uuid:
          description: UUID of the tag category.
          type: str
          returned: always
          sample: "123456"
  sample: |
    {
      "data": {
        "created_at": "123456",
        "created_by": "email@email.com",
        "description": "this is the description",
        "name": "name",
        "product": "1",
        "reserved": false,
        "updated_at": "123456",
        "updated_by": "email@email.com",
        "uuid": "123456"
      },
      "status_code": 200
    }
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "name", "description")
    argument_spec["name"]["required"] = True

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "tags/categories"
    payload_keys = ["name", "description"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
