# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_asset_details
short_description: Retrieve detailed information of a asset using its asset_uuid.
version_added: "0.0.1"
description:
  - This module fetches detailed information about a specific asset.
  - The module is made from https://developer.tenable.com/reference/assets-asset-info docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
"""

EXAMPLES = r"""
- name: Get information of a asset
  get_asset_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    asset_uuid: 11111

- name: Get information of a asset using enviroment keys
  get_asset_details:
    asset_uuid: 11111
"""

RETURN = r"""
api_response:
  description: Detailed information about the asset.
  type: dict
  returned: always
  contains:
    data:
      description: Includes comprehensive details about the asset, such as identification, status, and network information.
      type: dict
      returned: always
      sample:
        id: "123456789"
        has_agent: true
        created_at: "2021-02-08T09:42:51.056Z"
        updated_at: "2021-02-23T22:23:52.005Z"
        terminated_at: null
        deleted_at: null
        first_seen: "2021-04-08T09:42:47.910Z"
        last_seen: "2021-04-23T22:23:49.000Z"
        last_scan_target: "192.168.1.11"
        last_authenticated_scan_date: "2021-04-10T18:11:01.849Z"
        last_licensed_scan_date: "2021-04-10T18:11:01.849Z"
        last_scan_id: null
        last_schedule_id: null
        sources:
          - name: "NESSUS_AGENT"
            first_seen: "2021-04-08T09:42:47.910Z"
            last_seen: "2021-04-23T09:48:44.998Z"
          - name: "CloudDiscoveryConnector"
            first_seen: "2021-04-08T11:10:16.000Z"
            last_seen: "2021-04-23T22:23:49.000Z"
        tags:
          - tag_uuid: "thae_tag_uid_value"
            tag_key: "Department"
            tag_value: "Finance"
            added_by: null
            added_at: null
          - tag_uuid: "thae_tag_uid_value"
            tag_key: "Unavailable"
            tag_value: "Unavailable"
            added_by: null
            added_at: null
        acr_score: 4
        acr_drivers: null
        exposure_score: 600
        scan_frequency: null
        interfaces:
          - ipv4: ["192.168.1.11"]
            ipv6: []
            fqdn: ["i_am_fdqn"]
            mac_address: ["i_am_mac_addres"]
            name: "UNKNOWN"
            virtual: null
            aliased: null
        network_id: ["i_am_network_id"]
        ipv4: ["10.55.0.219"]
        ipv6: []
        fqdn: ["i_am_fdqn"]
        mac_address: ["i_am_mac_addres"]
        netbios_name: []
        operating_system: ["Linux"]
        system_type: []
        tenable_uuid: ["i_am_tenable_uuid"]
        hostname: ["i_am_hostname"]
        agent_name: ["i_am_name"]
        bios_uuid: []
        aws_ec2_instance_id: ["i-123456789"]
        aws_ec2_instance_ami_id: ["ami-123456789"]
        aws_owner_id: ["123456789"]
        aws_availability_zone: ["eu-west-1b"]
        aws_region: ["eu-west-1"]
        aws_vpc_id: ["i_am_aws_vpc_id"]
        aws_ec2_instance_group_name: ["i_am_aws_ec2_instance_group_name"]
        aws_ec2_instance_state_name: ["stopped"]
        aws_ec2_instance_type: ["t2.micro"]
        aws_subnet_id: ["subnet-02e977eb39cee9a25"]
        aws_ec2_product_code: []
        aws_ec2_name: ["i_am_name"]
        azure_vm_id: []
        azure_resource_id: []
        azure_subscription_id: []
        azure_resource_group: []
        azure_location: []
        azure_type: []
        gcp_project_id: []
        gcp_zone: []
        gcp_instance_id: []
        ssh_fingerprint: []
        mcafee_epo_guid: []
        mcafee_epo_agent_guid: []
        qualys_asset_id: []
        qualys_host_id: []
        servicenow_sysid: []
        installed_software: ["cpe:/a:amazon:amazon_ssm_agent:3.2.2303.0", "cpe:/a:java:jre:1.21.0_2"]
        bigfix_asset_id: []
        security_protection_level: null
        security_protections: []
        exposure_confidence_value: null
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    run_module(module, "assets", module.params["asset_uuid"], method="GET")


if __name__ == "__main__":
    main()
