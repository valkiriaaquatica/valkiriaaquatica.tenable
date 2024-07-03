# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: delete_tag_category
short_description: Deletes the specified category and any associated tag values.
version_added: "0.0.1"
description:
  - This module  Deletes the specified category and any associated tag values
  - Deleting an asset tag category automatically deletes all tag values associated with that category
    and removes the tags from any assets where the tags were assigned
  - To delete a category you must be an admin or have edit permissions on all tags within the category.
  - The module is made from https://developer.tenable.com/reference/tags-delete-tag-category docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  category_uuid:
    description:
      - The UUID of the category to delete.
      - For more information on determining this value, see https://developer.tenable.com/docs/determine-tag-identifiers-tio.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""


EXAMPLES = r"""
- name: Delete tag category using creds as vars
  delete_tag_category:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    category_uuid: "{{ tag_category_uuid }}"

- name: Delete tag category using enviroment creds
  delete_tag_category:
    category_uuid: "{{ tag_category_uuid }}"
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
    argument_spec = get_spec("access_key", "secret_key", "category_uuid")
    argument_spec["category_uuid"]["required"] = True

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"tags/categories/{module.params['category_uuid']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
