# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_plugin_outputs
short_description: Retrieves the vulnerability outputs for a plugin.
version_added: "0.0.1"
description:
  - This module fetches detailed information about a specific plugin from Tenable.io.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Note This endpoint is not intended for large or frequent exports of data.
  - This module was made from https://developer.tenable.com/reference/workbenches-vulnerability-output docs.
options:
  plugin_id:
    description:
      - The ID of the plugin to retrieve information for.
      - You can find the plugin ID by examining the output of list_vulnerabilities module.
    required: true
    type: int
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.filter_search_type
"""

EXAMPLES = r"""
- name: Retrieve plugin details with specific filters
  list_plugin_outputs:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    plugin_id: 123456
    filters:
      - type: port.protocol
        operator: eq
        value: tcp

- name: Get plugin details using environmental credentials
  list_plugin_outputs:
    plugin_id: 123456
"""


RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on success
  contains:
    data:
      description: The data about the plugin and its associated vulnerabilities.
      type: dict
      contains:
        info:
          description: General information about the plugin and associated vulnerabilities.
          type: dict
          contains:
            accepted_count:
              description: The number of times the vulnerability has been accepted.
              type: int
              returned: always
              sample: 0
            count:
              description: The number of vulnerabilities associated with this plugin.
              type: int
              returned: always
              sample: 1
            description:
              description: Description of the plugin.
              type: str
              returned: always
              sample: "This could be a long or short description."
            discovery:
              description: Information about when the vulnerability was first and last seen.
              type: dict
              contains:
                seen_first:
                  description: The first time the vulnerability was seen.
                  type: str
                  returned: always
                  sample: "2023-07-03T09:23:22.907Z"
                seen_last:
                  description: The last time the vulnerability was seen.
                  type: str
                  returned: always
                  sample: "2024-04-14T13:52:52.626Z"
            plugin_details:
              description: Specific details about the plugin.
              type: dict
              contains:
                family:
                  description: The family to which the plugin belongs.
                  type: str
                  returned: always
                  sample: "Red Hat Local Security Checks"
                modification_date:
                  description: The date when the plugin was last modified.
                  type: str
                  returned: always
                  sample: "2023-09-29T00:00:00Z"
                name:
                  description: Name of the plugin.
                  type: str
                  returned: always
                  sample: "RHEL 7 : httpd (RHSA-2023:1593)"
                publication_date:
                  description: The publication date of the plugin.
                  type: str
                  returned: always
                  sample: "2023-04-04T00:00:00Z"
                severity:
                  description: The severity rating of the plugin.
                  type: int
                  returned: always
                  sample: 4
                type:
                  description: The type of the plugin, e.g., local or network.
                  type: str
                  returned: always
                  sample: "local"
                version:
                  description: The version number of the plugin.
                  type: str
                  returned: always
                  sample: "1.4"
            risk_information:
              description: Detailed risk information associated with the plugin.
              type: dict
              contains:
                cvss3_base_score:
                  description: The CVSS v3 base score of the vulnerability.
                  type: str
                  returned: always
                  sample: "9.8"
                cvss3_temporal_score:
                  description: The CVSS v3 temporal score of the vulnerability.
                  type: str
                  returned: always
                  sample: "8.8"
                cvss3_temporal_vector:
                  description: The CVSS v3 temporal vector of the vulnerability.
                  type: str
                  returned: always
                  sample: "E:P/RL:O/RC:C"
                cvss3_vector:
                  description: The CVSS v3 vector of the vulnerability.
                  type: str
                  returned: always
                  sample: "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
                cvss_base_score:
                  description: The CVSS base score of the vulnerability.
                  type: str
                  returned: always
                  sample: "10.0"
                cvss_temporal_score:
                  description: The CVSS temporal score of the vulnerability.
                  type: str
                  returned: always
                  sample: "7.8"
                cvss_temporal_vector:
                  description: The CVSS temporal vector of the vulnerability.
                  type: str
                  returned: always
                  sample: "E:POC/RL:OF/RC:C"
                cvss_vector:
                  description: The CVSS vector of the vulnerability.
                  type: str
                  returned: always
                  sample: "AV:N/AC:L/Au:N/C:C/I:C/A:C"
                risk_factor:
                  description: The risk factor of the vulnerability.
                  type: str
                  returned: always
                  sample: "Critical"
                stig_severity:
                  description: The STIG severity level of the vulnerability, if applicable.
                  type: str
                  returned: when available
                  sample: null
            vulnerability_information:
              description: Additional details about the vulnerabilities found.
              type: dict
              contains:
                asset_inventory:
                  description: Indicates if the vulnerability is included in asset inventory.
                  type: bool
                  returned: always
                  sample: false
                cpe:
                  description: List of CPE entries associated with the vulnerability.
                  type: list
                  elements: str
                  returned: always
                  sample: ["cpe:/o:redhat:enterprise_linux:7"]
                default_account:
                  description: Indicates if a default account is associated with the vulnerability.
                  type: bool
                  returned: always
                  sample: false
                exploit_available:
                  description: Indicates if an exploit is available for the vulnerability.
                  type: bool
                  returned: always
                  sample: true
                exploit_frameworks:
                  description: List of exploit frameworks that apply to the vulnerability.
                  type: list
                  elements: str
                  returned: always
                  sample: []
                exploitability_ease:
                  description: A descriptive rating of how easy it is to exploit the vulnerability.
                  type: str
                  returned: always
                  sample: "Exploits are available"
                exploited_by_malware:
                  description: Indicates if the vulnerability is known to be exploited by malware.
                  type: bool
                  returned: always
                  sample: false
                exploited_by_nessus:
                  description: Indicates if Nessus has exploited the vulnerability.
                  type: bool
                  returned: always
                  sample: false
                in_the_news:
                  description: Indicates if the vulnerability has been reported in the news.
                  type: bool
                  returned: always
                  sample: false
                malware:
                  description: Indicates if malware is associated with the vulnerability.
                  type: bool
                  returned: always
                  sample: false
                patch_publication_date:
                  description: The publication date of any patches for the vulnerability.
                  type: str
                  returned: always
                  sample: "2023-04-04T00:00:00Z"
                unsupported_by_vendor:
                  description: Indicates if the vulnerability is unsupported by the vendor.
                  type: bool
                  returned: always
                  sample: false
                vulnerability_publication_date:
                  description: The publication date of the vulnerability.
                  type: str
                  returned: always
                  sample: "2023-03-07T00:00:00Z"
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
    common_spec = get_spec("access_key", "secret_key", "date_range", "filters", "filter_search_type")
    specific_spec = {
        "plugin_id": {"required": True, "type": "int"},
    }
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"workbenches/vulnerabilities/{module.params['plugin_id']}/outputs"

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
