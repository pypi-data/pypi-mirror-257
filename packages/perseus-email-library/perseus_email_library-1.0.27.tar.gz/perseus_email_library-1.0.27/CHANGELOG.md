# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.27] - 2022-11-18
### Changed
- Add default MIME type of attached files

## [1.0.23] - 2022-01-03
### Changed
- Fix type mismatch when building Mailjet email attachment
- Fix encoding issue with message content

## [1.0.17] - 2022-01-02
### Added
- Support text files attachment to Mailjet email service provider

## [1.0.16] - 2021-08-19
### Changed
- Cleanse the subject of an email, removing unnecessary spaces and capitalizing the first word

## [1.0.15] - 2021-06-14
### Added
- Add localized HTML email templating

## [1.0.13] - 2021-06-14
### Added
- Complete code refactoring

## [1.0.12] - 2021-05-03
### Added
- Parse email from JSON expression

## [1.0.10] - 2021-02-20
### Changed
- Fix class `Email`'s constructor declaration
- Upgrade library dependencies
- Fix method `GmailService.__build_author_name_expr`

## [1.0.0] - 2021-02-21
### Added
- Initial import
