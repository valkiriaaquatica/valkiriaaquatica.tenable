# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: list_plugins
short_description: Lists plugins in Tenable.io.
version_added: "0.0.1"
description:
  - This module retrieves a list of plugin from Tenable.io
  - Supporting complex filtering, sorting, pagination, and the option to include deleted plugin objects.
  - Module made from https://developer.tenable.com/reference/was-v2-plugins-list docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  last_updated:
    description:
     - The last updated date to filter on in the YYYY-MM-DD format.
     - Tenable Vulnerability Management returns only the plugins that have been updated after the specified date.
     - His parameter does not take VPR updates into account.
     - If you need to filter the plugin list by VPR update date, you should use a last_updated
     - Date of 1970-01-01 to return all plugins, and then filter the result set manually based on the updated field in the vpr object.
    required: false
    type: str
  size:
    description:
      - The number of records to include in the result set
      - Default is 1000. The maximum size is 10000.
    required: false
    type: int
  page:
    description:
      - The index of the page to return relative to the specified page size
      - For example, to return records 10-19 with page size 10, you must specify page 2. If you omit this parameter.
      - Tenable Vulnerability Management applies the default value of 1.
    required: false
    type: int
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all plugins passing credentials to the module
  list_plugins:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"

- name: List one plugin record with enviroment credentials
  list_plugins:
    size: 1

- name: List four record plugins specifying page using enviorent credentials
  list_plugins:
    size: 4
    page: 3
- name: List plugins filtering by last update date and passing credentials.
  list_plugins:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    last_updated: 2023-01-01

- name: Use the three filters
  list_plugins:
    last_updated: 2024-01-01
    size: 1
    page: 1
  register: plugins
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about plugins.
      type: dict
      contains:
        plugin_details:
          description: A list of detailed plugin attributes.
          type: list
          elements: dict
          contains:
            attributes:
              description: Attributes associated with each plugin.
              type: dict
              contains:
                always_run:
                  description: Indicates if the plugin always runs regardless of the scan configuration.
                  type: bool
                  returned: always
                  sample: false
                bid:
                  description: List of Bugtraq IDs associated with the plugin.
                  type: list
                  elements: str
                  returned: always
                  sample: []
                compliance:
                  description: Indicates if the plugin is used for compliance checks.
                  type: bool
                  returned: always
                  sample: false
                cve:
                  description: List of CVE identifiers related to the plugin.
                  type: list
                  elements: str
                  returned: always
                  sample: []
                cvss_base_score:
                  description: CVSS base score of the vulnerabilities detected by the plugin.
                  type: float
                  returned: always
                  sample: 10
                cvss_vector:
                  description: Detailed CVSS vector information.
                  type: dict
                  contains:
                    AccessComplexity:
                      description: The complexity required for exploiting the vulnerability found.
                      type: str
                      returned: always
                      sample: "Low"
                    AccessVector:
                      description: Network access vector through which the vulnerability can be exploited.
                      type: str
                      returned: always
                      sample: "plugin"
                    Authentication:
                      description: Type of authentication needed to exploit the vulnerability.
                      type: str
                      returned: always
                      sample: "None required"
                    AvailabilityImpact:
                      description: The impact on availability due to the vulnerability.
                      type: str
                      returned: always
                      sample: "Complete"
                    ConfidentialityImpact:
                      description: The impact on confidentiality due to the vulnerability.
                      type: str
                      returned: always
                      sample: "Complete"
                    IntegrityImpact:
                      description: The impact on integrity due to the vulnerability.
                      type: str
                      returned: always
                      sample: "Complete"
                    raw:
                      description: The raw CVSS vector string.
                      type: str
                      returned: always
                      sample: "AV:N/AC:L/Au:N/C:C/I:C/A:C"
                description:
                  description: Description of the plugin.
                  type: str
                  returned: always
                  sample: "This is a description."
                exploit_available:
                  description: Indicates if an exploit is available for the vulnerabilities detected by the plugin.
                  type: bool
                  returned: always
                  sample: false
                has_patch:
                  description: Indicates if a patch is available for the vulnerabilities detected by the plugin.
                  type: bool
                  returned: always
                  sample: false
                intel_type:
                  description: Type of intelligence provided by the plugin, e.g., SENSOR.
                  type: str
                  returned: always
                  sample: "SENSOR"
                plugin_modification_date:
                  description: Date when the plugin was last modified.
                  type: str
                  returned: always
                  sample: "2008-04-23T00:00:00Z"
                plugin_publication_date:
                  description: Date when the plugin was published.
                  type: str
                  returned: always
                  sample: "1999-07-29T00:00:00Z"
                plugin_type:
                  description: Type of the plugin, e.g., REMOTE.
                  type: str
                  returned: always
                  sample: "REMOTE"
                plugin_version:
                  description: Version number of the plugin.
                  type: float
                  returned: always
                  sample: 1.36
                potential_vulnerability:
                  description: Indicates if the plugin potentially identifies vulnerabilities.
                  type: bool
                  returned: always
                  sample: true
                risk_factor:
                  description: Risk factor as determined by the plugin.
                  type: str
                  returned: always
                  sample: "CRITICAL"
                see_also:
                  description: List of URLs or references for more information.
                  type: list
                  elements: str
                  returned: always
                  sample: []
                solution:
                  description: Recommended solution or mitigation steps provided by the plugin.
                  type: str
                  returned: always
                  sample: "I am the solution."
                synopsis:
                  description: Brief synopsis provided by the plugin.
                  type: str
                  returned: always
                  sample: "I am the synopsis."
                vpr:
                  description: Vulnerability Priority Rating information if available.
                  type: dict
                  returned: when available
                xref:
                  description: Cross-references to other security documentation.
                  type: list
                  elements: str
                  returned: always
                  sample: []
                xrefs:
                  description: Extended references, similar to xref.
                  type: list
                  elements: str
                  returned: always
                  sample: []
            id:
              description: Unique identifier for the plugin.
              type: int
              returned: always
              sample: 10024
            name:
              description: Name of the plugin.
              type: str
              returned: always
              sample: "BackOrifice Software Detection"
        params:
          description: Parameters associated with the request or the response.
          type: dict
          contains:
            last_updated:
              description: Date when the data was last updated.
              type: str
              returned: always
              sample: "2024-01-01"
            page:
              description: Page number of the response data.
              type: int
              returned: always
              sample: 1
            size:
              description: Number of items per page in the response.
              type: int
              returned: always
              sample: 1
        size:
          description: The size of the data returned.
          type: int
          returned: always
          sample: 1
        total_count:
          description: Total number of items available in the database.
          type: int
          returned: always
          sample: 26385
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    # last_updated is unique in this module
    # size is unique for this module
    # page is unique for this module
    common_spec = get_spec("access_key", "secret_key", "last_updated", "size", "page")

    module = AnsibleModule(argument_spec=common_spec, supports_check_mode=False)

    def query_params():
        return build_query_parameters(
            last_updated=module.params["last_updated"], size=module.params["size"], page=module.params["page"]
        )

    endpoint = "plugins/plugin"
    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
