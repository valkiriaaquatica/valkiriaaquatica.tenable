# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_asset_with_vulnerabilities
short_description: Returns a list of assets with their vulnerability data from Tenable.io.
version_added: "0.0.1"
description:
  - This modules returns a list of assets and their vulnerabilities associated.
  - Filters can be applied.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/workbenches-assets-vulnerabilities docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.filter_search_type
"""

EXAMPLES = r"""
- name: Get assets within vulnerbailities have 1 day old
  list_asset_with_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    date_range: 1

- name: Retrieve assets with a specific IPv4 address
  list_asset_with_vulnerabilities:
    access_key: your_access_key
    secret_key: your_secret_key
    filters:
      - type: ipv4
        operator: eq
        value: "192.168.1.150"

- name: Get assets with log4j and with enviroment credential variables
  list_asset_with_vulnerabilities:
    filter_search_type: and
    filters:
      - type: plugin.name
        operator: match
        value: log4j

- name: Get assets from a project that have critical vulns in the last week using enviroment creds
  list_asset_with_vulnerabilities:
    date_range: 7
    filter_search_type: and
    filters:
      - type: severity
        operator: eq
        value: "Critical"
      - type: tag.Project
        operator: set-has
        value: "Project Name"

- name: Get assets where crictical vulns where found in last 24 hours
  list_asset_with_vulnerabilities:
    date_range: 1
    filters:
      - type: severity
        operator: eq
        value: "Critical"

- name: Get assets filtering with ip
  list_asset_with_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filters:
      - type: host.target
        operator: eq
        value: "172.31.1.4,192.168.32.118"

- name: Get assets  that have a vulnerability that the solution is to Update the affected packages and enviroment creds
  list_asset_with_vulnerabilities:
    filters:
      - type: plugin.attributes.solution
        operator: match
        value: "Update the affected packages"
  tags:
    - vulns
"""

RETURN = r"""
api_response:
  description: The API response containing assets details.
  returned: on success
  type: complex
  contains:
    data:
      description: The data containing the list of assets and their details.
      type: dict
      contains:
        assets:
          description: A list of assets that match the filter criteria. In this case just 1
          type: list
          elements: dict
          sample: [
            {
              "agent_name": ["name_of_asset"],
              "fqdn": ["name_of_asset_fdqn"],
              "id": "022342281",
              "ipv4": ["192.168.1.120", "172.145..6"],
              "ipv6": ["451sd::5615d:14ff:541457:451", "451sd::5615d:14ff:541457:452"],
              "last_seen": "2021-04-22T06:53:37.428Z",
              "netbios_name": [],
              "severities": [
                {"count": 0, "level": 0, "name": "Info"},
                {"count": 0, "level": 1, "name": "Low"},
                {"count": 2, "level": 2, "name": "Medium"},
                {"count": 0, "level": 3, "name": "High"},
                {"count": 1, "level": 4, "name": "Critical"}
              ],
              "total": 3
            }
          ]
        total_asset_count:
          description: The total number of assets matching the filter criteria.
          type: int
          sample: 1
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "date_range", "filters", "filter_search_type")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "workbenches/assets/vulnerabilities"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                date_range=module.params["date_range"], filter_search_type=module.params["filter_search_type"]
            ),
            module.params["filters"],
            handle_multiple_filters,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
