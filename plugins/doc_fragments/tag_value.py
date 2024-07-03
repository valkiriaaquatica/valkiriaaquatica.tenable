# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  value_uuid:
    description:
      - The UUID of the tag value you want to delete.
      - Changed the original Tenable interface name value_uuid to tag_value_uuid.
      - Use the list_tag_values to get the id of the tag.
      - For more information on determining this value, see https://developer.tenable.com/docs/determine-tag-identifiers-tio
    required: true
    type: str
"""
