# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_plugin_details
short_description: Retrieves the details for a plugin.
version_added: "0.0.1"
description:
  - This module retrieves the details for a plugin.
  - Note this endpoint is not intended for large or frequent exports of data.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - This module was made from https://developer.tenable.com/reference/workbenches-vulnerability-info docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.plugin
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.filter_search_type
"""

EXAMPLES = r"""
- name: Retrieve plugin details with specific filters
  get_plugin_details:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    plugin_id: 123456
    filters:
      - type: plugin.attributes.vpr.score
        operator: gte
        value: "6.5"

- name: Get plugin details using environmental credentials
  get_plugin_details:
    plugin_id: 123456
"""

RETURN = r"""
api_response:
  description: The API response containing plugin details.
  returned: on success
  type: complex
  contains:
    data:
      description: Detailed information about the plugin.
      type: dict
      contains:
        info:
          description: Detailed description of the plugin.
          type: dict
          contains:
            accepted_count:
              description: The number of times the plugin's findings have been accepted.
              type: int
            count:
              description: The count of vulnerabilities identified by this plugin.
              type: int
            description:
              description: The description of the vulnerability.
              type: str
            discovery:
              description: Discovery dates of the vulnerability.
              type: dict
              contains:
                seen_first:
                  description: The first date the vulnerability was seen.
                  type: str
                seen_last:
                  description: The most recent date the vulnerability was seen.
                  type: str
            plugin_details:
              description: Details about the plugin.
              type: dict
              contains:
                family:
                  description: The family to which the plugin belongs.
                  type: str
                modification_date:
                  description: The date when the plugin was last modified.
                  type: str
                name:
                  description: The name of the plugin.
                  type: str
                publication_date:
                  description: The publication date of the plugin.
                  type: str
                severity:
                  description: The severity rating of the vulnerability.
                  type: int
                type:
                  description: The type of the plugin.
                  type: str
                version:
                  description: The version of the plugin.
                  type: str
            risk_information:
              description: Information about the risk associated with the vulnerability.
              type: dict
              contains:
                cvss3_base_score:
                  description: The CVSS v3 base score of the vulnerability.
                  type: float
                cvss3_temporal_score:
                  description: The CVSS v3 temporal score of the vulnerability.
                  type: float
                cvss3_temporal_vector:
                  description: The CVSS v3 temporal vector of the vulnerability.
                  type: str
                cvss3_vector:
                  description: The CVSS v3 vector of the vulnerability.
                  type: str
                cvss_base_score:
                  description: The CVSS base score of the vulnerability.
                  type: float
                cvss_temporal_score:
                  description: The CVSS temporal score of the vulnerability.
                  type: float
                cvss_temporal_vector:
                  description: The CVSS temporal vector of the vulnerability.
                  type: str
                cvss_vector:
                  description: The CVSS vector of the vulnerability.
                  type: str
                risk_factor:
                  description: The risk factor of the vulnerability.
                  type: str
                stig_severity:
                  description: The STIG severity of the vulnerability.
                  type: str
            see_also:
              description: Related links and references for further information.
              type: list
              elements: str
status_code:
  description: HTTP status code returned by the API.
  returned: always
  type: int
  sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "plugin_id", "date_range", "filters", "filter_search_type")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                date_range=module.params["date_range"], filter_search_type=module.params["filter_search_type"]
            ),
            module.params["filters"],
            handle_multiple_filters,
        )

    endpoint = f"workbenches/vulnerabilities/{module.params['plugin_id']}/info"
    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
