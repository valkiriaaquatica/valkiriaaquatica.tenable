# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: list_tag_categories
short_description: Returns a list of tag categories.
version_added: "0.0.1"
description:
  - This module retrieves a list of tag categories from Tenable.io
  - Supporting complex filtering,date, offset and limit.
  - Module made from https://developer.tenable.com/reference/tags-list-tag-categoriesdocs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.filter_type
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.generics
"""


EXAMPLES = r"""
- name: List tag categories using enviroment creds
  list_tag_categories:

- name: List tag categories using enviroment creds
  list_tag_categories:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    limit: 1

- name: List tag categories using enviroment creds and filtering
  list_tag_categories:
    filters:
      - type: name
        operator: eq
        value: name
"""

RETURN = r"""
api_response:
  description:  Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about network categories.
      type: dict
      contains:
        categories:
          description: A list of categories within the networks.
          type: list
          elements: dict
          contains:
            created_at:
              description: The date and time when the category was created.
              type: str
              returned: always
              sample: "2023-01-01T00:00:00Z"
            created_by:
              description: Email of the user who created the category.
              type: str
              returned: always
              sample: "email@email.com"
            description:
              description: Description of the category.
              type: str
              returned: always
              sample: ""
            name:
              description: Name of the category.
              type: str
              returned: always
              sample: "name"
            product:
              description: Product identifier associated with the category.
              type: str
              returned: always
              sample: "1"
            reserved:
              description: Indicates if the category is reserved.
              type: bool
              returned: always
              sample: false
            updated_at:
              description: The date and time when the category was last updated.
              type: str
              returned: always
              sample: "2023-01-02T00:00:00Z"
            updated_by:
              description: Email of the user who last updated the category.
              type: str
              returned: always
              sample: "autobit@nttdata.com"
            uuid:
              description: UUID of the category.
              type: str
              returned: always
              sample: "12356"
        pagination:
          description: Pagination details of the list.
          type: dict
          contains:
            limit:
              description: The maximum number of records returned per page.
              type: int
              returned: always
              sample: 5000
            offset:
              description: The offset from which records start.
              type: int
              returned: always
              sample: 0
            total:
              description: The total number of records available.
              type: int
              returned: always
              sample: 1
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
    argument_spec = get_spec("access_key", "secret_key", "filters", "filter_type", "limit", "offset", "sort")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = "tags/categories"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                limit=module.params["limit"],
                offset=module.params["offset"],
                sort=module.params["sort"],
                filter_type=module.params["filter_type"],
            ),
            module.params["filters"],  # this is handled by handle_special_filter
            handle_special_filter,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
