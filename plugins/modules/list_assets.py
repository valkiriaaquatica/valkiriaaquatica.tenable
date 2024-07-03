# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_assets
short_description: Retrieve a filtered list of assets from Tenable.io
version_added: "0.0.1"
description:
  - This module retrieves a filtered list of assets from Tenable.io.
  - Multiple filters can be applied and get full of default info rmo assets.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - This module was made from https://developer.tenable.com/reference/workbenches-assets docs.
options:
  all_fields:
    description:
      - Specifies whether to include all fields ('full') or only the default fields ('default') in the returned data.
    type: str
    required: false
    choices: ['full', 'default']
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.date
  - valkiriaaquatica.tenable.filter_search_type
"""

EXAMPLES = r"""
- name: Get Assets based on thei size
  list_assets:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filters:
      - type: "aws_ec2_instance_type"
        operator: "eq"
        value: "t2.micro"

- name: Get Aall assets from all networks except one
  list_assets:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filters:
      - type: network_id
        operator: neq
        value: 123456

- name: Get all assets from two networks
  list_assets:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filter_search_type: or
    filters:
      - type: network_id
        operator: eq
        value: 123456
      - type: network_id
        operator: eq
        value: 5678

- name: Get an asset from aws instance id
  list_assets:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filters:
      - type: aws_ec2_instance_id
        operator: eq
        value: i-123456789

- name: List assets from a network_id using eniroment creds
  list_assets:
    filters:
      - type: network_id
        operator: eq
        value: 123456

- name: List assets from a network_id using eniroment creds and getting full data
  list_assets:
    filters:
      - type: network_id
        operator: eq
        value: 123456
      - type: fqdn
        operator: eq
        value: "i123451795"
    all_fields: full
"""

RETURN = r"""
api_response:
  description: The API response containing a list of assets.
  type: dict
  returned: on success
  contains:
    data:
      description: A list of assets retrieved from the API.
      type: dict
      returned: always
      contains:
        assets:
          description: Details of each asset.
          type: list
          elements: dict
          returned: always
          contains:
            acr_drivers:
              description: Indicates the ACR drivers associated with the asset, if applicable.
              type: str
              returned: always
              sample: null
            acr_score:
              description: The ACR score of the asset, if applicable.
              type: int
              returned: always
              sample: null
            agent_name:
              description: List of agent names associated with the asset.
              type: list
              elements: str
              returned: always
              sample: []
            aws_ec2_name:
              description: List of AWS EC2 names associated with the asset, if applicable.
              type: list
              elements: str
              returned: always
              sample: ["aws_iam_name"]
            exposure_confidence_value:
              description: The confidence value of the exposure assessment, if applicable.
              type: str
              returned: always
              sample: null
            exposure_score:
              description: The score of the exposure assessment, if applicable.
              type: str
              returned: always
              sample: null
            fqdn:
              description: List of fully qualified domain names associated with the asset.
              type: list
              elements: str
              returned: always
              sample: ["111l"]
            has_agent:
              description: Indicates whether the asset has an associated agent.
              type: bool
              returned: always
              sample: true
            hostname:
              description: List of hostnames associated with the asset.
              type: list
              elements: str
              returned: always
              sample: ["iam_hostname"]
            id:
              description: Unique identifier of the asset.
              type: str
              returned: always
              sample: "fe56ee29-0213-11"
            ipv4:
              description: List of IPv4 addresses associated with the asset.
              type: list
              elements: str
              returned: always
              sample: ["222"]
            ipv6:
              description: List of IPv6 addresses associated with the asset.
              type: list
              elements: str
              returned: always
              sample: []
            last_scan_target:
              description: The target of the last scan performed on the asset, if applicable.
              type: str
              returned: always
              sample: null
            last_seen:
              description: The last time the asset was seen by str monitoring systems.
              type: str
              returned: always
              sample: "2023-06-26T16:51:34.609Z"
            mac_address:
              description: List of MAC addresses associated with the asset.
              type: list
              elements: str
              returned: always
              sample: ["mac"]
            netbios_name:
              description: List of NetBIOS names associated with the asset.
              type: list
              elements: str
              returned: always
              sample: ["iam_netbios_name"]
            operating_system:
              description: List of operating systems running on the asset.
              type: list
              elements: str
              returned: always
              sample: ["Red Hat Enterprise Linux 8.6"]
            scan_frequency:
              description: The frequency at which the asset is scanned, if regularly scheduled.
              type: str
              returned: always
              sample: null
            security_protection_level:
              description: The level of security protection assigned to the asset, if applicable.
              type: str
              returned: always
              sample: null
            security_protections:
              description: List of security protections applied to the asset.
              type: list
              elements: str
              returned: always
              sample: []
            sources:
              description: Sources that have reported data about the asset.
              type: list
              elements: dict
              returned: always
              contains:
                first_seen:
                  description: The first time this source reported data about the asset.
                  type: str
                  returned: always
                  sample: "2023-06-15T12:36:18.502Z"
                last_seen:
                  description: The last time this source reported data about the asset.
                  type: str
                  returned: always
                  sample: "2023-06-26T16:51:34.609Z"
                name:
                  description: Name of the source reporting the data.
                  type: str
                  returned: always
                  sample: "AWS"
        total:
          description: The total number of assets returned.
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
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "date_range", "filters", "filter_search_type", "all_fields")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "workbenches/assets"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                date_range=module.params["date_range"],
                filter_search_type=module.params["filter_search_type"],
                all_fields=module.params["all_fields"],
            ),
            module.params["filters"],
            handle_multiple_filters,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
