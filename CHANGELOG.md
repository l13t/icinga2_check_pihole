# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0](https://github.com/l13t/icinga2_check_pihole/compare/v0.4.1...v1.0.0) (2025-03-31)


### ⚠ BREAKING CHANGES

* Updated code with dedicated getting sid and logout functions so we're not hitting limit on connections
to Pi-Hole API.
* switched from urllib3 to requests library and removed json as obsolete

### Features

* Refactored code and changed libraries ([#14](https://github.com/l13t/icinga2_check_pihole/issues/14)) ([14adeca](https://github.com/l13t/icinga2_check_pihole/commit/14adeca99298d3cb85acf2d1b125e332b71aeff5))

## [0.4.1](https://github.com/l13t/icinga2_check_pihole/compare/v0.4.0...v0.4.1) (2025-03-31)


### Bug Fixes

* Updated get sid process and extended error output ([#13](https://github.com/l13t/icinga2_check_pihole/issues/13)) ([79c6553](https://github.com/l13t/icinga2_check_pihole/commit/79c6553a3a48b78c5e525924a2f91de39d50fe39))

## [0.4.0](https://github.com/l13t/icinga2_check_pihole/compare/v0.3.0...v0.4.0) (2025-03-27)


### Features

* Updated code for v6 support ([f91e6ed](https://github.com/l13t/icinga2_check_pihole/commit/f91e6ed86b9d1ac025138044ae71ff30be0522b7))


### Bug Fixes

* Added missing release configuration ([18ed58e](https://github.com/l13t/icinga2_check_pihole/commit/18ed58ee630317b381ff66ba830e0afaee230f62))
* Updated readme and removed apilog in help ([#11](https://github.com/l13t/icinga2_check_pihole/issues/11)) ([ce941aa](https://github.com/l13t/icinga2_check_pihole/commit/ce941aaedb0b1efcf86d9fc51f93194040c51b38))
