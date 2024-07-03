# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  filter_search_type:
    description:
      - Specifies whether to use the 'AND' or 'OR' logical operator for multiple filters.
      - Default is 'AND'.
    type: str
    required: false
    choices: ['and', 'or']
"""
