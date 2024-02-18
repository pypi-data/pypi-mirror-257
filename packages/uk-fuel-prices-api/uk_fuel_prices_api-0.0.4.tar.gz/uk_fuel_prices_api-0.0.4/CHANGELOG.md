# Changelog

All notable changes to this project will be documented in this file.

## [0.0.4] - 2024.-02.18

### Changed
- Updated README
- Reverted required python version to >=3.10

## [0.0.3] - 2024-02-18

### Added

- This Changelog file!
- ```distance``` static method to calculate distance between two lat, lng points, and ```test_distance``` test
- Added ```stationWithinRadius``` to return all stations within a given distance of a lat, lng point, and ```test_stationsWithinRadius``` test

### Changed

- Moved API code to \_\_init\_\_.py to prevent clumsy imports
- Renamed ```nearest``` to ```nearestN``` to fetch the nearest N stations to a lat, lng point

### Removed

### Fixed




[//]: <> (
    Added for new features.
    Changed for changes in existing functionality.
    Deprecated for soon-to-be removed features.
    Removed for now removed features.
    Fixed for any bug fixes.
    Security in case of vulnerabilities.)