# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_tag_value
short_description: Creates a tag value.
version_added: "0.0.1"
description:
  - This module creates a tag value.
  - The tag category can be specified by UUID or name.
  - If Tenable Vulnerability Management cannot find a category you specify by name, the system creates a new category with the specified name
  - To automatically apply the tag to assets, specify the rules using the filters property.
  - Module made from https://developer.tenable.com/reference/tags-create-tag-value docs.
  - Requires SCAN MANAGER [40] user permissions
options:
  category_name:
    description:
      - The name of the tag category to associate with the new value.
      - Specify the name of a new category if you want to add both a new category and tag value.
      - Specify the name of an existing category if you want to add the tag value to the existing category.
      - The category_name can result in the following responses.
      - If category_name and tag value exists  a error 400 is returned.
      - If category_name exists but not tag value, Tenable adds the tag value to the existing category.
      - If category_name and tag value do not exist, Tenable creates a new tag category and adds the new tag value to that category.
    type: str
    required: false
  category_uuid:
    description:
      - The UUID of the tag category to associate with the new value.
      - This parameter is used to add the tag value to an existing category. If the UUID does not exist, a 400 error is returned.
      - This parameter is required if category_name is not present in the request message.
    type: str
    required: false
  category_description:
    description:
      - Description for a new tag category that is created if the category specified by name does not exist.
      - Otherwise, Tenable Vulnerability Management ignores the description
    type: str
    required: false
  value:
    description:
      - The new tag value. Cannot exceed 50 characters in length and must not contain commas.
    type: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.tag_value_args
"""


EXAMPLES = r"""
- name: Create tag value using enviroment creds, matching with a category
  create_tag_value:
    value: "name_value"
    category_name: "name"
    category_uuid: "12345"

- name: Create tag value and apply them in the assets where aws_ec2_name is equal to jenkins
  create_tag_value:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    value: "name_2"
    category_name: "cat_1"
    filters:
      asset:
        and:
          - field: aws_ec2_name
            operator: eq
            value: jenkins

- name: Create tag value aand apply ir to all assets that are licensed or their sysid is not equal to sysid123456
  create_tag_value:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    value: "name_2"
    category_name: "cat_1"
    filters:
      asset:
        or:
          - field: is_was_licensed
            operator: eq
            value: true
          - field: servicenow_sysid
            operator: neq
            value: sysid123456
"""


RETURN = r"""
api_response:
  description: Detailed information about the creation of the tag value.
  returned: always
  type: dict
  contains:
    data:
      description: Contains details about the tag such as access controls, metadata, and properties related to the tag's category.
      type: dict
      returned: always
      sample:
        access_control:
          current_user_permissions: ["permission1", "permission2"]
        category_description: "this is the description"
        category_name: "name"
        category_uuid: "123456"
        consecutive_error_count: 0
        created_at: "date"
        created_by: "email@email.com"
        filters:
          asset: "{\"and\": [{\"value\": [\"name_asset\"], \"operator\": \"eq\", \"property\": \"aws_ec2_name\"}]}"
        product: "1"
        saved_search: false
        type: "dynamic"
        updated_at: "date"
        updated_by: "name@name.com"
        uuid: "123456"
        value: "use"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_repeated_special_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_tag_values_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec(
        "access_key",
        "secret_key",
        "category_name",
        "category_uuid",
        "category_description",
        "value",
        "description",
        "access_control",
        "",
    )
    special_spec = get_repeated_special_spec("filters", "value")
    argument_spec = {**common_spec, **special_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "tags/values"
    payload = build_tag_values_payload(module.params)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
