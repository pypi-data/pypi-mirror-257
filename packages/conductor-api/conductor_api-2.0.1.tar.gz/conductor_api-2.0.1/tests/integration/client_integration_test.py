from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import pytest
from unittest.mock import patch

import json
import requests

from conductor_api.client import ConductorService, AccountService


class MockServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(requests.codes.ok)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        if "/v3/locations?apiKey" in self.path:
            response_content = json.dumps([{
                "locationId": "1",
                "description": "United States"
            }]
            )
        elif "/v3/rank-sources?apiKey" in self.path:
            response_content = json.dumps([{
                "baseDomain": "google.com",
                "description": "Google (US / English)",
                "rankSourceId": "1",
                "name": "GOOGLE_EN_US"
            }]
            )
        elif "/v3/devices?apiKey" in self.path:
            response_content = json.dumps([{
                "locationId": "1",
                "description": "Desktop",
                "deviceId": "1",
            }]
            )
        elif "/v3/accounts?apiKey" in self.path:
            response_content = json.dumps([{
                "isActive": True,
                "accountId": "10550",
                "webProperties": "https://api.conductor.com/v3/"
                                 "accounts/10550/web-properties",
                "name": "PS Reporting Test",
            }]
            )
        elif "/web-properties?apiKey" in self.path:
            response_content = json.dumps([{
                "isActive": True,
                "rankSourceInfo": [],
                "webPropertyId": "43162",
                "trackedSearchList": "https://api.conductor.com/v3/"
                                     "accounts/10550/web-properties/43162/"
                                     "tracked-searches",
                "name": "conductor.com"
            }]
            )
        elif "/tracked-searches?apiKey" in self.path:
            response_content = json.dumps([{
                "isActive": True,
                "trackedSearchId": "7188291",
                "preferredUrl": "https://www.conductor.com/",
                "queryPhrase": "conductor",
                "locationId": "1",
                "rankSourceId": "1",
                "deviceId": "1"
            }]
            )
        elif "/categories?apiKey" in self.path:
            response_content = json.dumps([{
                "created": "2018-02-12T13:53:46.000Z",
                "trackedSearchIds": [],
                "modified": "2018-02-12T13:53:46.000Z",
                "name": "Intent - Early - Why"
            }]
            )
        elif "/serp-items?apiKey" in self.path:
            response_content = json.dumps([{
                "ranks": {
                    "UNIVERSAL_RANK": None,
                    "TRUE_RANK": 6,
                    "CLASSIC_RANK": 3
                },
                "webPropertyId": 43162,
                "trackedSearchId": 7188291,
                "itemType": "ANSWER_BOX",
                "target": "",
                "targetDomainName": "conductor.com",
                "targetUrl": "https://www.conductor.com/blog"
            }]
            )
        elif "/search-volumes?apiKey" in self.path:
            response_content = json.dumps([{
                "averageVolume": 135000,
                "trackedSearchId": 7188291,
                "volumeItems": []
            }]
            )
        else:
            response_content = None
        self.wfile.write(response_content.encode("utf-8"))
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(("localhost", port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


@pytest.fixture(scope="module")
def mock_server():
    mock_server_port = get_free_port()
    mock_url = f"http://localhost:{mock_server_port}"
    mock_api_key = 'mock-api-key'
    mock_secret = 'mock-secret'
    start_mock_server(mock_server_port)
    return mock_url, mock_api_key, mock_secret


def test_get_locations(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        cs = ConductorService(api_key=mock_api_key, secret=mock_secret)
        locations = cs.get_locations()
    assert locations == [{
        "locationId": "1",
        "description": "United States"
    }]


def test_get_rank_sources(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        cs = ConductorService(api_key=mock_api_key, secret=mock_secret)
        rank_sources = cs.get_rank_sources()
    assert rank_sources == [{
        "baseDomain": "google.com",
        "description": "Google (US / English)",
        "rankSourceId": "1",
        "name": "GOOGLE_EN_US"
    }]


def test_get_devices(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        cs = ConductorService(api_key=mock_api_key, secret=mock_secret)
        devices = cs.get_devices()
    assert devices == [{
        "locationId": "1",
        "description": "Desktop",
        "deviceId": "1",
    }]


def test_get_accounts(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        cs = ConductorService(api_key=mock_api_key, secret=mock_secret)
        accounts = cs.get_accounts()
    assert accounts == [{
        "isActive": True,
        "accountId": "10550",
        "webProperties": "https://api.conductor.com/v3/"
                         "accounts/10550/web-properties",
        "name": "PS Reporting Test",
    }]


def test_get_web_properties(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        account_service = AccountService(10550, api_key=mock_api_key, secret=mock_secret)
        web_properties = account_service.get_web_properties()
    assert web_properties == [{
        "isActive": True,
        "rankSourceInfo": [],
        "webPropertyId": "43162",
        "trackedSearchList": "https://api.conductor.com/v3/accounts/"
                             "10550/web-properties/43162/tracked-searches",
        "name": "conductor.com"
    }]


def test_get_tracked_searches(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        ss = AccountService(10550, api_key=mock_api_key, secret=mock_secret)
        tracked_searches = ss.get_tracked_searches(43162)
    assert tracked_searches == [{
        "isActive": True,
        "trackedSearchId": "7188291",
        "preferredUrl": "https://www.conductor.com/",
        "queryPhrase": "conductor",
        "locationId": "1",
        "rankSourceId": "1",
        "deviceId": "1"
    }]


def test_get_categories(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        ss = AccountService(10550, api_key=mock_api_key, secret=mock_secret)
        categories = ss.get_categories()
    assert categories == [{
        "created": "2018-02-12T13:53:46.000Z",
        "trackedSearchIds": [],
        "modified": "2018-02-12T13:53:46.000Z",
        "name": "Intent - Early - Why"
    }]


def test_get_ranks(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        ss = AccountService(10550, api_key=mock_api_key, secret=mock_secret)
        ranks = ss.get_ranks(43162, 1, "CURRENT")
    assert ranks == [{
        "ranks": {"UNIVERSAL_RANK": None, "TRUE_RANK": 6, "CLASSIC_RANK": 3},
        "webPropertyId": 43162,
        "trackedSearchId": 7188291,
        "itemType": "ANSWER_BOX",
        "target": "",
        "targetDomainName": "conductor.com",
        "targetUrl": "https://www.conductor.com/blog"
    }]


def test_get_volume(mock_server):
    mock_url, mock_api_key, mock_secret = mock_server
    with patch.dict("conductor_api.client.__dict__", {"API_BASE_URL": mock_url}):
        ss = AccountService(10550, api_key=mock_api_key, secret=mock_secret)
        volume = ss.get_volume(43162, 1, "CURRENT")
    assert volume == [{
        "averageVolume": 135000,
        "trackedSearchId": 7188291,
        "volumeItems": []
    }]
