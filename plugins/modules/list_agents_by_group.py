# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_agents_by_group
short_description: Returns a list of agents for the specified agent group.
version_added: "0.0.1"
description:
  - This module retrieves a list of agents from Tenable.io
  - Supporting complex filtering,wilcarding, sorting, limit.
  - Module made from https://developer.tenable.com/reference/agent-group-list-agents docs.
  - Requires SCAN MANAGER  [40] user permissions as specified in the Tenable.io API documentation.
options:
  agent_group_id:
    description:
      - The id of the agent group.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.filters
  - valkiriaaquatica.tenable.generics
  - valkiriaaquatica.tenable.filters_wildcards
  - valkiriaaquatica.tenable.filter_type
"""

EXAMPLES = r"""
- name: List agents by group wiht enviroment creentials
  list_agents_by_group:
    agent_group_id: 123456
    filters:
      - type: core_version
        operator: match
        value: "10.6.2"

- name: List agents by group with variables
  list_agents_by_group:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    agent_group_id: 123456

- name: List agents by group with variables
  list_agents_by_group:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    agent_group_id: 123456
    wildcard_text: bastion
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  returned: on success
  type: dict
  contains:
    data:
      description: Contains detailed information about the agents and pagination.
      type: dict
      contains:
        agents:
          description: A list of agents that are in the group.
          type: list
          elements: dict
          contains:
            aws_account_id:
              description: AWS account identifier associated with the agent.
              type: str
              returned: when available
              sample: "12345"
            aws_instance_id:
              description: AWS instance identifier for the agent.
              type: str
              returned: when available
              sample: "i-12345"
            aws_public_hostname:
              description: Public AWS hostname associated with the agent.
              type: str
              returned: when available
              sample: "HOSTNAME"
            aws_public_ipv4:
              description: Public IPv4 address of the agent in AWS.
              type: str
              returned: when available
              sample: "1.1.1.1"
            core_build:
              description: Core build version of the agent.
              type: str
              returned: when available
              sample: "1"
            core_version:
              description: Core version of the agent.
              type: str
              returned: when available
              sample: "1.1.1"
            distro:
              description: Distribution information of the agent operating system.
              type: str
              returned: when available
              sample: "win-x86-64"
            groups:
              description: List of groups the agent belongs to.
              type: list
              elements: dict
              contains:
                id:
                  description: Unique identifier for the group.
                  type: int
                  returned: always
                  sample: 1111
                name:
                  description: Name of the group.
                  type: str
                  returned: always
                  sample: "group1"
            id:
              description: Unique identifier of the agent.
              type: int
              returned: always
              sample: 123466
            ip:
              description: IP address of the agent.
              type: str
              returned: always
              sample: "172.31.34.199"
            last_connect:
              description: Timestamp of the last time the agent connected to the network.
              type: int
              returned: when available
              sample: 1111
            last_scanned:
              description: Timestamp of the last scan performed by the agent.
              type: int
              returned: when available
              sample: 1111
            linked_on:
              description: Timestamp when the agent was linked to the network.
              type: int
              returned: when available
              sample: 1111
            name:
              description: Name of the agent.
              type: str
              returned: always
              sample: "name"
            network_uuid:
              description: Network UUID associated with the agent.
              type: str
              returned: when available
              sample: "1111"
            platform:
              description: Platform of the agent.
              type: str
              returned: always
              sample: "WINDOWS"
            plugin_feed_id:
              description: Plugin feed ID associated with the agent.
              type: str
              returned: when available
              sample: "1111"
            status:
              description: Current status of the agent.
              type: str
              returned: always
              sample: "off"
            supports_remote_logs:
              description: Indicates if the agent supports remote logs.
              type: bool
              returned: always
              sample: false
            supports_remote_settings:
              description: Indicates if the agent supports remote settings.
              type: bool
              returned: always
              sample: true
            uuid:
              description: UUID of the agent.
              type: str
              returned: always
              sample: "1111"
        pagination:
          description: Pagination details of the response.
          type: dict
          contains:
            limit:
              description: The maximum number of records returned in the response.
              type: int
              returned: always
              sample: 1
            offset:
              description: The starting point from which records are returned.
              type: int
              returned: always
              sample: 0
            sort:
              description: List of sort conditions applied to the response.
              type: list
              elements: dict
              contains:
                name:
                  description: Name of the field by which the results are sorted.
                  type: str
                  returned: always
                  sample: "name"
                order:
                  description: Order of sorting, ascending or descending.
                  type: str
                  returned: always
                  sample: "asc"
            total:
              description: Total number of items available.
              type: int
              returned: always
              sample: 163
    status_code:
      description: HTTP status code returned by the API.
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
    common_spec = get_spec(
        "access_key",
        "secret_key",
        "filters",
        "filter_type",
        "wildcard_text",
        "wildcard_fields",
        "limit",
        "offset",
        "sort",
    )
    special_args = {
        "agent_group_id": {
            "required": True,
            "type": "str",
        },
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agent-groups/{module.params['agent_group_id']}/agents"

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
