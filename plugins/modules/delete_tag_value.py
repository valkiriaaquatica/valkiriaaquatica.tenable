# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: delete_tag_value
short_description: Deletes the specified tag value.
version_added: "0.0.1"
description:
  - This module  deletes an agent group.
  - If you delete an asset tag, Tenable Vulnerability Management also removes that tag from any assets where the tag was assigned.
  - Note If you delete all asset tags associated with a category, Tenable Vulnerability Management retains the category.
  -  You must delete the category separately with delete_tag_category module or https://developer.tenable.com/reference/tags-delete-tag-category .
  - Additionally, to delete a tag value, you must be an admin or have edit permissions on the tag value.
  - The module is made from https://developer.tenable.com/reference/tags-delete-tag-value docs.
  - Requires SCAN OPERATOR [24] user permissions as specified in the Tenable.io API documentation.
options:
  value_uuid:
    description:
      - The UUID of the tag value you want to delete.
      - A tag UUID is technically assigned to the tag value only (the second half of the category:value pair).
      - But the API commands use this value to represent the whole category:value pair
      - For more information on determining this value, see https://developer.tenable.com/docs/determine-tag-identifiers-tio
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Delete tag value
  delete_tag_value:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    value_uuid: "{{ tag_value_uuid }}"

- name: Delete tag value using enviroment creds
  delete_tag_value:
    value_uuid: "123456"
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
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {"value_uuid": {"required": True, "type": "str"}}  # unique for this module
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"tags/values/{module.params['value_uuid']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
