# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_agent_group_details
short_description: Gets details for the agent group. Returns a list of agents
version_added: "0.0.1"
description:
  - This module retrieves a list of agents from a group and group information.
  - Supporting complex filtering,wilcarding, sorting, limit.
  - Module made from https://developer.tenable.com/reference/agent-groups-details docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.filter_type
  - valkiriaaquatica.tenable.filters_wildcards
  - valkiriaaquatica.tenable.generics
"""


EXAMPLES = r"""
- name: Get agents from group using enviroment creds
  get_agent_group_details:
    group_id: 123456

- name: Get agents from grup 123456
  get_agent_group_details:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: 123456

- name: Get agents from group 123456 that in any of the values contain jenkins
  get_agent_group_details:
    group_id: 123456
    wildcard_text: jenkins

- name: Get agents from group that in any of the fields contain git or jenkins limiting 2 agents
  get_agent_group_details:
    group_id: 123456
    wildcard_text: jenkins, git
    limit: 2

- name: Get agents from group 123456 and filtering just the Linux
  get_agent_group_details:
    group_id: 123456
    filters:
      - type: platform
        operator: eq
        value: LINUX
"""

RETURN = r"""
api_response:
  description: Detailed information about the network.
  type: dict
  returned: on success
  contains:
    data:
      description: Detailed data about the machine including its network settings and specific attributes.
      type: dict
      returned: always
      sample:
        id: 1234567
        uuid: "the_uuid"
        name: "name_machine"
        platform: "WINDOWS"
        distro: "win-x86-64"
        ip: "10.55.0.254"
        last_scanned: 123456789
        plugin_feed_id: "202312010556"
        core_build: "7"
        core_version: "10.4.4"
        linked_on: 123456789
        last_connect: 123456789
        status: "off"
        aws_instance_id: "i-123456"
        aws_account_id: "123456789"
        supports_remote_logs: false
        network_uuid: "the_network_uuid"
        network_name: "the_network_name"
        remote_settings:
          - name: "Minimum Health Update Interval"
            setting: "min_agent_health_update_interval"
            type: "integer"
            description: "Specifies, in minutes, the minimum interval to update health events"
            min: 60
            status: "current"
            value: "60"
            default: "60"
        supports_remote_settings: true
        restart_pending: false
        health_events: []
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_special_filter
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec(
        "access_key",
        "secret_key",
        "group_id",
        "filters",
        "filter_type",
        "limit",
        "offset",
        "sort",
        "wildcard_text",
        "wildcard_fields",
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    group_id = module.params["group_id"]
    endpoint = f"scanners/null/agent-groups/{group_id}"

    def query_params():
        return add_custom_filters(
            build_query_parameters(
                filter_type=module.params["filter_type"],
                wildcard_text=module.params["wildcard_text"],
                wildcard_fields=module.params["wildcard_fields"],
                limit=module.params["limit"],
                offset=module.params["offset"],
                sort=module.params["sort"],
            ),
            module.params["filters"],
            handle_special_filter,
        )

    run_module(module, endpoint, query_params_func=query_params, method="GET")


if __name__ == "__main__":
    main()
