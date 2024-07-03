# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_asset_information
short_description: Returns information about the specified asset.
version_added: "0.0.1"
description:
  - This module returns information about the specified asset.
  - Note This endpoint is not intended for large or frequent exports of vulnerability or assets data
  - If you experience errors, reduce the volume, rate, or concurrency of your requests or narrow your filters.
  - For information and best practices for retrieving assets see https://developer.tenable.com/docs/retrieve-asset-data-from-tenableio
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - The module is made from https://developer.tenable.com/reference/workbenches-asset-info docs.
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
  - valkiriaaquatica.tenable.asset
"""

EXAMPLES = r"""
- name: Get asset information
  get_asset_information:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_id: "123456"

- name: Get full asset information using enviroment creds
  get_asset_information:
    asset_id: "123456"
    all_fields: full
"""

RETURN = r"""
api_response:
  description: Detailed information about the asset.
  type: dict
  returned: on success
  contains:
    data:
      description: Includes comprehensive details about the asset including identification, security, and network information.
      type: dict
      returned: on success
      sample:
        acr_drivers: []
        acr_score: null
        agent_name: ["agent_name"]
        aws_availability_zone: ["eu-west-1a"]
        aws_ec2_instance_ami_id: ["ami-123456"]
        aws_ec2_instance_group_name: ["group_name"]
        aws_ec2_instance_id: ["i-123456"]
        aws_ec2_instance_state_name: ["running"]
        aws_ec2_instance_type: ["t2.small"]
        aws_ec2_name: ["aws_ec2_name"]
        aws_ec2_product_code: []
        aws_owner_id: ["123456789"]
        aws_region: ["eu-west-1"]
        aws_subnet_id: ["subnet-123456789"]
        aws_vpc_id: ["vpc-123456789"]
        azure_location: []
        azure_resource_group: []
        azure_resource_id: []
        azure_subscription_id: []
        azure_type: []
        azure_vm_id: []
        bigfix_asset_id: []
        bios_uuid: []
        counts:
          audits:
            statuses: [{"count": 0, "level": 1, "name": "Passed"}]
            total: 0
          vulnerabilities:
            severities: [{"count": 0, "level": 1, "name": "Low"}]
            total: 68
        created_at: "date"
        deleted_at: null
        exposure_confidence_value: 0
        exposure_score: null
        first_seen: "date"
        fqdn: ["fqdn_1", "fqdn_2"]
        gcp_instance_id: []
        gcp_project_id: []
        gcp_zone: []
        has_agent: true
        hostname: ["hostname"]
        id: "123456789"
        installed_software: ["cpe:/a:gnupg:libgcrypt:1.9.4"]
        interfaces:
          - fqdn: ["fqdn_1", "fqdn_2"]
            ipv4: ["192.168.1.10", "10.10.10.15"]
            ipv6: []
            mac_address: ["mac_address"]
            name: "UNKNOWN"
        ipv4: ["192.168.1.10", "10.10.10.15"]
        ipv6: []
        last_authenticated_scan_date: "date"
        last_licensed_scan_date: "date"
        last_scan_id: null
        last_scan_target: "192.168.1.20"
        last_schedule_id: null
        last_seen: "date"
        mac_address: ["mac_address"]
        mcafee_epo_agent_guid: []
        mcafee_epo_guid: []
        netbios_name: []
        network_name: "network_name"
        operating_system: ["Linux"]
        qualys_asset_id: []
        qualys_host_id: []
        scan_frequency: []
        security_protection_level: null
        security_protections: []
        servicenow_sysid: []
        sources:
          - first_seen: "date"
            last_seen: "date"
            name: "NESSUS_AGENT"
          - first_seen: "date"
            last_seen: "date"
            name: "AWS"
          - first_seen: "date"
            last_seen: "date"
            name: "name"
        ssh_fingerprint: []
        system_type: ["x86_64"]
        tags:
          - added_at: "date"
            source: "dynamic"
            tag_key: "Cloud Provider"
            tag_uuid: "123456"
            tag_value: "AWS"
          - added_at: "date"
            source: "dynamic"
            tag_key: "Department"
            tag_uuid: "123456"
            tag_value: "tag_value"
          - added_at: "date"
            added_by: "123456"
            source: "static"
            tag_key: "Project"
            tag_uuid: "123456"
            tag_value: "name"
        tenable_uuid: ["123456789"]
        time_end: null
        time_start: "date"
        updated_at: "date"
        uuid: "123456"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid", "all_fields")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"workbenches/assets/{module.params['asset_id']}/info"

    def query_params():
        return build_query_parameters(all_fields=module.params["all_fields"])

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
