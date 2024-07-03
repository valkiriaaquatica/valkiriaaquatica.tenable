# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_asset_activity_log
short_description: Returns the activity log for the specified asset
version_added: "0.0.1"
description:
  - "This module returns the activity log for the specified asset."
  - "Event types include the following:"
  - "Discovered—Asset created (for example, by a network scan or import)."
  - "Seen—Asset observed by a network scan without any changes to its attributes."
  - "Tagging—Tag added to or removed from asset."
  - "Attribute_change—A scan identified new or changed attributes for the asset (for example, new software applications installed on the asset)."
  - "Updated—Asset updated either manually by a user or automatically by a new scan."
  - "Note: This endpoint is not intended for large or frequent exports of vulnerability or assets data."
  - "Tenable recommends the export_vulnerabilities module or https://developer.tenable.com/reference/exports-vulns-request-export for large amount."
  - "For information and best practices for retrieving vulnerability see https://developer.tenable.com/docs/retrieve-vulnerability-data-from-tenableio."
  - "For information and best practices for retrieving assets see https://developer.tenable.com/docs/retrieve-asset-data-from-tenableio."
  - "Module made from https://developer.tenable.com/reference/workbenches-assets-activitydocs."
  - "Requires BASIC [16] user permissions as specified in the Tenable.io API documentation."
author:
  - "Fernando Mendieta Ovejero (@valkiriaaquatica)"
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.asset
"""


EXAMPLES = r"""
- name: Get asset activity log
  get_asset_activity_log:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    asset_uuid: "123456"

- name: Get asset activity log using enviroment creds
  get_asset_activity_log:
    asset_uuid: "123456"
"""

RETURN = r"""
api_response:
  description: Detailed information about the asset.
  type: dict
  returned: always
  contains:
    data:
      description: Includes detailed activity data and match information for the asset.
      type: dict
      returned: always
      sample:
        activity:
          - type: "seen"
            timestamp: "date"
            source: "discovery"
            updates: []
            acceptedMatch:
              matchingProperty:
                propertyName: "aws_ec2_instance_id"
                propertyValue: "i-123456"
        updatedAt: "date"
        rejectedMatch:
          assetUuid: "123456"
          contradictingProperty:
            propertyName: "aws_ec2_instance_id"
            propertyValue:
              - "i-123456"
            contradictingValue:
              - "i-123456"
          matchingProperty:
            propertyName: "fqdn"
            propertyValue: "123456"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "asset_uuid")
    argument_spec["asset_uuid"]["required"] = True
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"workbenches/assets/{module.params['asset_uuid']}/activity"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
