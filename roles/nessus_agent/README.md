Nessus Agent Role
=========

-- not prepraed yet for macOS :( --

1. Detects the windows or Linux distro used and downloads the nesssus agent package on host machine from Tenable API to /tmp.
2. Copies the download package to remote machine to /tmp.
3. Install the package.
4. Check for the nessus agent service.
5. Links the agent to Tenable (please fill with the variables needed on vars.yml)
6. Checks if the machine reports in Tenable API . (it is used the ansible_host variable but can be change to any other like mac address for more unique values).
7. Unlinks the agent (delete this if you want to preserve the agent linked).

Requirements
------------

None.

Role Variables
--------------

Variables in main.yml
- tenable_host: "your_secret_host"
- tenable_port: "your_tenable_port"
- tenable_group: "your_tenable_group"
- tenable_network: "your_tenable_network"
- linking_key: "your_linking_key"
- tenable_access_key: "your_access_key"
- tenable_secret_key: "your_secret_key"

Dependencies
------------

- A Windows or Linux machine to target

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: all
      gather_facts: true
      roles:
         - { role: nesuss_agent, tags: nesuss_agent } 

License
-------

BSD

Author Information
------------------
Fernando Mendieta Ovejero (@valkiriaaquatica)

