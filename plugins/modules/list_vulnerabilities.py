# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_vulnerabilities
short_description: Returns a list of recorded vulnerabilities.
version_added: "0.0.1"
description:
  - This modules returns a list of assets and their vulnerabilities associated.
  - Filters can be applied.
  - The list returned is limited to 5,000. To retrieve more than 5,000 vulnerabilities, use the export_workbench module (deprecated).
  - Additionally, this endpoint only returns data less than 450 days (15 months) old.
  - Note This endpoint is not intended for large or frequent exports of vulnerability or assets data.
  - Tenable recommends the export_vulnerabilities  module or https://developer.tenable.com/reference/exports-vulns-request-export for large amount.
  - For information and best practices for retrieving vulnerability see https://developer.tenable.com/docs/retrieve-vulnerability-data-from-tenableio
  - For information and best practices for retrieving assets see https://developer.tenable.com/docs/retrieve-asset-data-from-tenableio
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/workbenches-vulnerabilities docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filter_search_type
  - valkiriaaquatica.tenable.filters
"""


EXAMPLES = r"""
- name: List vulnerabilities with fiilters and date range
  list_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    date_range: 2
    filters:
      - type: plugin.attributes.vpr.score
        operator: eq
        value: "5"

- name: List vulnerabilities with two condicional and filters and using enviroment creds
  list_vulnerabilities:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filters:
      - type: plugin.attributes.vpr.score
        operator: eq
        value: "5"
      - type: tracking.state
        operator: neq
        value: "Fixed"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about the assets and vulnerabilities.
      type: dict
      contains:
        total_asset_count:
          description: The total number of assets.
          type: int
          returned: always
          sample: 0
        total_vulnerability_count:
          description: The total number of vulnerabilities found across all assets.
          type: int
          returned: always
          sample: 1
        vulnerabilities:
          description: A list of detailed vulnerability information.
          type: list
          elements: dict
          contains:
            accepted_count:
              description: The number of vulnerabilities that have been accepted as manageable risks.
              type: int
              returned: always
              sample: 0
            count:
              description: The number of instances this particular vulnerability has been found.
              type: int
              returned: always
              sample: 1
            counts_by_severity:
              description: A list of counts of vulnerabilities classified by their severity.
              type: list
              elements: dict
              contains:
                count:
                  description: The count of vulnerabilities for the particular severity level.
                  type: int
                  returned: always
                  sample: 1
                value:
                  description: The severity level value.
                  type: int
                  returned: always
                  sample: 1
            cvss3_base_score:
              description: The CVSS version 3 base score of the vulnerability.
              type: float
              returned: always
              sample: 6.5
            cvss_base_score:
              description: The CVSS version 2 base score of the vulnerability.
              type: float
              returned: always
              sample: 6.4
            plugin_family:
              description: The family of the plugin that identified the vulnerability.
              type: str
              returned: always
              sample: "amazon linux"
            plugin_id:
              description: The unique identifier of the plugin that identified the vulnerability.
              type: int
              returned: always
              sample: 123456
            plugin_name:
              description: The name of the plugin that identified the vulnerability.
              type: str
              returned: always
              sample: "amazon linux)"
            recasted_count:
              description: The number of vulnerabilities that have been recast or reclassified by the user.
              type: int
              returned: always
              sample: 0
            severity:
              description: The severity rating of the vulnerability.
              type: int
              returned: always
              sample: 2
            vpr_score:
              description: Tenable's Vulnerability Priority Rating (VPR) score for the vulnerability.
              type: float
              returned: always
              sample: 5
            vulnerability_state:
              description: The current state of the vulnerability, ex, active, solved.
              type: str
              returned: always
              sample: "Active"
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "filters", "filter_search_type", "date_range")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "workbenches/vulnerabilities"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                date_range=module.params["date_range"],
                filter_search_type=module.params["filter_search_type"],
            ),
            module.params["filters"],
            handle_multiple_filters,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
