from unittest.mock import Mock, patch

from conductor_api.analysis import search_volume, rank_data, all_tracked_searches


class MockAccountService:
    def __init__(self, account_id):
        self.account_id = account_id


def test_search_volume():
    # Mocking the account_service methods and return values
    mock_service = Mock()
    mock_service.get_web_properties.return_value = [
        {
            "webPropertyId": "property1",
            "rankSourceInfo": [{"rankSourceId": "source1"}, {"rankSourceId": "source2"}]
        },
        {
            "webPropertyId": "property2",
            "rankSourceInfo": [{"rankSourceId": "source3"}]
        }
    ]
    mock_service.get_volume.side_effect = [
        [{"volume": 100}, {"volume": 200}],
        [{"volume": 150}],
        [{"volume": 75}],
    ]

    # Using patch to mock the sleep method (so we don't actually sleep during tests)
    with patch("conductor_api.analysis.time.sleep", return_value=None):  # Adjust the import path as needed
        result = search_volume(mock_service)

    # Expected result based on the mock data
    expected = [
        {"volume": 100, "webPropertyId": "property1", "rankSourceId": "source1"},
        {"volume": 200, "webPropertyId": "property1", "rankSourceId": "source1"},
        {"volume": 150, "webPropertyId": "property1", "rankSourceId": "source2"},
        {"volume": 75, "webPropertyId": "property2", "rankSourceId": "source3"}
    ]

    assert result == expected


def test_rank_data():
    # Mocking the account_service methods and return values
    mock_service = Mock()
    mock_service.get_web_properties.return_value = [
        {
            "webPropertyId": "property1",
            "rankSourceInfo": [{"rankSourceId": "source1"}, {"rankSourceId": "source2"}]
        },
        {
            "webPropertyId": "property2",
            "rankSourceInfo": [{"rankSourceId": "source3"}]
        }
    ]
    mock_service.get_ranks.side_effect = [
        [{"ranks": {"CLASSIC_RANK": 1, "TRUE_RANK": 5}, "webPropertyId": "wp1"}],
        [],
        [{"ranks": {"CLASSIC_RANK": 2, "TRUE_RANK": 7}, "webPropertyId": "wp2"}]
    ]

    # Using patch to mock the sleep method
    with patch("conductor_api.analysis.time.sleep", return_value=None):  # Adjust the import path as needed
        result = rank_data(mock_service)

    # Expected result based on the mock data
    expected = [
        {
            "targetWebPropertyId": "wp1",
            "rankSourceId": "source1",
            "standardRank": 1,
            "trueRank": 5,
            "webPropertyId": "property1"
        },
        {
            "targetWebPropertyId": "wp2",
            "rankSourceId": "source3",
            "standardRank": 2,
            "trueRank": 7,
            "webPropertyId": "property2"
        }
    ]

    assert result == expected


def test_all_tracked_searches():
    # Mocking the account_service methods and their return values
    mock_service = Mock()
    mock_service.get_web_properties.return_value = [
        {
            "webPropertyId": "property1"
        },
        {
            "webPropertyId": "property2"
        }
    ]
    mock_service.get_tracked_searches.side_effect = [
        [{"trackedSearchId": "123"}, {"trackedSearchId": "456"}],
        [{"trackedSearchId": "789"}]
    ]

    # Using patch to mock the sleep method
    with patch("conductor_api.analysis.time.sleep", return_value=None):  # Adjust the import path as needed
        result = all_tracked_searches(mock_service)

    # Expected result based on the mock data
    expected = [
        {
            "trackedSearchId": 123,
            "webPropertyId": "property1"
        },
        {
            "trackedSearchId": 456,
            "webPropertyId": "property1"
        },
        {
            "trackedSearchId": 789,
            "webPropertyId": "property2"
        }
    ]

    assert result == expected
