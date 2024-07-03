# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  category_uuid:
    description:
      - The UUID of the tag category to return details for.
      - To list the t<g categories use the module list_tag_categories .
      - For more information on determining this value, see https://developer.tenable.com/docs/determine-tag-identifiers-tio
    required: true
    type: str
"""
