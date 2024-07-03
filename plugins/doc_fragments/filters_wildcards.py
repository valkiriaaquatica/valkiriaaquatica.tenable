# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  wildcard_text:
    description:
      - Wildcard text to be used in wildcard search across specified fields.
      - It refers to w key in the docs https://developer.tenable.com/reference/agent-group-list-agents
    type: str
    required: false
  wildcard_fields:
    description:
      - Comma-delimited fields to apply the wildcard text.
      - It refers to wf in the docs https://developer.tenable.com/reference/agent-group-list-agents.
      - If omitted, all wildcard_fields are searched.
    type: list
    elements: str
    required: false

"""
