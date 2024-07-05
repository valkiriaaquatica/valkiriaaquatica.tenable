from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: unlink_agent_linux
short_description: Unlink nessus agent from Linux server.
version_added: "0.0.1"
description:
  - This module unlinks the nessus agent relation that has a server with Tenable IO.
  - No macOS module yet.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
"""


EXAMPLES = r"""
- name: Unlink the Nessus Agent on the target machine
  unlink_agent_linux:
  become: true
"""

RETURN = r"""
msg:
  description: Message about the result of the unlink operation.
  returned: on success
  type: str
  sample: "Nessus Agent unlinked successfully"
"""


import subprocess

from ansible.module_utils.basic import AnsibleModule


def unlink_nessus_agent(module):
    command = "/opt/nessus_agent/sbin/nessuscli agent unlink"

    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return True, "Nessus Agent unlinked successfully"
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        if "No host information found" in output:
            return True, "No Agent is running on the server, no need to unlink"
        else:
            module.fail_json(msg="Failed to unlink Nessus Agent: {}".format(output))


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=False,
    )

    is_unlinked, message = unlink_nessus_agent(module)
    if is_unlinked:
        module.exit_json(changed=True, msg=message)


if __name__ == "__main__":
    main()
