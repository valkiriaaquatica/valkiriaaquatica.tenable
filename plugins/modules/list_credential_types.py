# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_credential_types
short_description: Lists all credential types supported for managed credentials in Tenable Vulnerability Management.
version_added: "0.0.1"
description:
  - This module lists all credential types supported for managed credentials in Tenable Vulnerability Management
  - For more information about using the data returned by this endpoint to create managed credentials,
    see https://developer.tenable.com/docs/determine-settings-for-credential-type
  - Requires BASIC  [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/credentials-list-credential-types docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List credential types
  list_credential_types:
      access_key: "{{ tenable_access_key }}"
      secret_key: "{{ tenable_secret_key }}"

- name: List credential  types file filters with enviroment creds
  list_credential_types:
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    credentials:
      description: A list of managed credentials.
      type: list
      elements: dict
      contains:
        id:
          description: The identifier for the credential category.
          type: str
          sample: "Cloud Services"
        category:
          description: The category of the credential.
          type: str
          sample: "Cloud Services"
        default_expand:
          description: Indicates if the category should be expanded by default.
          type: bool
          sample: false
        types:
          description: A list of credential types within the category.
          type: list
          elements: dict
          contains:
            id:
              description: The identifier for the credential type.
              type: str
              sample: "Amazon AWS"
            name:
              description: The name of the credential type.
              type: str
              sample: "Amazon AWS"
            max:
              description: The maximum number of this type of credential that can be created.
              type: int
              sample: 1
            configuration:
              description: The configuration settings for the credential type.
              type: list
              elements: dict
              contains:
                type:
                  description: The type of the configuration setting (e.g., text, password).
                  type: str
                  sample: "password"
                name:
                  description: The name of the configuration setting.
                  type: str
                  sample: "AWS Access Key ID"
                required:
                  description: Indicates if the configuration setting is required.
                  type: bool
                  sample: true
                id:
                  description: The identifier for the configuration setting.
                  type: str
                  sample: "access_key_id"
            expand_settings:
              description: Indicates if the settings for the credential type should be expanded by default.
              type: bool
              sample: true
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "credentials/types"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
