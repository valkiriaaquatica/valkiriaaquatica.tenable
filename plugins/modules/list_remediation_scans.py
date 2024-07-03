# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_remediation_scans
short_description: List possible filters for assets
version_added: "0.0.1"
description:
  - Returns a list of remediation scans
  - Note Keep in mind potential rate limits when using this endpoint
  - Requires BASIC  [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/io-scans-remediation-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.generics
"""

EXAMPLES = r"""
- name: List all remediation scans
  list_remediation_scans:
      access_key: "{{ tenable_access_key }}"
      secret_key: "{{ tenable_secret_key }}"

- name: List all remediation scans using enviroment creds
  list_remediation_scans:
      limit: 1
      sort: asc
"""

RETURN = r"""
pagination:
  description: Pagination details for the returned results.
  returned: always
  type: dict
  contains:
    offset:
      description: The starting record of the result set.
      type: int
    total:
      description: The total number of records.
      type: int
    sort:
      description: The field and order used for sorting the results.
      type: str
    limit:
      description: The number of records retrieved.
      type: int
scans:
  description: A list of remediation scans.
  returned: always
  type: list
  elements: dict
  contains:
    type:
      description: The type of the scan.
      type: str
    uuid:
      description: The UUID of the scan.
      type: str
    permissions:
      description: The permissions for the scan.
      type: int
    enabled:
      description: Whether the scan is enabled.
      type: bool
    control:
      description: Whether the scan is under control.
      type: bool
    read:
      description: Whether the scan has been read.
      type: bool
    last_modification_date:
      description: The last modification date of the scan.
      type: int
    creation_date:
      description: The creation date of the scan.
      type: int
    status:
      description: The status of the scan.
      type: str
    shared:
      description: Whether the scan is shared.
      type: bool
    user_permissions:
      description: The user permissions for the scan.
      type: int
    schedule_uuid:
      description: The UUID of the scan schedule.
      type: str
    wizard_uuid:
      description: The UUID of the scan wizard.
      type: str
    scan_creation_date:
      description: The Unix timestamp when the remediation scan run was created.
      type: int
    owner:
      description: The owner of the scan.
      type: str
    policy_id:
      description: The policy ID of the scan.
      type: int
    id:
      description: The unique ID of the scan.
      type: int
    name:
      description: The name of the scan.
      type: str
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "limit", "offset", "sort")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scans/remediation"

    def query_params():
        return build_query_parameters(
            limit=module.params["limit"], offset=module.params["offset"], sort=module.params["sort"]
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
