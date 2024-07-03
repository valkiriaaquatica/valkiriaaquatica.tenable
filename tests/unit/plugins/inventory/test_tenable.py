from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

mock_assets = [
    {
        "id": "asset1",
        "hostname": "host1.example.com",
        "fqdn": "host1.example.com",
        "agent_name": "agent1",
        "operating_system": ["OS1"],
    },
    {
        "id": "asset2",
        "hostname": "host2.example.com",
        "fqdn": "host2.example.com",
        "agent_name": "agent2",
        "operating_system": ["OS2"],
    },
]


@pytest.fixture
def inventory_module():
    from ansible_collections.valkiriaaquatica.tenable.plugins.inventory.tenable import InventoryModule

    return InventoryModule()


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.inventory.tenable.init_tenable_api")
@patch("ansible_collections.valkiriaaquatica.tenable.plugins.inventory.tenable.InventoryModule.fetch_assets")
def test_parse(mock_fetch_assets, mock_init_api, inventory_module):
    """Test the parse function of the InventoryModule."""
    mock_api_client = MagicMock()
    mock_init_api.return_value = mock_api_client
    mock_fetch_assets.return_value = mock_assets

    mock_inventory = MagicMock()
    mock_loader = MagicMock()
    path = "test_path"

    inventory_module._read_config_data = MagicMock()
    inventory_module.get_option = MagicMock(
        side_effect=lambda key, default=None: {
            "access_key": "test_access_key",
            "secret_key": "test_secret_key",
            "include_filters": [],
            "filter_search_type": "",
            "all_fields": "",
            "full_info": False,
            "date_range": 30,
            "hostname_sources": ["hostname", "fqdn", "agent_name"],
            "hostname_prefix": "",
            "hostname_suffix": "",
            "hostname_separator": "",
            "cache": False,
            "groups": {},
            "compose": {},
            "keyed_groups": {},
            "strict": False,
        }[key]
    )

    inventory_module.parse(mock_inventory, mock_loader, path)
    mock_init_api.assert_called_once_with(access_key="test_access_key", secret_key="test_secret_key")
    mock_fetch_assets.assert_called_once()


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.inventory.tenable.init_tenable_api")
@patch("ansible_collections.valkiriaaquatica.tenable.plugins.inventory.tenable.InventoryModule.fetch_assets")
@patch("ansible_collections.valkiriaaquatica.tenable.plugins.inventory.tenable.InventoryModule.fetch_asset_details")
def test_full_info(mock_fetch_asset_details, mock_fetch_assets, mock_init_api, inventory_module):
    """Test full information fetching for assets."""
    mock_api_client = MagicMock()
    mock_init_api.return_value = mock_api_client
    mock_fetch_assets.return_value = mock_assets

    detailed_asset_1 = {**mock_assets[0], "details": "full details for asset 1"}
    detailed_asset_2 = {**mock_assets[1], "details": "full details for asset 2"}

    mock_fetch_asset_details.side_effect = [detailed_asset_1, detailed_asset_2]

    mock_inventory = MagicMock()
    mock_loader = MagicMock()
    path = "test_path"

    inventory_module._read_config_data = MagicMock()
    inventory_module.get_option = MagicMock(
        side_effect=lambda key, default=None: {
            "access_key": "test_access_key",
            "secret_key": "test_secret_key",
            "include_filters": [],
            "filter_search_type": "",
            "all_fields": "",
            "full_info": True,
            "date_range": 30,
            "hostname_sources": ["hostname", "fqdn", "agent_name"],
            "hostname_prefix": "",
            "hostname_suffix": "",
            "hostname_separator": "",
            "cache": False,
            "groups": {},
            "compose": {},
            "keyed_groups": {},
            "strict": False,
        }[key]
    )

    inventory_module.parse(mock_inventory, mock_loader, path)

    mock_init_api.assert_called_once_with(access_key="test_access_key", secret_key="test_secret_key")
    mock_fetch_assets.assert_called_once()
    assert mock_fetch_asset_details.call_count == len(mock_assets)
