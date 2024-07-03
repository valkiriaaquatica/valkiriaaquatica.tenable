# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_agents
short_description: Returns a list of agents for the specified scanner.
version_added: "0.0.1"
description:
  - This module returns a list of agents for the specified scanner.
  - Supporting complex filtering,wilcarding, sorting, limit.
  - Module made from https://developer.tenable.com/reference/agents-list docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
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
- name: List agents that
  list_agents:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    filters:
      - type: platform
        operator: eq
        value: LINUX

- name: List agents that contain test in its name using enviroment cred
  list_agents:
    wildcard_text: test
    wildcard_fields: name

- name: List all agents using enviroment credentials
  list_agents:


- name: List all agents
  list_agents:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"

- name: List all agents that in their ip and name contain 192.168.
  list_agents:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    wildcard_text: 192.168.
    wildcard_fields: ip,name

- name: List agents with specified filters and wildcard using env variables
  list_agents:
    wildcard_text: POLLER
    wildcard_fields: name
    filters:
      - type: core_version
        operator: match
        value: 10.4.4
      - type: platform
        operator: eq
        value: LINUX
      - type: groups
        operator: eq
        value: 127110
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  returned: on success
  type: dict
  contains:
    data:
      description: Contains detailed information about agents and pagination settings.
      type: dict
      contains:
        agents:
          description: A list of agent details retrieved from the API.
          type: list
          elements: dict
          contains:
            aws_account_id:
              description: AWS account identifier associated with the agent.
              type: str
              returned: when available
              sample: "12334"
            aws_instance_id:
              description: AWS instance identifier for the agent.
              type: str
              returned: when available
              sample: "i-5445545d452"
            core_build:
              description: Core build version of the agent.
              type: str
              returned: when available
              sample: "10"
            core_version:
              description: Core version of the agent.
              type: str
              returned: when available
              sample: "10.6.2"
            distro:
              description: Distribution information of the agent's operating system.
              type: str
              returned: when available
              sample: "es7-x86-64"
            groups:
              description: List of groups the agent belongs to.
              type: list
              elements: dict
              contains:
                id:
                  description: Unique identifier for the group.
                  type: int
                  returned: always
                  sample: 123456
                name:
                  description: Name of the group.
                  type: str
                  returned: always
                  sample: "name"
            id:
              description: Unique identifier of the agent.
              type: int
              returned: always
              sample: 12652464
            ip:
              description: IP address of the agent.
              type: str
              returned: always
              sample: "192.168.1.120"
            last_connect:
              description: Timestamp of the last time the agent connected.
              type: int
              returned: when available
              sample: 1713870756
            last_scanned:
              description: Timestamp of the last scan performed by the agent.
              type: int
              returned: when available
              sample: 1713769041
            linked_on:
              description: Timestamp when the agent was linked to the network.
              type: int
              returned: when available
              sample: 1708585081
            name:
              description: Name of the agent.
              type: str
              returned: always
              sample: "poller"
            network_name:
              description: Name of the network the agent is associated with.
              type: str
              returned: when available
              sample: "AWS_ADA"
            network_uuid:
              description: UUID of the network the agent is associated with.
              type: str
              returned: when available
              sample: "12345"
            platform:
              description: Platform of the agent.
              type: str
              returned: always
              sample: "LINUX"
            plugin_feed_id:
              description: Plugin feed ID associated with the agent.
              type: str
              returned: when available
              sample: "202404230143"
            status:
              description: Current status of the agent.
              type: str
              returned: always
              sample: "on"
            supports_remote_logs:
              description: Indicates if the agent supports remote logs.
              type: bool
              returned: always
              sample: true
            supports_remote_settings:
              description: Indicates if the agent supports remote settings.
              type: bool
              returned: always
              sample: true
            uuid:
              description: UUID of the agent.
              type: str
              returned: always
              sample: "545621-545g-51564fr-5645"
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
    module = AnsibleModule(argument_spec=common_spec, supports_check_mode=False)

    endpoint = "scanners/null/agents"

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
