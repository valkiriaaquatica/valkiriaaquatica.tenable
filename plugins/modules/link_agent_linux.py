# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: link_agent_linux
short_description: Link a Nessus Agent from a linux machine to Tenable.io.
version_added: "0.0.1"
description:
  - This module links a Nessus Agent to Tenable.io by executing a command on the host machine.
  - Module made from https://docs.tenable.com/nessus/Content/LinkAgenttoNessusManager.htm docs.
  - No macOS module yet.
options:
  linking_key:
    description:
      - The linking key provided by Tenable.io or Tenable.sc for the agent.
    required: true
    type: str
  name:
    description:
      - The name to assign to the Nessus Agent.
    required: true
    type: str
  groups:
    description:
      - The agent groups to assign the Nessus Agent to.
    required: true
    type: str
  network:
    description:
      - The network address for Tenable.sc.
    required: true
    type: str
  host:
    description:
      - The hostname or IP address of Tenable.io or Tenable.sc.
    required: true
    type: str
  port:
    description:
      - The port number to communicate with Tenable.io or Tenable.sc.
    required: true
    type: int
  become:
    description:
      - Whether to execute the linking command with elevated privileges (sudo).
    required: false
    type: bool
    default: false
requirements:
  - Python >= 3.0
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
"""

EXAMPLES = r"""
- name: Link Nessus Agent to Tenable.io
  link_agent_linux:
    linking_key: "{{ your_linking_key_here }}"
    name: "{{ ansible_hostname  }}"
    groups: "{{ tenable_group }}"
    network: "{{ tenable_network }}"
    host: "sensor.cloud.tenable.com"
    port: 443
  become: true

- name: Link Nessus Agent to Tenable.sc
  link_agent_linux:
    linking_key: "your_linking_key_here"
    name: "my_nessus_agent"
    groups: "Linux Servers,Datacenter 2"
    network: "Your Network"
    host: "tenable.sc.yourdomain.com"
    port: 8834
"""

RETURN = r"""
msg:
  description: The output message of the linking command.
  type: str
  returned: always
  sample: "Agent linked successfully."
rc:
  description: The return code of the command.
  type: int
  returned: always
  sample: 0
changed:
  description: A boolean that indicates if there was a change in the state of the target.
  returned: always
  type: bool
  sample: false
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


def link_nessus_agent(module):
    linking_key = module.params["linking_key"]
    name = module.params["name"]
    groups = module.params["groups"]
    network = module.params["network"]
    host = module.params["host"]
    port = module.params["port"]
    become = module.params["become"]

    sudo_prefix = "sudo " if become else ""
    command = "{} /opt/nessus_agent/sbin/nessuscli agent link --name='{}' --key={} --groups='{}' --network='{}' --host='{}' --port={}".format(
        sudo_prefix, name, linking_key, groups, network, host, port
    )
    rc, stdout, stderr = module.run_command(command, use_unsafe_shell=True)
    if rc != 0:
        module.fail_json(changed=False, stdout=to_native(stdout), stderr=to_native(stderr), rc=rc)
    return True, stdout, stderr, rc


def main():
    module = AnsibleModule(
        argument_spec=dict(
            linking_key=dict(required=True, type="str", no_log=True),
            name=dict(required=True, type="str"),
            groups=dict(required=True, type="str"),
            network=dict(required=True, type="str"),
            host=dict(required=True, type="str"),
            port=dict(required=True, type="int"),
            become=dict(required=False, type="bool", default=False),
        ),
        supports_check_mode=False,
    )

    is_linked, stdout, stderr, rc = link_nessus_agent(module)
    if is_linked:
        module.exit_json(changed=True, stdout=stdout, stderr=stderr, rc=rc)


if __name__ == "__main__":
    main()
