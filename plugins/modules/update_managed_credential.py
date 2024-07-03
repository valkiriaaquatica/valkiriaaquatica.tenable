# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_managed_credential
short_description: Updates a managed credential object.
version_added: "0.0.1"
description:
  - This module updates a managed credential object.
  - Note You cannot use this endpoint to update the credential type.
  -  If you create a managed credential with the incorrect type, create a new managed credential with the
    correct credential type, and delete the incorrect managed credential.
  - Requires CAN EDIT [64] credential permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/credentials-update docs.
options:
  name:
    description:
      - The name of the managed credential.
      - This name must be unique within your Tenable Vulnerability Management instance.
    type: str
    required: false
  description:
    description:
      - The description of the managed credential object.
    type: str
    required: false
  ad_hoc:
    description:
      - A value specifying if the credential is managed (false) versus stored in a scan or policy configuration (true).
      - You can only set this parameter from true to false
      - You cannot set this parameter to true. If you omit this parameter, the value defaults to false.
    type: bool
    required: false
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
  - valkiriaaquatica.tenable.credential
"""

EXAMPLES = r"""
- name: Update managed credential
  update_managed_credential:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    credential_uuid: "123456"
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


- name: Update managed credential using enviroment creds
  update_managed_credential:
    credential_uuid: "12345"
    name: "name"
    description: "description"
    type: "type"
    settings:
      domain: "domain"
      username: "username"
      auth_method: "Password"
      password: "password"
    ad_hoc: true
"""

RETURN = r"""
api_response:
  description: Contains the raw response from the Tenable API.
  returned: success
  type: dict
  contains:
    updated:
      description: Boolean indicating if the credentials was uploaded.
      type: bool
      sample: true
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "description", "credential_uuid")
    specific_spec = {  # unique arguments
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
        "ad_hoc": {"required": False, "type": "bool"},
        "name": {"required": False, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"credentials/{module.params['credential_uuid']}"
    payload_keys = ["name", "description", "type", "settings", "permissions", "ad_hoc"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
