# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-05-18

### Added
- Python package `gamepilot/` with TUI based on Textual
- Game scanning for Steam and Heroic installs
- Wine / winetricks helper flow for dependency installation
- Nexus Mods integration for tool downloads
- Desktop shortcut generation via `.desktop`
- Internationalization support for EN, PT, ES, IT and RU
- Packaging pipeline with PyInstaller
- Automated tests for core flows and shortcut generation

### Changed
- Replaced the old Rust application with the Python implementation
- Simplified the project layout and build workflow
- Standardized the developer entry points around `make setup`, `make run`, `make test` and `make build`
- Updated documentation to match the Python codebase

### Fixed
- Removed stale Rust-era documentation assumptions
- Aligned the README with the current project structure and commands

## [0.1.0] - 2026-05-18

### Added
- Initial Python rewrite of GamePiLot
- Textual-based TUI
- Manifest-driven game/tool configuration
- `gamepilot` console script and `python -m gamepilot` entry point
- Basic developer scripts and test suite
