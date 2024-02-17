# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2023-09-21

### Changes
- Changed the base URL for the API endpoint to the correct version.
- Changed all reference to previous product name, 'Searchlight' to 'Conductor'.
  - The SearchlightService class was renamed to ConductService as part of this.

### Added
- Implemented a 5-minute token refresh mechanism.
- Code enhancements for efficiency and readability.
- Added docstrings to all code for better understanding and readability.

### Removed
- Removed backwards compatibility with Python 2. This project now requires Python 3 or later.
- Removed the error handling functionality from GET request to allow end-users to handle errors.

## [1.0.0] - 2019-05-17

### Added
- Initial stable release

## [0.0.1] - 2019-02-19

### Added
- Initial release