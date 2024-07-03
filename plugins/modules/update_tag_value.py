# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_tag_value
short_description: Updates the specified tag value.
version_added: "0.0.1"
description:
  - This module updates the specified tag value.
  - The tag category can be specified by UUID or name.
  - Module made from https://developer.tenable.com/reference/tags-update-tag-value docs.
  - Requires SCAN OPERATOR [28] user permissions
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.tag_value
  - valkiriaaquatica.tenable.tag_value_args
"""


EXAMPLES = r"""
- name: Update tag value
  update_tag_value:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    value_uuid: "{{ tag_value_uuid }}"
    value: "this_is_the_new_value"

- name: Update tag value with envirometn creds and new filters
  update_tag_value:
    value_uuid: "123456"
    value: "this_is_the_new_value"
    filters:
      asset:
        and:
          - field: aws_ec2_name
            operator: eq
            value: jenkins
"""


RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  returned: always when a request is made, independent if it is correct or incorrect.
  type: dict
  contains:
    data:
      description: Contains detailed information about a category including access controls, metadata, and specific properties related to the category.
      type: dict
      returned: always
      sample:
        access_control:
          current_user_permissions: "CAN_USE"
        category_description: "this is the description"
        category_name: "category_name_i_am"
        category_uuid: "123456"
        consecutive_error_count: 0
        created_at: "date"
        created_by: "autobit@nttdata.com"
        description: "tag for dev machines"
        product: "IO"
        saved_search: false
        type: "static"
        updated_at: "date"
        updated_by: "email@email.com"
        uuid: "123456"
        value: "new_value"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_repeated_special_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "access_control", "value_uuid", "value", "description")
    special_spec = get_repeated_special_spec("filters")

    argument_spec = {**common_spec, **special_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = [key for key in module.params.keys() if key not in ["access_key", "secret_key", "value_uuid"]]
    payload = build_payload(module, payload_keys)

    endpoint = f"tags/values/{module.params['value_uuid']}"

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
