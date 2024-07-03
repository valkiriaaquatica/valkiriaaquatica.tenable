# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_asset_vulnerabilities_for_plugin
short_description: Retrieves the vulnerability outputs for a plugin recorded on a specified asset.
version_added: "0.0.1"
description:
  - This module retrieves the vulnerability outputs for a plugin recorded on a specified asset.
  - Multiple filters can be applied and get full of default info rmo assets.
  - Note This endpoint is not intended for large or frequent exports of vulnerability or assets data
  - For information and best practices for retrieving vulnerability see https://developer.tenable.com/docs/retrieve-vulnerability-data-from-tenableio
  - For information and best practices for retrieving assets see https://developer.tenable.com/docs/retrieve-asset-data-from-tenableio
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - This module was made from https://developer.tenable.com/reference/workbenches-asset-vulnerability-output  docs.
options:
  asset_id:
    description:
      - The UUID of the asset for which vulnerability details are to be retrieved.
    type: str
    required: true
  plugin_id:
    description:
      - The ID of the plugin associated with the vulnerability data.
    type: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filter_search_type
"""


EXAMPLES = r"""
- name: Get details of the plugin
  list_asset_vulnerabilities_for_plugin:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_id: "123456"
    plugin_id: "987654"

- name: Get details of the plugin using filters and enviroment creds in last five days
  list_asset_vulnerabilities_for_plugin:
    asset_id: "123456"
    plugin_id: "987654"
    date_range: 5
    filters:
      - type: plugin.name
        operator: match
        value: RHEL
"""

RETURN = r"""
api_response:
  description: The API response containing a list of assets.
  returned: on success
  type: dict
  contains:
    data:
      description: A list of assets retrieved from the API.
      type: dict
      contains:
        outputs:
          description: Details of each asset including specific outputs from plugins.
          type: list
          elements: dict
          contains:
            plugin_output:
              description: Description of the output provided by the plugin for a specific asset.
              type: str
              returned: always
              sample: "Port 1111/udp was found to be open"
            states:
              description: List of states related to the asset.
              type: list
              elements: dict
              contains:
                name:
                  description: The state name indicating the current state of the asset.
                  type: str
                  returned: always
                  sample: "active"
                results:
                  description: Results associated with the state of the asset.
                  type: list
                  elements: dict
                  contains:
                    application_protocol:
                      description: The application protocol used by the asset, if any.
                      type: str
                      returned: when available
                      sample: null
                    assets:
                      description: List of assets associated with the current state.
                      type: list
                      elements: dict
                      contains:
                        first_seen:
                          description: The first time the asset was seen.
                          type: str
                          returned: always
                          sample: "date"
                        fqdn:
                          description: Fully Qualified Domain Name of the asset.
                          type: str
                          returned: always
                          sample: "fqdn"
                        hostname:
                          description: Hostname of the asset.
                          type: str
                          returned: always
                          sample: "hostname"
                        id:
                          description: Unique identifier of the asset.
                          type: int
                          returned: always
                          sample: "1123456"
                        ipv4:
                          description: IPv4 addresses associated with the asset.
                          type: str
                          returned: always
                          sample: "10.10.10.1,192.168.1.10"
                        ipv6:
                          description: IPv6 addresses associated with the asset, if any.
                          type: str
                          returned: when available
                          sample: ""
                        last_seen:
                          description: The last time the asset was seen.
                          type: str
                          returned: always
                          sample: "date"
                        netbios_name:
                          description: NetBIOS name of the asset, if available.
                          type: str
                          returned: when available
                          sample: null
                        uuid:
                          description: UUID of the asset.
                          type: str
                          returned: always
                          sample: "123456789"
                    port:
                      description: Port number associated with the asset.
                      type: int
                      returned: always
                      sample: 1194
                    severity:
                      description: Severity level of the issue found on the asset.
                      type: int
                      returned: always
                      sample: 0
                    transport_protocol:
                      description: Transport protocol used by the asset.
                      type: str
                      returned: always
                      sample: "udp"
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
        "asset_id": {"required": True, "type": "str"},
        "plugin_id": {"required": True, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"workbenches/assets/{module.params['asset_id']}/vulnerabilities/{module.params['plugin_id']}/outputs"

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
