# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
name: tenable
short_description: Fetches assets, networks, or agents from Tenable as inventory hosts.
description:
    - This inventory plugin fetches data from Tenable.
    - Filters can be applied, group formation, compose creation and all inventory default carachteristics Ansible offers.
    - A preffix and a suffix can be added to the host name creation.
    - If full_info argument is set to true, the inventory will take a bit longer because more data is being fetched.
    - To use it, Tenable requires BASIC [16] user permissions.
    - Check more info on listing assets in the list_assets
      module or in https://developer.tenable.com/reference/workbenches-assets
options:
    hostname_sources:
        description: List of fields to consider for the host name, in order of priority.
        required: False
        type: list
        default: [hostname", "id", "agent_name", "fqdn"]
        elements: str
    hostname_prefix:
        description: Prefix to prepend to the host name. String value.
        required: False
        type: str
        default: ''
    hostname_suffix:
        description: Suffix to append to the host name. String value.
        required: False
        type: str
        default: ''
    hostname_separator:
        description: Separator to use between prefix, host name, and suffix.
        required: False
        type: str
        default: ''
    include_filters:
        description: Filters to include only assets that match certain tag criteria.
        required: False
        type: list
        elements: dict
        default: []
    full_info:
        description:
            - Include full information for each asset.
            - This include the information supplied when a request to get_asset_details.
            - With true option, more filters cna be applied like most of the agent filters.
            - Check for get asset details here https://developer.tenable.com/reference/io-asm-assets-details
        required: False
        type: bool
        default: False
    all_fields:
        description:
        - Specifies whether to include all fields ('full') or only the default fields ('default') in the returned data.
        - Note this argument is in Tenable default API parameters.
          Check this https://developer.tenable.com/reference/workbenches-assets for more info.
        type: str
        required: false
        choices: ['full', 'default']
extends_documentation_fragment:
    - ansible.builtin.constructed
    - inventory_cache
    - valkiriaaquatica.tenable.credentials
    - valkiriaaquatica.tenable.filters
    - valkiriaaquatica.tenable.date
    - valkiriaaquatica.tenable.filter_search_type
version_added: "0.0.1"
author: Fernando Mendieta Ovejero (@valkiriaaquatica)
"""

EXAMPLES = r"""
---

# simple example getting all assets
plugin: tenable

---

# use compose to create vars and forming keyed_groups for the operatying sytstem and a prefix
plugin: tenable
compose:
  ansible_host: aws_ec2_name
keyed_groups:
  - key: operating_system
    prefix: 'os'
    separator: '_'

---

# create group if the asset has no agent_name
# create group where the asset has no agent
# create group where the asset has agent
plugin: tenable
groups:
  assets_with_agent: has_agent == true
  assets_without_agent: has_agent == false
  assets_without_agent_name: agent_name | length == 0

---

# use filters to get asssets from eu-west-1b
# create ansible_hsot var with the aws_ec2_name value
# the hsotname or hostvar of the instance is created with a preffix
# the ostname of th einstance is change from default to just ipv4
plugin: tenable
hostname_suffix: "i_am_the_prefix"
hostname_sources: ipv4
include_filters:
  - type: aws_availability_zone
    operator: eq
    value: eu-west-1b

compose:
  ansible_host: aws_ec2_name

---

# use or flters to get aws and azure assets
# creates a static variable for al the hosts
# convertes the : of the first ipv6 to /
# a suffix is added to the default hostname creation name
plugin: tenable
filter_search_type: or
hostname_suffix: "i_am_the_suffix"
include_filters:
  - type: "tag.Cloud Provider"
    operator: set-has
    value: AZURE
  - type: "tag.Cloud Provider"
    operator: set-has
    value: AWS
compose:
  static_variable: "'the_static_variable'"
  converted_ip: ipv6[0] | regex_replace(':','/')
  first_seen: first_seen

groups:
  centos_group: operating_system[0] == "CentOS Linux 7 (Core)"
keyed_groups:

---

# get all info of assets and filter by the ones in google cloud
# creates a varable with asset as a string and getting the id variable of each host
# hases the id to md5
plugin: tenable
full_info: true
include_filters:
  - type: "tag.Cloud Provider"
    operator: set-has
    value: "Google Cloud"
compose:
  asset_id_host: "'asset' + id"
  hash_id: id | md5

---

# using the full_info more data is returend so new groups can be formed
# make groups os assets that their first tag value is Unavailable
# make groups of aws that their actual state is stopped
# make groups of instances that are of the same aws account
# make groups of network machine
# make groups with their system type
plugin: tenable
full_info: true
groups:
  unavailable_tag: tags[0].tag_value == "Unavailable"
  stpped_aws_machines: aws_ec2_instance_state_name[0] == "stopped"
keyed_groups:
  - key: aws_owner_id
    prefix: 'account'
    separator: '_'
  - key: network_id
    prefix: "_"
  - key: system_type
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api import init_tenable_api
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters

from ansible.inventory.group import to_safe_group_name as orig_safe
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.plugins.inventory import Cacheable
from ansible.plugins.inventory import Constructable
from ansible.utils.vars import combine_vars


class ConstructableWithLookup(Constructable):
    def _compose(self, template, variables):
        """Helper method for plugins to compose variables for Ansible based on jinja2 expression and inventory vars"""
        t = self.templar

        try:
            use_extra = self.get_option("use_extra_vars")
        except Exception:
            use_extra = False

        if use_extra:
            t.available_variables = combine_vars(variables, self._vars)
        else:
            t.available_variables = variables

        return t.template(
            "%s%s%s"
            % (
                t.environment.variable_start_string,
                template,
                t.environment.variable_end_string,
            ),
            disable_lookups=False,
        )


class InventoryModule(BaseInventoryPlugin, ConstructableWithLookup, Cacheable):
    NAME = "tenable"
    _sanitize_group_name = staticmethod(orig_safe)

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            valid = False
            if path.endswith(("tenable.yml", "tenable.yaml")):
                valid = True
            self.display.vvv('Skipping due to inventory source not ending in "tenable.yml" nor "tenable.yaml"')
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parses the inventory file"""
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        self.display.vv("Initializing Tenable API client")
        try:
            access_key = self.get_option("access_key")
            secret_key = self.get_option("secret_key")
            api_client = init_tenable_api(access_key=access_key, secret_key=secret_key)
        except Exception as e:
            self.display.error(f"Failed to initialize Tenable API client: {str(e)}")
            return

        filters = self.get_option("include_filters")
        filter_search_type = self.get_option("filter_search_type", "")
        all_fields = self.get_option("all_fields", "")
        full_info = self.get_option("full_info", False)
        date_range = self.get_option("date_range", 30)

        self.display.vvv(
            f"Building query params for: date_range={date_range}, filter_search_type={filter_search_type}, all_fields={all_fields}"
        )
        query_parameters = build_query_parameters(
            date_range=date_range, filter_search_type=filter_search_type, all_fields=all_fields
        )
        self.display.vvv(f"Adding custom filters: {filters}")
        query_parameters = add_custom_filters(query_parameters, filters, handle_multiple_filters)

        cache_key = self.get_cache_key(path)
        cache_enabled = self.get_option("cache")

        self.display.vvv(f"Checking cache: enabled={cache_enabled}, key={cache_key}")
        resources = self._cache.get(cache_key) if cache_enabled and self._cache.get(cache_key) else None

        if not resources:
            self.display.vv("Fetching assets from Tenable API")
            try:
                resources = self.fetch_assets(api_client, query_parameters)
                if cache_enabled and resources:
                    self.display.vv("Caching fetched assets")
                    self._cache.set(cache_key, resources)
            except Exception as e:
                self.display.error(f"Error fetching assets: {str(e)}")
                return

        if resources:
            self.display.vv("Populating inventory with fetched assets")
            self.populate_inventory(resources, api_client, full_info)

    def fetch_assets(self, api_client, query_parameters):
        """Fetches assets from Tenable API using the constructed query parameters"""
        endpoint = "workbenches/assets"
        self.display.vvvv(f"Making API request to endpoint: {endpoint} with parameters: {query_parameters}")
        try:
            response = api_client.request("GET", endpoint, params=query_parameters)
            self.display.vvvv(f"API response received: {response}")
            return response["data"].get("assets", [])
        except Exception as e:
            self.display.error(f"Failed to fetch assets from Tenable: {str(e)}")
            return []

    def fetch_asset_details(self, api_client, asset_id):
        """Fetches detailed information for a given asset"""
        endpoint = f"assets/{asset_id}"
        self.display.vvvv(f"Making API request to endpoint: {endpoint} for asset ID: {asset_id}")
        try:
            response = api_client.request("GET", endpoint)
            self.display.vvvv(f"API response for asset details: {response}")
            return response["data"] if response else None
        except Exception as e:
            self.display.error(f"Failed to fetch asset details for {asset_id}: {str(e)}")
            return None

    def populate_inventory(self, assets, api_client, full_info):
        """Populates the Ansible inventory with fetched assets based on tag filters."""
        for asset in assets:
            self.display.vvvv(f"Processing asset: {asset['id']}")
            if full_info:
                asset = self.fetch_asset_details(api_client, asset["id"]) or asset
            host_name = self.get_hostname_of_asset(asset)
            if host_name:
                self.display.vvv(f"Adding host to inventory: {host_name}")
                host = self.inventory.add_host(host_name)
                self.inventory.set_variable(host, "asset_details", asset)
                self._set_composite_vars(self.get_option("compose"), asset, host, self.get_option("strict"))
                self._add_host_to_composed_groups(self.get_option("groups"), asset, host, self.get_option("strict"))
                self._add_host_to_keyed_groups(self.get_option("keyed_groups"), asset, host, self.get_option("strict"))

    def get_hostname_of_asset(self, asset):
        """Determines the hostname from asset."""
        hostname_sources = self.get_option("hostname_sources", ["hostname", "agent_name", "id", "fqdn"])
        prefix = self.get_option("hostname_prefix", "")
        suffix = self.get_option("hostname_suffix", "")
        separator = self.get_option("hostname_separator", "")

        for key in hostname_sources:
            if key in asset and asset[key]:
                base_name = asset[key][0] if isinstance(asset[key], list) else asset[key]
                return f"{prefix}{separator}{base_name}{separator}{suffix}" if (prefix or suffix) else base_name

        self.display.warning("No valid host name found, using 'unknown_host'")
        return "unknown_host"
