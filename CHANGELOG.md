# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Template
## [{version}] - {year-month-day}

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
-->

## [0.3.0] - 2026-03-22
### Added
- new `pre-commit` framework-based formatting and linting hooks,
- new `flake8`, `isort` pre-commit hooks,
- new `pyproject.toml` and `CHANGELOG.md` files.
- new basic CI pipelines,
### Changed
- enforced `flake8` recommendations,
- updated documentation.
### Removed
- removed `requirements.txt` in favour of .toml file project configuration.

## [0.2.0] - 2026-03-20
### Added
- new type casting checks for config object,
- new offset configuration ('top' effect down towards the middle, 'bottom' effect up towards the middle.),
- new text spacing configuration ('top' effect down towards the middle, 'bottom' effect up - towards the middle, 'center' effect 'interwoven'.),
- new docstring function descriptions,
- new custom CLI-based tests.
### Changed
- improved error handling,
- improved line wrapping (by reversing lists of strings for the 'bottom' effect.) ,
- minor refactoring of structures,
- updated documentation.

## [0.1.0] - 2025-02-02
### Added
- new venv-based environment setup,
- new config.ini file,
- new `argparse` CLI interface.
### Changed
- reworked the entire code into a Python script,
- cleaned up the project structure,
- updated documentation.

## [0.0.0] - 2024-06-16
### Added
- prototype in Jupyter Notebook
