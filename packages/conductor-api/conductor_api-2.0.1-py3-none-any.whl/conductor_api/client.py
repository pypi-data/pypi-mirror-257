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

import hashlib
import os
import time

import requests
from requests.adapters import HTTPAdapter, Retry

from .utils import week_number
from .errors import CredentialsMissingError

API_BASE_URL = "https://api.conductor.com"
TOKEN_REFRESH_TIMER = 290


class ConductorService:
    """A class for interacting with the Conductor API.

    This class provides methods for interacting with the Conductor API.
    Handles authentication, requests, and provides methods for retrieving
    data from the API
    """
    def __init__(self, api_key=None, secret=None, retries=1):
        """
        Initialize a new class using the API key and shared secret. If not provided, it attempts
        to fetch them from the environment and raises an error if none are found. Creates a Session object
        for API calls and requests all accounts associated with the key. An assertion is raised if none
        are found.

        Args:
            api_key (str, optional): The API key to use for authentication. Defaults to None.
            secret (str, optional): The shared secret to use for authentication. Defaults to None.
            retries (int, optional): The number of retries to make for a failed GET request. Defaults to 1
        Raises:
            CredentialsMissingError: If no API key or secret is provided or found in the environment variables.
            AssertionError: If no accounts are associated with the provided API key and secret.
        """
        self.__api_key = api_key or os.getenv("CONDUCTOR_API_KEY")
        self.__secret = secret or os.getenv("CONDUCTOR_SHARED_SECRET")
        if not self.__api_key:
            raise CredentialsMissingError(token="Conductor API Key")
        if not self.__secret:
            raise CredentialsMissingError(token="Conductor Shared Secret")

        self._retries = retries
        self.__sig = None
        self._timer = 0
        self._session = self._build_session()
        self._base_url = API_BASE_URL
        self._v3_url = f"{self._base_url}/v3"

        self.accounts = self.get_accounts()
        assert self.accounts, "API Key or Secret is not valid"

    def _build_session(self):
        """
        Builds and returns a session, with a built-in retry mechanism for
        specific status codes. [429, 500, 502, 503, 504]. The retry mechanism
        is set to a maximum of 2 times with a backoff factor of 1 second.
        """
        status_force_list = frozenset([429, 500, 502, 503, 504])
        session = requests.Session()
        retries = Retry(
            total=self._retries,
            backoff_factor=1,
            status_forcelist=status_force_list
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        return session

    def _generate_signature(self):
        """Generates API signature for request

        This method generates an API signature by hashing the API key,
        shared secret, and current epoch time.

        Returns:
            str: The hashed API signature
        """
        self._timer = time.time()
        return hashlib.md5(
            f"{self.__api_key}{self.__secret}{int(self._timer)}".encode()
        ).hexdigest()

    def _get_signature(self):
        """Get the current hashed API signature.

        If more than 290 seconds have passed since the last
        signature generation, a new hashed signature is generated

        Return:
            str: Valid current hashed signature
        """
        current_time = time.time()
        time_passed = current_time - self._timer
        if time_passed > TOKEN_REFRESH_TIMER:
            self.__sig = self._generate_signature()
        return self.__sig

    def _make_request(self, url, verify=True, redirects=True):
        """Makes a GET request to the Conductor API.

        This function makes a GET request to the Conductor API. If the
        status code returned is 400 or above, returns an HTTPError object.
        By default, a failed request will be retried 1 time. This can be changed
        when creating the instance of ConductorService

        Args:
            url (str): The URL to make the request to.
            verify (bool): Whether to verify the server's TLS certificate. Defaults to True.
            redirects (bool): Whether to follow redirects. Defaults to True.

        Returns:
            list[any]: A list of the responses from the server, or None if the request failed.
        """
        params = {"apiKey": self.__api_key, "sig": self._get_signature()}
        response = self._session.get(
            url,
            verify=verify,
            allow_redirects=redirects,
            params=params
        )
        response.raise_for_status()
        return response.json()

    # Conductor Configuration Data

    def get_locations(self):
        """Returns all locations supported by the Conductor API.

        Returns:
           list[dict]:  A list containing JSON responses of supported locations

        Example::

            [{
                'locationId': 1,
                'description': 'United States'
            }]
        """
        return self._make_request(
            f"{self._v3_url}/locations"
        )

    def get_rank_sources(self):
        """Returns all rank sources supported by the Conductor API.

        Returns:
           list[dict]: A list containing JSON responses of supported rank sources

        Example::

            [{
                'baseDomain': 'google.com',
                'description': 'Google (US / English)',
                'rankSourceId': '1',
                'name': 'GOOGLE_EN_US'
             }]
        """
        return self._make_request(
            f"{self._v3_url}/rank-sources"
        )

    def get_devices(self):
        """Returns all devices supported by the Conductor API.

       Returns:
           list[dict]: A list containing JSON responses of supported device types

       Example::

            {
                'description': 'Desktop',
                'deviceId': '1'
            }
        """
        return self._make_request(
            f"{self._v3_url}/devices"
        )

    # Conductor Account Data

    def get_accounts(self):
        """
        Returns all available Conductor accounts available associated with te
        API key and secret. Checks to see if accounts have already been fetched
        and stored within. If not, this makes a request to the Conductor API to
        fetch the accounts.
        """
        if hasattr(self, "accounts"):
            return self.accounts
        else:
            return self._make_request(
                f"{self._v3_url}/accounts"
            )


class AccountService(ConductorService):
    """A class for retrieving data from specific accounts.

     This class provides methods for interacting with the Conductor API and
     retrieving data from endpoints within a specific account. Endpoints include
     web property list, category list (keyword groups), tracked search list (keywords),
     web property rank report, and web property search volume report. Methods available
     to ConductorService are also available to this class.
     """
    def __init__(self, account_id, **kwargs):
        super().__init__(**kwargs)
        self.account_id = account_id
        assert any(acct["accountId"] == str(self.account_id) for acct in
                   self.accounts), "Invalid account ID. Confirm you have " \
                                   "access to this account"
    # Account Configuration Data

    def get_web_properties(self):
        """Retrieves all web properties associated with the account

        Returns:
           list[dict]: A list containing JSON responses of web property details

        Example::

            [{
                'reports': {
                    'CURRENT': {
                        'startDate': date (str),
                        'endDate': date (str),
                        'webPropertySearchVolumeReport': request_url (str),
                        'webPropertyRankReport': request_url (str),
                        'timePeriodId': id (str)
                    }
                },
                'rankSourceId': id (str)
            }]
        """
        return self._make_request(
            f"{self._v3_url}/accounts/{self.account_id}/web-properties"
        )

    def get_domain_name(self, web_property_id):
        """Retrieves the domain name for the specified web property

        Args:
            web_property_id (str): The ID of the web property to retrieve the domain name for

        Returns:
            str: The domain associated with the web property

        Raises:
            StopIteration: If the provided web property is not found
        """
        try:
            return next(wp["name"] for wp in self.get_web_properties()
                        if wp["webPropertyId"] == str(web_property_id))
        except StopIteration:
            raise StopIteration(
                f"Unable to find web property {web_property_id}"
            )

    def get_web_properties_for_domain(self, domain):
        """Returns the web properties for the specified domain

        This function retrieves the account's web properties and filters
        based on the provided domain.

        Args:
            domain (str): The domain name for which to fetch the web properties.

        Return:
            list[str]: A list of web property IDs for the given domain.

        Raises:
            StopIteration: If no web properties are found for the given domain.
        """
        wps = [wp["webPropertyId"] for wp in self.get_web_properties()
               if wp["name"] == domain]
        if not wps:
            raise StopIteration(
                f"Unable to find any web property for domain {domain}"
            )
        return wps

    def get_tracked_searches(self, web_property_id):
        """Retrieves all of an account's configured tracked keywords for the specified web property.

        Args:
            web_property_id (str): The ID of the web property to retrieve the search volume for.

        Returns:
            list[dict]: A list containing the JSON responses for configured tracked keywords.

        Example::

            [{
                'isActive': True,
                'trackedSearchId': '93342323',
                'preferredUrl': None,
                'queryPhrase': 'towels',
                'locationId': '1',
                'rankSourceId': '1',
                'deviceId': '3'
            }]"""
        return self._make_request(
            f"{self._v3_url}/accounts/{self.account_id}/web-properties/{web_property_id}/tracked-searches"
        )

    def get_categories(self):
        """Retrieves an account's active keyword groups (formerly called 'categories')
        and each group's tracked keywords (formerly called 'searches')

        Returns:
            list[dict]: A list containing the JSON responses of the active keyword groups (formerly categories)

        Example::

            [{
                 'created': '2023-05-17T18:10:23.637Z',
                 'trackedSearchIds': [64109775, 94110693],
                 'modified': '2023-05-17T18:10:23.637Z',
                 'name': '2023 Targeted Keywords'
             }]
            """
        return self._make_request(
            f"{self._v3_url}/accounts/{self.account_id}/categories"
        )

    # Collection Data

    def get_ranks(self, web_property_id, rank_source_id, date="CURRENT"):
        """Retrieves the ranks for the specified web property and rank source
        for a given date.

        Args:
            web_property_id (str): The ID of the web property to retrieve the search volume for.
            rank_source_id (str): The ID of the rank source to retrieve the search volume for.
            date (str): The date to retrieve the search volume for. Defaults to "CURRENT", which is the current date.

        Returns:
            list[dict]: A list of the JSON responses containing the rank data

        Example::

         [{
              'trackedSearchId': 53383270,
              'webPropertyId': None,
              'targetDomainName': 'www.amazon.com',
              'itemType': 'STANDARD_LINK',
              'target': 'Young Living Valor Essential Oil - Empowering Blend with a ...',
              'targetUrl': 'https://www.amazon.com/example',
              'ranks': {'TRUE_RANK': 3, 'UNIVERSAL_RANK': 2, 'CLASSIC_RANK': 2}
          }]
        """
        time_period = week_number(date) if date != "CURRENT" else date
        rank_endpoint = f"/{self.account_id}/web-properties/{web_property_id}/rank-sources/{rank_source_id}" \
                        f"/tp/{time_period}/serp-items"
        url = self._v3_url + rank_endpoint
        return self._make_request(url)

    def get_volume(self, web_property_id, rank_source_id, date="CURRENT"):
        """Retrieves search volume for the specified web property and rank source
        for a given date.

        Args:
            web_property_id (str): The ID of the web property to retrieve the search volume for.
            rank_source_id (str): The ID of the rank source to retrieve the search volume for.
            date (str): The date to retrieve the search volume for. Defaults to "CURRENT", which is the current date.

        Returns:
            list[dict]: A list of the JSON response containing the search volume data.

        Example::

         [{
              'averageVolume': 2900,
              'trackedSearchId': 53383249,
              'volumeItems': [{'volume': 1000, 'month': 7, 'year': 2023},
                              {'volume': 880, 'month': 6, 'year': 2023}]
         }]
         """
        time_period = week_number(date) if date != "CURRENT" else date
        search_volume_endpoint = f"/{self.account_id}/web-properties/{web_property_id}/rank-sources/{rank_source_id}" \
                                 f"/tp/{time_period}/search-volumes"
        url = self._v3_url + search_volume_endpoint
        return self._make_request(url)
