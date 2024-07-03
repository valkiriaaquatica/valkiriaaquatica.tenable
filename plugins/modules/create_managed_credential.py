# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: create_managed_credential
short_description: Creates a managed credential object that you can use when configuring and running scans.
version_added: "0.0.1"
description:
  - This module creates a managed credential object that you can use when configuring and running scans.
  - You can grant other users the permission to use the managed credential object in scans and to edit the managed credential configuration.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/credentials-create docs.
options:
  name:
    description:
      - The name of the managed credential.
      - This name must be unique within your Tenable Vulnerability Management instance.
    type: str
    required: true
  description:
    description:
      - The description of the managed credential object.
    type: str
    required: false
  type:
    description:
      - The type of credential object.
      - For a list of supported credential types, use the GET /credentials/types endpoint or use the list_credential_types module.
    type: str
    required: true
  settings:
    description:
      - The configuration settings for the credential.
      - The parameters of this object vary depending on the credential type.
      - For more information, see  https://developer.tenable.com/docs/determine-settings-for-credential-type .
      - Note This form displays limited parameters that support a Windows type of credential that uses password authentication.
    required: true
    type: dict
    suboptions:
      domain:
        description:
          - The Windows domain to which the username belongs.
        required: false
        type: str
      username:
        description:
          - The username on the target system.
        required: false
        type: str
      auth_method:
        description:
          - The name for the authentication method.
          - This value corresponds to the credentials[].types[].configuration[].options[].id attribute in the
            response message of list_credential_types module.
        required: false
        type: str
      password:
        description:
          - The user password on the target system.
        required: false
        type: str
  permissions:
    description:
      - A list of user permissions for the managed credential.
      - If a request message omits this parameter, Tenable Vulnerability Management automatically creates
        a permissions object for the user account that submits the request.
    required: false
    type: list
    elements: dict
    suboptions:
      grantee_uuid:
        description:
          - The UUID of the user or user group granted permissions for the managed credential.
          - This parameter is required when assigning CAN USE (32) or CAN EDIT (64) permissions for a managed credential.
        required: false
        type: str
      type:
        description:
          - A value specifying whether the grantee is a user (user) or a user group (group).
          - This parameter is required when assigning CAN USE (32) or CAN EDIT (64) permissions for a managed credential.
        required: false
        type: str
      permissions:
        description:
          - A value specifying the permissions granted to the user or user group for the credential.
          - 32—The user can view credential information and use the credential in scans. Corresponds
            to the Can Use permission in the user interface.
          - 64—The user can view and edit credential settings, delete the credential, and use the credential in scans.
            Corresponds to the Can Edit permission in the user interface.
          - This parameter is required when assigning CAN USE (32) or CAN EDIT (64) permissions for a managed credential.
        required: false
        type: int
      name:
        description:
          - The name of the user or user group that you want to grant permissions for the managed credential.
        required: false
        type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Create managed credential
  create_managed_credential:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    name: "name"
    description: "description"
    type: "type"
    settings:
      domain: "domain"
      username: "username"
      auth_method: "Password"
      password: "password"
    permissions:
      - grantee_uuid: "grantee_uuid"
        type: "user"
        permissions: 64
        name: "name"
  tags: create_managed_credential

- name: Create managed credential using enviroment creds
  create_managed_credential:
    name: "name"
    description: "description"
    type: "type"
    settings:
      domain: "domain"
      username: "username"
      auth_method: "Password"
      password: "password"
"""

RETURN = r"""
api_response:
  description: Contains the raw response from the Tenable API.
  returned: success
  type: dict
  contains:
    id:
      description: The ID of the created credential.
      type: str
      sample: "1111122269a"
    name:
      description: The name of the created credential.
      type: str
      sample: "Managed Credential Name"
    description:
      description: The description of the created credential.
      type: str
      sample: "Credential Description"
    type:
      description: The type of the created credential.
      type: str
      sample: "Windows"
    settings:
      description: Configuration settings for the credential.
      type: dict
      contains:
        domain:
          description: The domain for the credential.
          type: str
          sample: "domain"
        username:
          description: The username for the credential.
          type: str
          sample: "username"
        auth_method:
          description: The authentication method for the credential.
          type: str
          sample: "Password"
    permissions:
      description: List of user permissions for the managed credential.
      type: list
      elements: dict
      contains:
        grantee_uuid:
          description: The UUID of the user or user group granted permissions.
          type: str
          sample: "grantee_uuid"
        type:
          description: Specifies whether the grantee is a user or a user group.
          type: str
          sample: "user"
        permissions:
          description: Permissions granted to the user or user group.
          type: int
          sample: 64
        name:
          description: The name of the user or user group.
          type: str
          sample: "name"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "name", "description")
    specific_spec = {  # unique arguments
        "type": {"required": True, "type": "str"},
        "settings": {
            "required": True,
            "type": "dict",
            "options": {
                "domain": {"required": False, "type": "str"},
                "username": {"required": False, "type": "str"},
                "auth_method": {"required": False, "type": "str"},
                "password": {"required": False, "type": "str", "no_log": True},
            },
        },
        "permissions": {
            "required": False,
            "type": "list",
            "elements": "dict",
            "options": {
                "grantee_uuid": {"required": False, "type": "str"},
                "type": {"required": False, "type": "str"},
                "permissions": {"required": False, "type": "int"},
                "name": {"required": False, "type": "str"},
            },
        },
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "credentials"
    payload_keys = ["name", "description", "type", "settings", "permissions"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
