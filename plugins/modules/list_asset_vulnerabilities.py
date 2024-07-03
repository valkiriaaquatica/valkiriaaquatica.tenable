# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_asset_vulnerabilities
short_description: Lists vulnerabilities for a specific asset in Tenable.io.
version_added: "0.0.1"
description:
  - Retrieves a list of recorded vulnerabilities for a specified asset.
  - Allows filtering results based on various criteria such as date range and severity.
  - Module made from https://developer.tenable.com/reference/workbenches-asset-vulnerabilities
  - The response to this endpoint is not returning any text, even if the asset does not exist.s
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.filter_search_type
  - valkiriaaquatica.tenable.date
"""

EXAMPLES = r"""
- name: Get all vulnerbailties from an asset
  list_asset_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_uuid: "123456789"

- name: Get all vulnerbailties from an asset within a date_range
  list_asset_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_uuid: "123456789"
    date_range: 80

- name: Get vulnerbailties filtered by three conditionals and condition
  list_asset_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_uuid: "123456789"
    filter_search_type: "and"
    filters:
      - type: severity
        operator: eq
        value: Info
      - type: plugin.family_id
        operator: eq
        value: 23
      - type: tracking.state
        operator: eq
        value: Active

- name: Get vulnerbailties filtered by three conditionals and or condition
  list_asset_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_uuid: "123456789"
    filter_search_type: "or"
    filters:
      - type: severity
        operator: eq
        value: Info
      - type: plugin.family_id
        operator: eq
        value: 23
      - type: tracking.state
        operator: eq
        value: Active

- name: Get vulns from asset applying filters and enviroment creds
  list_asset_vulnerabilities:
    asset_uuid: "123456789"
    filters:
      - type: plugin.attributes.solution
        operator: match
        value: "Update the affected packages"
      - type: plugin.attributes.cvss_base_score
        operator: gte
        value: "9.8"
      - type: tracking.state
        operator: eq
        value: "Active"
"""


RETURN = r"""
api_response:
  description: The API response containing vulnerability details for the specified asset.
  returned: on success
  type: dict
  contains:
    data:
      description: The data containing the details of the assets and their vulnerabilities.
      type: dict
      contains:
        total_asset_count:
          description: The total number of assets matching the filter criteria.
          type: int
          returned: always
          sample: 0
        total_vulnerability_count:
          description: The total number of vulnerabilities found for the assets.
          type: int
          returned: always
          sample: 17
        vulnerabilities:
          description: A list of vulnerabilities associated with the assets.
          type: list
          elements: dict
          returned: always
          sample: [
            {
              "accepted_count": 0,
              "count": 1,
              "counts_by_severity": [
                {
                  "count": 1,
                  "value": 4
                }
              ],
              "cvss3_base_score": 9.8,
              "cvss_base_score": 10.0,
              "plugin_family": "Red Hat Local Security Checks",
              "plugin_id": 100400,
              "plugin_name": "RHEL 6 / 7 : samba (RHSA-2017:1270) (SambaCry)",
              "recasted_count": 0,
              "severity": 4,
              "vpr_score": 7.4,
              "vulnerability_state": "Resurfaced"
            }
          ]
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid", "filters", "filter_search_type", "date_range")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"workbenches/assets/{module.params['asset_uuid']}/vulnerabilities"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                date_range=module.params["date_range"], filter_search_type=module.params["filter_search_type"]
            ),
            module.params["filters"],  # this is handled by handle_special_filter
            handle_multiple_filters,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
