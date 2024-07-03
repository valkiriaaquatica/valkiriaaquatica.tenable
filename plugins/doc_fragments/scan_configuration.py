# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  uuid:
    description:
      - The UUID for the Tenable-provided scan template to use
      - Use the list_templates module to list the available scan templates.
    type: str
    required: True
  settings:
    description: A dictionary containing various settings for the scan.
    type: dict
    required: True
    suboptions:
      name:
        description: The name of the scan.
        type: str
        required: True
      description:
        description: The description of the scan.
        type: str
        required: False
      policy_id:
        description:
          - The unique ID of the policy to use to create the scan.
          -  If your user permissions are set to SCAN OPERATOR [24], this parameter is required
          - Use the list_policies module to list them.
        type: int
        required: False
      folder_id:
        description:
          - The unique ID of the folder where you want to store the scan.
          - Use the list_folders module to list them.
          -  If no folder_id is passed in the request, Tenable asigna el main folder.
        type: int
        required: False
      scanner_id:
        description:
          - The unique ID of the scanner to use.
          - Use the list_scanners module to find de scanner id.
          - You can use the special value AUTO-ROUTED to assign scan targets to scanner groups based on the groups'
            configured scan route.
          - For more information on Auto-Routed see https://developer.tenable.com/docs/manage-scan-routing-tio .
          - If no scanner_id is passed in the request, Tenable assigns the US Cloud Scanner by default.
        type: str
        required: False
      target_network_uuid:
        description:
          - Network UUID that targets the scan.
          - This field is required if the scanner_id parameter is AUTO-ROUTED
          - If your scans involve separate environments with overlapping IP ranges, specify the UUID of the network you want
            to associate with the results of the auto-routed scan
          - This value must match the network where you have assigned the scanner groups that you configured for scan routing.
          - Note This parameter does not override network associations for scans that are not auto-routed.
          - Tenable Vulnerability Management automatically associates a non-routed scan with the network to which you have
            assigned the scanner that performs the scan.
        type: str
        required: False
      enabled:
        description:
          - Whether the scan is enabled.
          - If true, the schedule for the scan is enabled.
          - If no enabled variable is passed in the request, tenable assigns by default the true value.
          - Note that scheduled scans do not run if they are in the scan owner's trash folder.
        type: bool
        required: False
      launch:
        description:
          - When to launch the scan.
          - Note that scheduled scans do not run if they are in the scan owner's trash folder.
        choices: ["ON_DEMAND", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
        type: str
        required: False
      scan_time_window:
        description:
          - Time window in minutes for when the scan can run.
          - For Nessus Agent scans is the time frame in minutes during agents send data to tenable. If no value is passed,
            tenable assigns 180 min.
          - For Nessus Scanner is the time frame, in minutes, after which the scan will automatically stop. If no value
            is passed, Tenable assigns 0 min.
        type: int
        required: False
      starttime:
        description:
          - Start time for the first scan, in any format date string.
          - For one-time scans, the starting time and date for the scan.
          - For recurrent scans, the first date on which the scan schedule is active and the time that recurring scans launch
            based on the rrules parameter
          - This parameter must be in the following format YYYYMMDDTHHMMSS
          - This parameter corresponds to the Starts drop-down boxes in scan schedule settings in the Tenable Vulnerability
            Management user interface.
        type: str
        required: False
      rrules:
        description:
          - Recurrence rules for scheduled scanning.
          - The interval at which the scan repeats.
          - The interval is formatted as a string of three values delimited by semi-colons
          - (FREQ=ONETIME or DAILY or WEEKLY or MONTHLY or YEARLY), the interval (INTERVAL=1 or 2 or 3 ... x), and the
             days of the week (BYDAY=SU,MO,TU,WE,TH,FR,SA
          - For a scan that runs every three weeks on Monday Wednesday and Friday, the string would be FREQ=WEEKLY;INTERVAL=3;BYDAY=MO,WE,FR.
          - If the scan is not scheduled to recur, this attribute is null.
        type: str
        required: False
      timezone:
        description:
          - The timezone of the scheduled start time for the scan.
          - To list all available Tenable timezones use get_timezones module.
          - Corresponds to the Timezone drop-down box in the scan schedule settings in the Tenable Vulnerability Management user interface.
        type: str
        required: False
      text_targets:
        description:
          - The list of targets to scan.
          - This parameter is required if your request omits other target parameters.
          - Note that Tenable does not verify if values passed are correct or not.
        type: str
        required: False
      target_groups:
        description:
          - DEPRECATED
        type: list
        elements: int
        required: False
      file_targets:
        description:
          - The name of a file containing the list of targets to scan.
          - Before you use this parameter, use the upload_file module to upload the file to Tenable Vulnerability Management; then,
            use the fileuploaded attribute of the response message as the file_targets parameter value.
          - This parameter is required if your request omits other target parameters.
          - Note Unicode/UTF-8 encoding is not supported in the targets file.
        type: str
        required: False
      tag_targets:
        description:
          - The list of asset tag identifiers that the scan uses to determine which assets it evaluates.
          - For more information about tag-based scans, see https://developer.tenable.com/docs/manage-tag-based-scans-tio .
          - This parameter is required if your request omits other target parameters.
        type: list
        elements: str
        required: False
      host_tagging:
        description: Creates a unique identifier on hosts scanned using credentials.
        type: str
        required: False
      agent_group_id:
        description:
          - An array of agent group UUIDs to scan.
          - Required if the scan is an agent scan.
        type: list
        elements: str
        required: False
      agent_scan_launch_type:
        description:
          - Launch type for agent-based scans.
          - For Nessus Agent scans, indicates whether the agent scan should use the scan window (scheduled) or rule-based
            (triggered) method for scan launches.
        type: str
        required: False
        choices: ["scheduled", "triggered"]
      triggers:
        description:
          - List of triggers that define when a scan should be initiated.
          - Each trigger has a specific type and options related to that type.
        type: list
        elements: dict
        required: False
        suboptions:
          type:
            description:
              - Type of trigger for scan initiation.
              - "'periodic' for periodic launches."
              - "'file-exists' for launching a scan when a specific file is created."
            type: str
            required: False
            choices: ['periodic', 'file-exists']
          options:
            description:
              - Specific options depending on the type of trigger.
            type: dict
            required: False
            suboptions:
              periodic_hourly_interval:
                description:
                  - Interval in hours between scan launches. Only applicable if the trigger type is 'periodic'.
                type: int
                required: False
              filename:
                description:
                  - Name of the file which, when created, triggers a scan launch. Only applicable if the trigger type is 'file-exists'.
                type: str
                required: False
      refresh_reporting_type:
        description:
          - For Nessus Agent scans, specifies how often the agent should report unchanged info-level vulnerability findings
          - This setting corresponds to Info-level Reporting in Basic Settings in the user interface.
          - You can configure agent scans to launch a new baseline scan after a certain interval, either number of scans or number of days.
          - Scans—The agent scan reports all findings every x number of scans. You can choose any integer from 7 to 20. By default, Tenable uses a value of 10.
          - Days—The agent scan reports all findings after a set number of days after the previous day on which the scan last reported all findings.
            You can choose any integer from 7 to 90. By default, Tenable uses a value of 10.
          - Note This setting for info-level reporting can only be used by agents version 10.5.0 and later.
            Any agents on earlier versions always perform baseline scans.
        type: str
        required: False
        choices: ['scans','days']
      refresh_reporting_frequency_scans:
        description:
          - Determines the number of scans after which the Nessus Agent scan reports all findings.
          - This setting applies to Nessus Agent scans with the info-level reporting type (refresh_reporting_type) set to scans
          - You can choose any integer from 7 to 20. By default, Tenable Vulnerability Management uses a value of 10.
        type: int
        required: False
      refresh_reporting_frequency_days:
        description:
          - Determines the number of days after which the Nessus Agent scan reports all findings.
          - This setting applies to Nessus Agent scans with the info-level reporting type (refresh_reporting_type) set to days.
          - You can choose any integer from 7 to 90. By default, Tenable uses a value of 10.
        type: int
        required: False
      disable_refresh_reporting:
        description:
          - Indicates whether or not the Nessus Agent should force a refresh of all info-level findings on the next scan.
          - After the next scan completes and reports all findings, the refresh_reporting_type setting determines how
            often the scan reports info-severity findings.
          - Note All vulnerability findings with a severity of low or higher and new or changed info-level vulnerabilities
            are always reported after every scan.
        type: str
        required: False
        choices: ['yes','no']
      emails:
        description:
          - Email addresses to notify when the scan completes.
          - A comma-separated list of accounts that receive the email summary report.
        type: str
        required: False
      acls:
        description:
          - A list of access control entries specifying permissions to apply to the scan.
          - An array containing permissions to apply to the scan.
        type: list
        elements: dict
        required: False
        suboptions:
          permissions:
            description:
              - The scan permission.
              - For more information, refer to the Permissions section in the Tenable documentation.
            type: int
            required: False
          owner:
            description:
              - Indicates whether the specified user or group owns the scan.
              - Possible values are null (system-owned), 0 (not an owner), 1 (owner).
            type: int
            required: False
          display_name:
            description:
              - The display name of the user or group in the Tenable Vulnerability Management UI.
            type: str
            required: False
          name:
            description:
              - The name of the user or group granted the permissions.
            type: str
            required: False
          id:
            description:
              - The identifier used to order the display of user or groups in the Permissions tab in the Tenable Vulnerability Management UI.
            type: int
            required: False
          type:
            description:
              - The type of scan permission.
              - "'default' for default permissions, 'user' for individual user permissions, 'group' for user group permissions."
            type: str
            required: False
            choices: ['default', 'user', 'group']
  plugin_configurations:
    description:
      - List of plugin configurations for the scan. Each item in the list configures a specific plugin family.
    type: list
    required: False
    elements: dict
    suboptions:
      plugin_family_name:
        description:
          - The name of the plugin family.
        type: str
        required: True
      plugins:
        description:
          - List of plugins within the specified family.
        type: list
        required: True
        elements: dict
        suboptions:
          plugin_id:
            description:
              - The unique identifier for a specific plugin within the family.
            type: str
            required: True
          status:
            description:
              - Indicates whether the plugin is 'enabled' or 'disabled'.
            type: str
            required: True
            choices: ['enabled', 'disabled']
"""
