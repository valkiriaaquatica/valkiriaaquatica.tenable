# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  criteria:
    description:
      - Specifies the criteria you wish to filter agents on.
      - The criteria is used to narrow down the list of agents to perform the specified action on.
    type: dict
    required: false
    suboptions:
      all_agents:
        description:
          - Indicates whether or not to match against all agents.
        type: bool
      wildcard:
        description:
          - A string used to match against all string-like attributes of an agent.
        type: str
      filters:
        description:
          - An array of string or numeric operations to match against agents. For example, name:match:laptop or core_version:lt:10.0.0.
        type: list
        elements: str
      filter_type:
        description:
          - Indicates how to combine the filters conditions. Possible values are and or or.
        type: str
        choices: ["and", "or"]
      hardcoded_filters:
        description:
          - Additional filters that will always be added as and conditions.
        type: list
        elements: str
  items:
    description:
      - An array of agent IDs or agent UUIDs to add to the criteria filter.
    type: list
    elements: str
    required: false
  not_items:
    description:
      - An array of agent IDs or agent UUIDs to exclude from the criteria filter.
    type: list
    elements: str
    required: false
"""
