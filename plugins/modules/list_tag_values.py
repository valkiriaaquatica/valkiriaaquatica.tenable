# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_tag_values
short_description: Returns a list of tag values.
version_added: "0.0.1"
description:
  - This module retrieves a list of agents from Tenable.io
  - The list can also include the tag categories that do not have any associated values.
  - Supporting complex filtering,wilcarding, sorting, limit.
  - Module made from https://developer.tenable.com/reference/tags-list-tag-values docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.filter_type
  - valkiriaaquatica.tenable.filters_wildcards
  - valkiriaaquatica.tenable.generics
"""


EXAMPLES = r"""
- name: List tag values that in their value contain dev using enviroment creds and limit 1
  list_tag_values:
    filters:
      - type: value
        operator: match
        value: dev
    limit: 1

- name: List tag values that the value is equal to Production and theis description is not equal to Test passing creds as variables
  list_tag_values:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filter_type: and
    filters:
      - type: value
        operator: eq
        value: Production
      - type: description
        operator: neq
        value: "Test"

- name: List tag values that in their value exists dev using credentials as variables
  list_tag_values:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    wildcard_text: financ
    wildcard_fields: category_name
"""

RETURN = r"""
api_response:
  description:  Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about tag values and their attributes.
      type: dict
      contains:
        pagination:
          description: Pagination details of the list.
          type: dict
          contains:
            limit:
              description: The maximum number of records returned per page.
              type: int
              returned: always
              sample: 1
            offset:
              description: The offset from which records start.
              type: int
              returned: always
              sample: 0
            total:
              description: The total number of records available.
              type: int
              returned: always
              sample: 516
        values:
          description: A list of tag values.
          type: list
          elements: dict
          contains:
            access_control:
              description: Access control settings for the current user regarding this tag.
              type: dict
              contains:
                current_user_permissions:
                  description: Permissions of the current user on this tag.
                  type: list
                  elements: str
                  returned: always
                  sample: ["CAN_USE"]
            category_description:
              description: Description of the tag category.
              type: str
              returned: always
              sample: "name"
            category_name:
              description: Name of the tag category.
              type: str
              returned: always
              sample: "name"
            category_uuid:
              description: UUID of the tag category.
              type: str
              returned: always
              sample: "123456"
            consecutive_error_count:
              description: Count of consecutive errors encountered by this tag.
              type: int
              returned: always
              sample: 0
            created_at:
              description: Date and time when the tag was created.
              type: str
              returned: always
              sample: "2023-01-01T00:00:00Z"
            created_by:
              description: Email of the user who created the tag.
              type: str
              returned: always
              sample: "email@email.com"
            description:
              description: Description of the tag.
              type: str
              returned: always
              sample: "name"
            processed_at:
              description: Date and time when the tag was last processed.
              type: str
              returned: always
              sample: "2023-01-02T00:00:00Z"
            processing_status:
              description: Current processing status of the tag.
              type: str
              returned: always
              sample: "COMPLETE"
            product:
              description: Product associated with the tag.
              type: str
              returned: always
              sample: "IO"
            saved_search:
              description: Indicates if this tag is part of a saved search.
              type: bool
              returned: always
              sample: false
            type:
              description: Type of the tag, e.g., dynamic or static.
              type: str
              returned: always
              sample: "dynamic"
            updated_at:
              description: Date and time when the tag was last updated.
              type: str
              returned: always
              sample: "2023-01-02T00:00:00Z"
            updated_by:
              description: Email of the user who last updated the tag.
              type: str
              returned: always
              sample: "email@email.com"
            uuid:
              description: UUID of the tag.
              type: str
              returned: always
              sample: "123456"
            value:
              description: Value of the tag.
              type: str
              returned: always
              sample: "name"
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_special_filter
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec(
        "access_key",
        "secret_key",
        "filter_type",
        "filters",
        "wildcard_fields",
        "wildcard_text",
        "limit",
        "offset",
        "sort",
    )
    module = AnsibleModule(argument_spec=common_spec, supports_check_mode=False)
    endpoint = "tags/values"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                filter_type=module.params["filter_type"],
                wildcard_text=module.params["wildcard_text"],
                wildcard_fields=module.params["wildcard_fields"],
                limit=module.params["limit"],
                offset=module.params["offset"],
                sort=module.params["sort"],
            ),
            module.params["filters"],
            handle_special_filter,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
