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

import datetime
import math

EPOCH = datetime.datetime.strptime("2009-07-26", "%Y-%m-%d")


def week_number(date_string):
    """Convert a date string in the ISO 8601 format to a Conductor Time Period Number.

      Args:
        date_string (str): A string representing a date in the ISO 8601 format (i.e. YYYY-MM-DD)

      Returns:
        int: The Conductor Time Period Number corresponding to the input date.

      Raises:
        ValueError: If the input date does not match the format YYYY-MM-DD or another ISO 8601 date format."""
    try:
        date = datetime.datetime.fromisoformat(date_string)
    except ValueError:
        raise ValueError(f"Invalid isoformat date string for {date_string}") from None
    return math.ceil((date - EPOCH).days / 7)
