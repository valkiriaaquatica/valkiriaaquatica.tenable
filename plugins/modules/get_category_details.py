# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_category_details
short_description: Returns the details for the specified category.
version_added: "0.0.1"
description:
  - This module returns the details for the specified category.
  - The module is made from https://developer.tenable.com/reference/tags-tag-category-details docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.category
"""

EXAMPLES = r"""
- name: Get tag categories details
  get_category_details:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    category_uuid: "{{ tag_category_uuid }}"

- name: Get tag categories details using enviroment creds
  get_category_details:
    category_uuid: "12345"
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: always when a request is made, independent if it correct or incorrect.
  contains:
    data:
      description: Details of the created or updated entity including metadata and identifiers.
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
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "category_uuid")
    argument_spec["category_uuid"]["required"] = True  # in arguments is required False

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"tags/categories/{module.params['category_uuid']}"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
