"""
Copyright 2019 Conductor, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import time

from .client import AccountService


def search_volume(account_service: AccountService, date="CURRENT"):
    """This function makes a get request for keyword search volume across all web properties and rank sources in the
    account and aggregates them.

    This function fetches all web properties for the account designated via the AccountService instance
    and extracts the web_property_ids and rank_source_ids. This is then used to query the 'Web Property Search
    Volume' endpoint for monthly search volume data of the tracked keywords. The web_property_id and rank_source_id
    are inserted into each returned dictionary and then appended to a list.

    Args:
        account_service (object): The account service to retrieve web properties and search volume data from.
        date (str, optional): Date string in format YYYY-MM-DD. Defaults to "CURRENT" if none is entered
    Returns:
        list[dict]: A list of dictionaries containing search volume data for all tracked keywords across the account
    """
    web_properties = account_service.get_web_properties()
    volumes_list = []
    for web_property in web_properties:
        web_property_id = web_property["webPropertyId"]
        rank_sources = [rank_source["rankSourceId"] for rank_source in web_property["rankSourceInfo"]]
        for rank_source_id in rank_sources:
            msv = account_service.get_volume(web_property_id, rank_source_id, date)
            time.sleep(.5)
            if not msv:
                continue
            for m in msv:
                m.update({"webPropertyId": web_property_id, "rankSourceId": rank_source_id})
            volumes_list.extend(msv)
    return volumes_list


def rank_data(account_service: AccountService, date="CURRENT"):
    """
    This function makes a get request for keyword rank data across all web properties and rank sources in the account
    and aggregates them.

    The function first fetches all web property data for the account designated via the AccountService instance
    and extracts the web_property_ids and rank_source_ids. This is then used to query the 'Web Property Rank' endpoint
    for rank data of tracked keywords. The web_property_id and rank_source_id is inserted into each returned
    dictionary and then appended to a list.

    Args:
        account_service (object): The account service to retrieve web properties and rank data from.
        date (str, optional): Date string in format YYYY-MM-DD. Defaults to "CURRENT" if none is entered
    Returns:
        list[dict]: A list of dictionaries containing rank data for all tracked keywords across the account.
    """
    web_properties = account_service.get_web_properties()
    ranks_list = []
    for web_property in web_properties:
        web_property_id = web_property["webPropertyId"]
        rank_sources = [rank_source["rankSourceId"] for rank_source in web_property["rankSourceInfo"]]
        for rank_source_id in rank_sources:
            ranks = account_service.get_ranks(web_property_id, rank_source_id, date)
            time.sleep(.5)
            if not ranks:
                continue
            for r in ranks:
                r["targetWebPropertyId"] = r["webPropertyId"]
                r.update({"rankSourceId": rank_source_id,
                          "standardRank": r["ranks"]["CLASSIC_RANK"],
                          "trueRank": r["ranks"]["TRUE_RANK"],
                          "webPropertyId": web_property_id})
                r.pop("ranks", None)
            ranks_list.extend(ranks)
    return ranks_list


def all_tracked_searches(account_service: AccountService):
    """This function makes a get request for tracked keywords for all web properties in the account
    and aggregates them.

    The function first fetches all web property data for the account designated via the AccountService instance
    and extracts the web_property_ids. This is then used to query the 'Tracked Search List' endpoint
    for all tracked keywords. The web_property_id is inserted into each returned
    dictionary and then appended to a list.

    Args:
        account_service (object): The account service to retrieve web properties and all tracked keywords from.
    Returns:
        list[dict]: A list of dictionaries containing all tracked keywords and details across the account.
    """

    web_properties = account_service.get_web_properties()
    tracked_search_list = []
    for web_property in web_properties:
        web_property_id = web_property["webPropertyId"]
        tracked_searches = account_service.get_tracked_searches(web_property_id)
        time.sleep(.5)
        if not tracked_searches:
            continue
        for ts in tracked_searches:
            ts["trackedSearchId"] = int(ts["trackedSearchId"])
            ts.update({"webPropertyId": web_property_id})
        tracked_search_list.extend(tracked_searches)
    return tracked_search_list
