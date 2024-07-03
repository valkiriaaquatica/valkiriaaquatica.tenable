# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_managed_credential_details
short_description: Returns details of the specified managed credential object.
version_added: "0.0.1"
description:
  - This module returns details of the specified managed credential object.
  - The module is made from https://developer.tenable.com/reference/credentials-detailsdocs.
  - Requires CAN USE [32] credential  user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.credential
"""

EXAMPLES = r"""
- name: Get managed credential details
  get_managed_credential_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    credential_uuid: 11111

- name: Get managed credential details using enviroment keys
  get_managed_credential_details:
    credential_uuid: 11111
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    name:
      description: The name of the managed credential.
      type: str
      sample: "Windows devices (Headquarters)"
    description:
      description: The description of the managed credential.
      type: str
      sample: "Use for scans of Windows devices located at headquarters."
    category:
      description: The category of the managed credential.
      type: dict
      contains:
        id:
          description: The identifier for the category.
          type: str
          sample: "Host"
        name:
          description: The name of the category.
          type: str
          sample: "Host"
    type:
      description: The type of the managed credential.
      type: dict
      contains:
        id:
          description: The identifier for the type.
          type: str
          sample: "Windows"
        name:
          description: The name of the type.
          type: str
          sample: "Windows"
    ad_hoc:
      description: Indicates if the credential is ad-hoc.
      type: bool
      sample: false
    user_permissions:
      description: The user permissions for the credential.
      type: int
      sample: 64
    settings:
      description: The settings for the credential.
      type: dict
      contains:
        domain:
          description: The Windows domain to which the username belongs.
          type: str
          sample: ""
        username:
          description: The username on the target system.
          type: str
          sample: "user@example.com"
        auth_method:
          description: The authentication method.
          type: str
          sample: "Password"
        password:
          description: The user password on the target system.
          type: str
          sample: "********"
    permissions:
      description: A list of user permissions for the managed credential.
      type: list
      elements: dict
      contains:
        grantee_uuid:
          description: The UUID of the user or user group granted permissions for the managed credential.
          type: str
          sample: "59042c90-5379-43a2-8cf4-87d97f7cb68f"
        type:
          description: Specifies whether the grantee is a user or a user group.
          type: str
          sample: "user"
        permissions:
          description: Specifies the permissions granted to the user or user group for the credential.
          type: int
          sample: 64
        name:
          description: The name of the user or user group granted permissions for the managed credential.
          type: str
          sample: "user1@tenable.com"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "credential_uuid")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"credentials/{module.params['credential_uuid']}"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
