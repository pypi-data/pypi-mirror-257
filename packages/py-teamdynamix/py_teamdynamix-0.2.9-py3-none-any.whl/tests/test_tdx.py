import pytest
from pytdx.tdx import Tdx
import os
import json
import base64
from pytdx.models.ticket import Ticket, TicketFeed, TicketType
from pytdx.models.attribute import AttributeChoice
from pytdx.models.asset import Asset, AssetModel
from pytdx.models.knowledge_article import KnowledgeArticle

conn_info_encoded = os.environ.get("TDX_SB_CONN")
conn_info = json.loads(base64.b64decode(conn_info_encoded))

username = conn_info[0]
password = conn_info[1]
hostname = conn_info[2]
environment = conn_info[3]
asset_app_id = conn_info[4]
client_portal_app_id = conn_info[5]
ticketing_app_id = conn_info[6]
is_admin = conn_info[7]


@pytest.fixture
def tdx_client():
    return Tdx(
        username=username,
        password=password,
        hostname=hostname,
        environment=environment,
        ticketing_app_id=ticketing_app_id,
        client_portal_app_id=client_portal_app_id,
        asset_app_id=asset_app_id,
        is_admin=is_admin,
    )


def test_get_ticket(tdx_client):
    result = tdx_client.get_ticket(id=20896274)
    assert result.ID == 20896274
    assert isinstance(result, Ticket)


def test_get_kb_article(tdx_client):
    result = tdx_client.get_kb_article(kb_article_id=148208)
    assert result.ID == 148208
    assert isinstance(result, KnowledgeArticle)


def test_get_asset(tdx_client):
    result = tdx_client.get_asset(asset_id=1145451)
    assert result.ID == 1145451
    assert isinstance(result, Asset)


def test_get_types(tdx_client):
    # Retrieve ticket types
    types = tdx_client.get_types()
    assert isinstance(types, list)
    assert len(types) > 0
    assert all(isinstance(type, TicketType) for type in types)


def test_get_asset_models(tdx_client):
    # Retrieve asset models
    models = tdx_client.get_asset_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert models[0].ID > 0
    assert all(isinstance(model, AssetModel) for model in models)


def test_get_asset_product_type_id(tdx_client):
    # Retrieve product type ID
    product_type_name = "Laptop"
    product_type_id = tdx_client.get_asset_product_type_id(
        asset_product_type_name=product_type_name
    )
    assert isinstance(product_type_id, int)


def test_get_asset_manufacturer_id(tdx_client):
    # Retrieve manufacturer ID
    manufacturer_name = "Apple"
    manufacturer_id = tdx_client.get_asset_manufacturer_id(
        asset_manufacturer_name=manufacturer_name
    )
    assert isinstance(manufacturer_id, int)


def test_update_ticket_with_mock(mocker, tdx_client):
    # Create a mock response for the update_ticket method
    mock_updated_ticket_data = {
        "ID": 12345,
        "Title": "Updated Mock Ticket",
        "Description": "Updated Mock Description",
    }
    mock_updated_ticket = Ticket(**mock_updated_ticket_data)

    # Mock the __request method to return the mock_updated_ticket_data
    mocker.patch.object(
        tdx_client, "_Tdx__request", return_value=mock_updated_ticket_data
    )

    # Call the update_ticket method
    updated_ticket = tdx_client.update_ticket(id=12345, data=mock_updated_ticket)

    # Assertion
    assert updated_ticket.to_dict() == mock_updated_ticket.to_dict()
    assert isinstance(updated_ticket, Ticket)


### Admin tests

"""
def test_get_attribute_choices(tdx_client):
    # Retrieve attribute choices
    attribute_id = 139852
    choices = tdx_client.get_attribute_choices(attribute_id=attribute_id)
    assert isinstance(choices, list)
    assert len(choices) > 0
"""
