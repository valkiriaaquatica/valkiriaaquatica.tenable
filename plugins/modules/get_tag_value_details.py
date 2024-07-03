# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_tag_value_details
short_description: Returns the details for specified tag value.
version_added: "0.0.1"
description:
  - This module returns the details for specified tag value.
  - The module is made from https://developer.tenable.com/reference/tags-tag-value-details docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  value_uuid:
    description:
      - The UUID of the tag value.
      - Use the list_tag_values module to list and get the id.
      - For more information on determining this value, see https://developer.tenable.com/docs/determine-tag-identifiers-tio
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Get tag value details
  get_tag_value_details:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    value_uuid: "{{ tag_value_uuid }}"

- name: Get tag value details using enviroment creds
  get_tag_value_details:
    value_uuid: "123456"
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about a category within the system, including metadata and access control settings.
      type: dict
      returned: on success
      sample:
        access_control:
          current_user_permissions: ["CAN_USE", "CAN_EDIT"]
        category_description: "this is the category_description"
        category_name: "name"
        category_uuid: "123456"
        consecutive_error_count: 0
        created_at: "date"
        created_by: "email@email.com"
        description: "description i am"
        product: "IO"
        saved_search: false
        type: "static"
        updated_at: "date"
        updated_by: "email@email.com"
        uuid: "123456"
        value: "value i'm"
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
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {
        "value_uuid": {"required": True, "type": "str"},
    }

    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"tags/values/{module.params['value_uuid']}"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
