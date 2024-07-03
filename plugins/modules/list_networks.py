# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_networks
short_description: Lists network objects for your organization.
version_added: "0.0.1"
description:
  - This module retrieves a lists network objects for your organization.
  - Supporting complex filtering, sorting, pagination, and the option to include deleted network objects.
  - Module made from https://developer.tenable.com/reference/networks-list docs.
  - Requires ADMINISTRATOR  [64] user permissions as specified in the Tenable.io API documentation.
  - ft option not included because is only suported OR value, there is no other option.
options:
  include_deleted:
    description:
      - Indicates whether to include deleted network objects in the response.
      - Deleted network objects contain the additional attributes, deleted and deleted_by
      - Which specifies the date (in Unix time) when the network object was deleted and the UUID of the user that deleted the network object.
    required: false
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.generics
  - valkiriaaquatica.tenable.filters
"""

EXAMPLES = r"""
- name: List all networks
  list_networks:
    access_key: your_access_key
    secret_key: your_secret_key
  register: all_networks

- name: List all network objects getting keys from enviroment variables
  list_networks:
  register: all_networks

- name: List network objects with filters and pagination
  list_networks:
    access_key: your_access_key
    secret_key: your_secret_key
    filters:
      - type: "name"
        operator: "eq"
        value: "aws_network_1"
    limit: 20
    offset: 0
    sort: "name:asc"
    include_deleted: false

- name: List all tenable networks with names and passing keys through enviroment
  list_networks:
    filters:
      - type: name
        operator: eq
        value: name1
      - type: name
        operator: eq
        value: name2
"""

RETURN = r"""
api_response:
  description: Detailed information of all the networks listed.
  type: dict
  returned: always
  contains:
    data:
      description: Contains detailed information about the network.
      type: dict
      contains:
        created:
          description: Timestamp in when the network was created.
          type: int
          returned: always
          sample: 1689849698540
        created_by:
          description: The UUID of the user who created the network.
          type: str
          returned: always
          sample: "fdfsd-c9e7-4e1d-sdfef-sfrfds"
        created_in_seconds:
          description: Timestamp  when the network was created.
          type: int
          returned: always
          sample: 1689849698
        is_default:
          description: Indicates whether this network is the default network.
          type: bool
          returned: always
          sample: false
        modified:
          description: Timestamp  when the network was last modified.
          type: int
          returned: always
          sample: 1689849698540
        modified_by:
          description: The UUID of the user who last modified the network.
          type: str
          returned: always
          sample: "SFREVFGF6"
        modified_in_seconds:
          description: Timestamp when the network was last modified.
          type: int
          returned: always
          sample: 1689849698
        name:
          description: Name of the network.
          type: str
          returned: always
          sample: "network_name"
        owner_uuid:
          description: UUID of the owner of the network.
          type: str
          returned: always
          sample: "CRFRE"
        scanner_count:
          description: The count of scanners associated with this network.
          type: int
          returned: always
          sample: 0
        uuid:
          description: The unique identifier of the network.
          type: str
          returned: always
          sample: "ssdfef-4f59-efgerg-b193-frtgtr"
        pagination:
          description: Pagination details of the response.
          type: dict
          contains:
            limit:
              description: The maximum number of records returned in the response.
              type: int
              returned: always
              sample: 1
            offset:
              description: The starting point from which records are returned.
              type: int
              returned: always
              sample: 0
            sort:
              description: List of sort conditions applied to the response.
              type: list
              elements: dict
              contains:
                name:
                  description: Name of the field by which the results are sorted.
                  type: str
                  returned: always
                  sample: "name"
                order:
                  description: Order of sorting, ascending or descending.
                  type: str
                  returned: always
                  sample: "asc"
            total:
              description: Total number of items available.
              type: int
              returned: always
              sample: 163
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
    common_spec = get_spec("access_key", "secret_key", "filters", "limit", "offset", "sort")
    specific_spec = {
        "include_deleted": {"required": False, "type": "bool"},  # unique for this module
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    def query_params():
        return add_custom_filters(
            build_query_parameters(limit=module.params["limit"], offset=module.params["offset"]),
            module.params["filters"],
            handle_special_filter,
        )

    run_module(module, "networks", query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
