# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  directive:
    description:
      - Specifies the instructions you wish to send to the agents.
      - The directive object is different depending on whether you want to restart the agents or change settings for the agents.
    type: dict
    required: true
    suboptions:
      type:
        description:
          - The type of instruction to perform.
          - For restarting agents, the type is always restart.
        type: str
        required: true
        choices: ["restart", "settings"]
      options:
        description:
          - The options for the directive operation.
        type: dict
        required: true
        suboptions:
          hard:
            description:
              - Indicates whether or not to perform a hard restart.
              - A hard restart will inform the Nessus Agent to restart immediately regardless of what it is doing.
            type: bool
          idle:
            description:
              - Indicates whether or not to restart when the scanning engine is idle.
            type: bool
          settings:
            description:
              - An array of objects where each object is one individual instruction to perform.
              - For example, {"setting":"backend_log_level","value":"debug"}
            type: list
            elements: dict
            suboptions:
              setting:
                description:
                  - The setting to send to the scanner.
                type: str
                required: true
              value:
                description:
                  - The value for the setting.
                type: str
                required: true
"""
