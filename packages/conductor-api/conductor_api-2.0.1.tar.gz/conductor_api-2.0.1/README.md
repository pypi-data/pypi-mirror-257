# conductor-api-client-python
![Latest Version](https://img.shields.io/pypi/v/searchlight-api.svg)

The Conductor API Client is a Python package that makes it easy to authenticate with and retrieve data from the Conductor API.

## Getting Started

### Installation

The latest released version can be installed through the Python package index.

```
pip install conductor-api
```

### Dependencies

* [Requests](http://docs.python-requests.org/en/master/): 2.19.1 or higher

### Authentication
The Conductor API Client needs to know your API Key and API Secret to authenticate with Conductor. It can find these in one of two ways:
* Add the credentials to your environmental variables (preferred)
    * MacOS / Linux: Edit your .bash_profile to include the lines
        * export CONDUCTOR_API_KEY=xxxxx
        * export CONDUCTOR_SHARED_SECRET=xxxxx
    * Windows: Add CONDUCTOR_API_KEY and CONDUCTOR_SHARED_SECRET in the [Environment Variables in the Advanced system settings](https://docs.microsoft.com/en-us/windows/desktop/procthread/environment-variables)
* Pass the credentials when instantiating the API Client
    from conductor_api.client import AccountService
    account_service = AccountService(api_key=xxxxx, secret=xxxxx)

To access your API Key and Secret please navigate to the Settings section in the Conductor platform or reach out to [Conductor Support](mailto:support@conductor.com)

### Using conductor_api

The Conductor API Package has two main functionalities: **client** and **analysis**
* **client** provides an SDK around the Conductor REST API, making it easy to request the data that you need from your accounts.
* **analysis** includes functions for aggregating data (Rank and Search Volume) using the Conductor API.

#### Examples

##### Client

###### ConductorService
The ConductorService client provides wrappers for getting Conductor and profile configuration data
```
from conductor_api import client

# instantiate Conductor client
cs = client.ConductorService(api_key="xxxxxxx", secret="xxxxxx")
# Retrieve all Conductor accounts you have access to.
# You can use this to retrieve Account IDs to instantiate the AccountService client

my_accounts = cs.get_accounts()
print(my_accounts)
[{'accountId': 'XXXX',
  'isActive': False,
  'name': 'Account 1',
  'webProperties': 'https://api.conductor.com/v3/accounts/XXXX/web-properties'},
 {'accountId': 'YYYY',
  'isActive': True,
  'name': 'Account 2',
  'webProperties': 'https://api.conductor.com/v3/accounts/YYYY/web-properties'}]

# Account IDs can also be found in Conductor URLs: https://api.conductor.com/YYYY/insight-stream
```

In Conductor, keywords can be tracked across different Rank Sources (or Search Engines), Locations and Devices.
You can retrieve what's supported with the following:

```
rank_sources = cs.get_rank_sources()
locations = cs.get_locations()
devices = cs.get_devices()
```

###### AccountService
The AccountService client provides functionality for retrieving reporting data from Conductor accounts, while retaining 
all the functionality found in the ConductorService client. A Conductor account id is required upon instantiation.
```
from conductor_api import client
# instantiate the AccountService client
account_service = client.AccountService(YYYY, api_key="xxxxxxx", secret="xxxxxx")
# retrieve all web properties tracked in the account
web_properties = account_service.get_web_properties()

web_property_id = web_properties[0]['webPropertyId']

# the web_property_id can be used to get the name of the corresponding domain
domain_name = account_service.get_domain_name(web_property_id)

# use the web_property_id to get all tracked searches in the account
tracked_searches = account_service.get_tracked_searches(web_property_id)

# get a rank_source_id that the web_property is tracked against
rank_source_id = web_properties[0]['rankSourceInfo'][0]['rankSourceId']

# retrieve rank data for searches tracked against a web property and rank source for a given date within a reporting interval.
# by default the current date is used.
ranks = account_service.get_ranks(web_property_id, rank_source_id, date='2019-01-12')

# retrieve search volume data for searches tracked against a web property and rank source for a given date within a reporting interval.
# by default the current date is used.
search_volume = account_service.get_volume(web_property_id, rank_source_id, date='2019-01-12')
```

##### Analysis
Analysis allows you to use the AccountService client to aggregate reporting data across an entire account for a given date.

```
from conductor_api.client import AccountService
from conductor_api import analysis

account_service = AccountService(YYYY, api_key="xxxxxxx", secret="xxxxxx")

rank_data = analysis.rank_data(account_service, date='2019-01-12')
search_volume = analysis.search_volume(account_service)
```

##### Using Pandas with Conductor API Client

```
from conductor_api import client, analysis
import pandas as pd

# instantiate AccountService object
account_service = client.AccountService(YYYY, api_key="xxxxxxx", secret="xxxxxx")

# get rank sources, locations and devices and turn to dfs
rank_source_df = pd.DataFrame(account_service.get_rank_sources())
location_df = pd.DataFrame(account_service.get_locations())
device_df = pd.DataFrame(account_service.get_devices())

# get the tracked searches and turn into a df
tracked_search_df = pd.DataFrame(analysis.all_tracked_searches(account_service))

# turn search_volume and rank_data to Data Frames
search_volume_df = pd.DataFrame(analysis.search_volume(account_service))
rank_data_df = pd.DataFrame(analysis.rank_data(account_service))

report = pd.merge(rank_data_df, search_volume_df, on=['trackedSearchId', 'rankSourceId', 'webPropertyId'])
report = report.merge(rank_source_df, on='rankSourceId', how='left')
print(report.head())
       itemType rankSourceId  standardRank target           targetDomainName  \
0    ANSWER_BOX            1           3.0                        example.com
1  IMAGE_RESULT            1           NaN                        example.com
2  LOCAL_RESULT            1           NaN         www.organiccompetitor.com
3  LOCAL_RESULT            1           NaN         www.organiccompetitor.com
4  LOCAL_RESULT            1           NaN         www.organiccompetitor.com
                                           targetUrl  targetWebPropertyId  \
0  https://www.example.com/subfolder1/             43162.0
1  https://www.example.com/subfolder2/...             43162.0
2  http://www.organiccompetitor.com/subfolder...                 NaN
3  http://www.organiccompetitor.com/subfolder/...                 NaN
4  http://www.organiccompetitor.com/subfolder/...                 NaN
   trackedSearchId  trueRank webPropertyId  averageVolume  \
0          7188291         6         43162         135000
1          7188291        62         43162         135000
2          7188291         4         43162         135000
3          7188291         2         43162         135000
4          7188291         3         43162         135000
                                         volumeItems  baseDomain  \
0  [{'volume': 165000, 'month': 11, 'year': 2018}...  google.com
1  [{'volume': 165000, 'month': 11, 'year': 2018}...  google.com
2  [{'volume': 165000, 'month': 11, 'year': 2018}...  google.com
3  [{'volume': 165000, 'month': 11, 'year': 2018}...  google.com
4  [{'volume': 165000, 'month': 11, 'year': 2018}...  google.com
             description          name deviceId  isActive locationId  \
0  Google (US / English)  GOOGLE_EN_US        1      True          1
1  Google (US / English)  GOOGLE_EN_US        1      True          1
2  Google (US / English)  GOOGLE_EN_US        1      True          1
3  Google (US / English)  GOOGLE_EN_US        1      True          1
4  Google (US / English)  GOOGLE_EN_US        1      True          1
             preferredUrl queryPhrase
0  http://www.example.com/     example phrase
1  http://www.example.com/     example phrase
2  http://www.example.com/     example phrase
3  http://www.example.com/     example phrase
4  http://www.example.com/     example phrase
```
