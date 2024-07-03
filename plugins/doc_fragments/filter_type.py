# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  filter_type:
    description:
      - Determines if the filters should match all ('and') or any ('or') conditions.
      - It is the ft value that can be check here https://developer.tenable.com/reference/agent-group-list-agents.
    type: str
    choices: ['and', 'or']
    required: false
"""
