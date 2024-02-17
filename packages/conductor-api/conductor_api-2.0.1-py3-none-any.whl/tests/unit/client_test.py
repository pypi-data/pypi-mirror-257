from unittest.mock import patch


@patch("conductor_api.client.ConductorService")
def test_get_locations(MockConductorService):
    ss = MockConductorService()
    ss.get_locations.return_value = [{
        "locationId": "1",
        "description": "United States"
    }]
    data = ss.get_locations()
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.ConductorService")
def test_get_rank_sources(MockConductorService):
    ss = MockConductorService()
    ss.get_rank_sources.return_value = [{
        "baseDomain": "google.com",
        "description": "Google (US / English)",
        "rankSourceId": "1",
        "name": "GOOGLE_EN_US"
    }]
    data = ss.get_rank_sources()
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.ConductorService")
def test_get_devices(MockConductorService):
    ss = MockConductorService()
    ss.get_devices.return_value = [{
        "locationId": "1",
        "description": "Desktop",
        "deviceId": "1",
    }]
    data = ss.get_devices()
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.ConductorService")
def test_get_accounts(MockConductorService):
    ss = MockConductorService()
    ss.get_accounts.return_value = [{
        "isActive": True,
        "accountId": "10550",
        "webProperties": "https://api.conductor.com/v3/accounts/"
                         "10550/web-properties",
        "name": "PS Reporting Test",
    }]
    data = ss.get_accounts()
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.AccountService")
def test_get_web_properties(MockAccountService):
    ss = MockAccountService(10550)
    ss.get_web_properties.return_value = [{
        "isActive": True,
        "rankSourceInfo": [],
        "webPropertyId": "43162",
        "trackedSearchList": "https://api.conductor.com/v3/accounts/10550/"
                             "web-properties/43162/tracked-searches",
        "name": "conductor.com"
    }]
    data = ss.get_web_properties()
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.AccountService")
def test_get_domain_name(MockAccountService):
    ss = MockAccountService(10550)
    ss.get_domain_name.return_value = "conductor.com"
    domain_name = ss.get_domain_name(43162)
    assert domain_name is not None
    assert isinstance(domain_name, str)


@patch("conductor_api.client.AccountService")
def test_get_web_properties_for_domain(MockAccountService):
    ss = MockAccountService(10550)
    ss.et_web_properties_for_domain.return_value = [43162]
    wps = ss.et_web_properties_for_domain()
    assert wps is not None
    assert isinstance(wps[0], int)


@patch("conductor_api.client.AccountService")
def test_get_tracked_searches(MockAccountService):
    ss = MockAccountService(10550)
    ss.get_tracked_searches.return_value = [{
        "isActive": True,
        "trackedSearchId": "7188291",
        "preferredUrl": "http://www.conductor.com/",
        "queryPhrase": "conductor",
        "locationId": "1",
        "rankSourceId": "1",
        "deviceId": "1"
    }]
    data = ss.get_tracked_searches(43162)
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.AccountService")
def test_get_categories(MockAccountService):
    ss = MockAccountService(10550)
    ss.get_categories.return_value = [{
        "created": "2018-02-12T13:53:46.000Z",
        "trackedSearchIds": [],
        "modified": "2018-02-12T13:53:46.000Z",
        "name": "Intent - Early - Why"
    }]
    data = ss.get_categories()
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.AccountService")
def test_get_ranks(MockAccountService):
    ss = MockAccountService(10550)
    ss.get_ranks.return_value = [{
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
    data = ss.get_ranks(43162, 1, "CURRENT")
    assert data is not None
    assert isinstance(data[0], dict)


@patch("conductor_api.client.AccountService")
def test_get_volume(MockAccountService):
    ss = MockAccountService(10550)
    ss.get_volume.return_value = [{
        "averageVolume": 135000,
        "trackedSearchId": 7188291,
        "volumeItems": []
    }]
    data = ss.get_volume(43162, 1, "CURRENT")
    assert data is not None
    assert isinstance(data[0], dict)
