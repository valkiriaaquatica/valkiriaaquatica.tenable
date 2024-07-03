# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: download_nessus_agent
short_description: Downloads the specified version of the Nessus Agent.
version_added: "0.0.1"
description:
    - This module downloads a specified version of the Nessus Agent for a given OS distribution and version.
    - It can automatically fetch the latest version of the Nessus Agent if no specific version is provided.
    - Module made from https://developer.tenable.com/reference/get_pages-slug-files-file docs.
    - No authorization is required.
options:
    os_distribution:
        description:
            - The target OS distribution for the Nessus Agent.
            - Supported distributions include Amazon, CentOS, 'OracleLinux', 'Debian', 'RedHat', 'SLES', 'Ubuntu', and 'Windows'.
        required: true
        type: str
    os_version:
        description:
            - The version of the OS distribution. Not required for distributions like 'Debian', 'Ubuntu',
              and 'Windows'. For others, it specifies the version, example, '7' for CentOS 7.
        required: false
        type: str
        default: 'default'
    nessus_agent_version:
        description:
            - The version of the Nessus Agent to download. If not specified, the module will automatically determine the latest version available.
        required: false
        type: str
    dest:
        description:
            - The destination path on the local machine where the Nessus Agent package will be saved. PLeaes include two slashes.
        required: true
        type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
"""

EXAMPLES = r"""
- name: Download latest nessus agent in Linux gathering facts, this is the recomendes way of using, in localhost
  download_nessus_agent:
    os_distribution: "{{ ansible_facts['distribution'] }}"
    os_version: "{{ ansible_facts['lsb']['major_release'] }}"
    dest: "/tmp/"
  delegate_to: localhost


- name: Download latest Nessus Agent for Ubuntu
  download_nessus_agent:
    os_distribution: "Ubuntu"
    dest: "/path/to/download/"

- name: Download latest nessus agent for AmazonLinux.
  download_nessus_agent:
    os_distribution: "Amazon"
    dest: "/tmp/"

- name: Download Nessus Agent version for RedHat 7
  download_nessus_agent:
    os_distribution: "RedHat"
    os_version: "7"
    nessus_agent_version: "8"
    dest: "/path/to/download/"

- name: Download Nessus Agent version for CentOS 7
  download_nessus_agent:
    os_distribution: "CentOS"
    os_version: "7"
    dest: "/tmp/"

- name: Download latest Nessus Agent for Windows
  download_nessus_agent:
    os_distribution: "Windows"
    dest: "C:\\path\\to\\download\\"


# this is an exmaple of how to downlaod and install nessus agent in linux server
- name: Ensure requests module exists in the target machine
  ansible.builtin.command: pip install requests

- name: Download latest nessus agent and saved it in /tmp directory
  download_nessus_agent:
    os_distribution: "{{ ansible_facts['distribution'] }}"
    os_version: "{{ ansible_facts['lsb']['major_release'] }}"
    dest: "/tmp/"
  register: nessu_agent_download

- name: Get the package name just downloaded
  ansible.builtin.set_fact:
    nessus_agent_filename: "{{ nessu_agent_download.filename }}"

- name: Install agent Nessus Agent
  apt:
    deb: "{{ nessus_agent_filename }}"
    state: present
  register: install_result
  become: true

- name: Verify package was well installed
  ansible.builtin.assert:
    that:
      - install_result.changed
"""

RETURN = r"""
filename:
    description: The name of the file downloaded.
    type: str
    returned: on sucess
msg:
    description: Debug of imrmation
    type: str
    returned: on sucess
changed:
  description: A boolean that indicates if there was a change in the state of the target.
  returned: always
  type: bool
  sample: false
"""

# the logic of this module is not related with the rest of moedules

from ansible.module_utils.basic import AnsibleModule

try:
    import requests
except ImportError:
    pass


def get_latest_nessus_version():
    url = "https://www.tenable.com/downloads/api/v2/pages/nessus-agents"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for release_name, files in data["releases"]["latest"].items():
            if "Nessus Agents - " in release_name:
                return release_name.split(" - ")[1]
    return "latest"


def get_filename(os_distribution, os_version, nessus_agent_version=None):
    if not nessus_agent_version:
        nessus_agent_version = get_latest_nessus_version()
    # this may be updated
    os_dict = {
        "Amazon": {
            "default": f"NessusAgent-{nessus_agent_version}-amzn2.x86_64.rpm",
        },
        "CentOS": {
            "7": f"NessusAgent-{nessus_agent_version}-el7.x86_64.rpm",
            "8": f"NessusAgent-{nessus_agent_version}-el8.x86_64.rpm",
        },
        "OracleLinux": {
            "7": f"NessusAgent-{nessus_agent_version}-el7.x86_64.rpm",
            "8": f"NessusAgent-{nessus_agent_version}-el8.x86_64.rpm",
        },
        "Debian": {
            "default": f"NessusAgent-{nessus_agent_version}-debian10_amd64.deb",
        },
        "RedHat": {
            "6": f"NessusAgent-{nessus_agent_version}-el6.x86_64.rpm",
            "7": f"NessusAgent-{nessus_agent_version}-el7.x86_64.rpm",
            "8": f"NessusAgent-{nessus_agent_version}-el8.x86_64.rpm",
            "9": f"NessusAgent-{nessus_agent_version}-el9.x86_64.rpm",
        },
        "SLES": {
            "12": f"NessusAgent-{nessus_agent_version}-suse12.x86_64.rpm",
            "15": f"NessusAgent-{nessus_agent_version}-suse15.x86_64.rpm",
        },
        "Ubuntu": {
            "default": f"NessusAgent-{nessus_agent_version}-ubuntu1404_amd64.deb",
        },
        "Windows": {
            "default": f"NessusAgent-{nessus_agent_version}-x64.msi",
        },
    }

    if os_distribution in ["Ubuntu", "Debian", "Windows"]:
        filename_template = os_dict[os_distribution]["default"]
    else:
        filename_template = os_dict.get(os_distribution, {}).get(
            os_version, os_dict.get(os_distribution, {}).get("default")
        )

    if filename_template:
        return filename_template.format(nessus_agent_version=nessus_agent_version)

    return None


def main():
    argument_spec = {
        "os_distribution": {"required": True, "type": "str"},
        "os_version": {"required": False, "type": "str", "default": "default"},
        "nessus_agent_version": {"required": False, "type": "str", "default": None},
        "dest": {"required": True, "type": "str"},
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    os_distribution = module.params["os_distribution"]
    os_version = module.params["os_version"]
    nessus_agent_version = module.params["nessus_agent_version"]
    dest = module.params["dest"]

    filename = get_filename(os_distribution, os_version, nessus_agent_version)

    if filename:
        base_url = "https://www.tenable.com/downloads/api/v2/pages/nessus-agents/files/"
        full_url = base_url + filename
        response = requests.get(full_url, stream=True)

        if response.status_code == 200:
            file_path = filename
            with open(dest + filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            module.exit_json(changed=True, filename=file_path, msg=f"File: {filename} download sucessefully.")
        else:
            module.fail_json(msg=f"Error downloading the file. Status code: {response.status_code}")
    else:
        module.fail_json(msg=f"File was not found for distribution: {os_distribution} with version {os_version}.")


if __name__ == "__main__":
    main()
