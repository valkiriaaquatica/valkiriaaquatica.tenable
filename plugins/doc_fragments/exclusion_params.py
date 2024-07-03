# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# use in create_an_exclusion and update_an_exclusion

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  description:
    description:
      - The description of the exclusion.
    type: str
    required: false
  network_id:
    description:
      - The ID of the network object associated with scanners where Tenable Vulnerability Management applies the exclusion.
    type: str
    required: false
"""
