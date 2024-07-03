# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  value:
    description:
      - The new tag value.
      - Cannot exceed 50 characters in length and must not contain commas.
    type: str
    required: false
  description:
    description:
      - Description of the new tag value.
    type: str
    required: false
  access_control:
    description:
      - Defines access control settings for the tag value.
    type: dict
    suboptions:
      current_user_permissions:
        description:
          - List of permissions for the current user on the tag.
        type: list
        elements: str
      defined_domain_permissions:
        description:
          - List of defined permissions for objects of type tag for administrators and tag owners.
        type: list
        elements: str
      all_users_permissions:
        description:
          - List of the minimum set of permissions all users have on the tag.
        type: list
        elements: str
      current_domain_permissions:
        description:
          - Specific permissions for the current tag.
        type: list
        elements: dict
        suboptions:
          id:
            description:
              - UUID of the user or group.
            type: str
          name:
            description:
              - Name of the user or group.
            type: str
          type:
            description:
              - Type of the entity, either USER or GROUP.
            type: str
            choices: ["USER", "GROUP", "ROLE"]
          permissions:
            description:
              - Permissions associated with the user or group.
            type: list
            elements: str
      version:
        description:
          - Optional, user-defined value.
          -  This value must be incremented each time the permissions are updated. Set to 1 by default.
        type: int
  filters:
    description:
      - Conditional rules for automatically applying the tag to assets, allowing for complex matching criteria.
      - Supports a maximum of 1,000 'and' or 'or' conditions per tag and a maximum of 1,024 values per condition.
      - The total size of the request body must not exceed 1 MB.
      - For more detailed information about how asset tags are managed and their limitations, refer to the Tenable documentation on applying dynamic tags.
      - See more info on applying dynamic tags in https://developer.tenable.com/docs/apply-dynamic-tags
    type: dict
    suboptions:
      asset:
        description:
          - Defines the rules for applying tags based on asset attributes or other tags.
        type: dict
        suboptions:
          and:
            description:
              - Specifies a list of conditions all of which must be met to apply the tag.
              - Values specified are not case sensitive.
            type: list
            elements: dict
            suboptions:
              field:
                description:
                  - The asset attribute name or tag to match against.
                type: str
              operator:
                description:
                  - The operator to apply on the field for matching, such as 'equals', 'does not equal', or 'contains'.
                  - Supported operators can be found in the Tenable API documentation under asset filter endpoints.
                type: str
              value:
                description:
                  - The value to match against the field. Can be a single string or multiple comma-delimited strings.
                type: str
          or:
            description:
              - Specifies a list of conditions where the tag is applied if any condition is met.
              - Values specified are not case sensitive.
            type: list
            elements: dict
            suboptions:
              field:
                description:
                  - The asset attribute name or tag to match against.
                type: str
              operator:
                description:
                  - The operator to apply on the field for matching, such as 'equals', 'does not equal', or 'contains'.
                  - Supported operators can be found in the Tenable API documentation under asset filter endpoints.
                type: str
              value:
                description:
                  - The value to match against the field. Can be a single string or multiple comma-delimited strings.
                type: str
"""
