import pytest
from pytdx.tdx import Tdx
import os
import json
import base64

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


def test_get_kb_article(tdx_client):
    result = tdx_client.get_kb_article(kb_article_id=148208)
    assert result.ID == 148208


def test_get_asset(tdx_client):
    result = tdx_client.get_asset(asset_id=1145451)
    assert result.ID == 1145451


"""
def test_get_ticket_feed(ticket_client):
    result = ticket_client.get_ticket_feed(ticket_id=20896274)
    assert len(result) > 0


def test_get_kb_article(kb_client):
    result = kb_client.get_kb_article(kb_article_id=148208)
    assert result.id == 148208


def test_put_kb_article(kb_client):

    article = KnowledgeArticleModel(subject="TeamDynamix Changes - Jan 2024 - 2")

    print(article.model_dump())
    exit(0)

    result = kb_client.put_kb_article(kb_article_id=148208, data=article)
"""
