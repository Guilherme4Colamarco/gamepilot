# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-05-06

### Added
- Complete rewrite from Rust to Python
- TUI using Textual framework
- Game detection for Steam and Heroic Games Store
- Dependency management via winetricks
- Nexus Mods API integration for automatic mod downloads
- Desktop shortcut creation with .desktop files
- Internationalization support (English, Portuguese, Spanish, Italian, Russian)
- Configuration management with TOML
- Mod manifest system for game-specific tools
- Async subprocess handling for Wine operations
- Comprehensive test suite

### Changed
- Replaced all Rust src/ with Python gamepilot/ package
- Updated build system to use PyInstaller and Makefile
- Updated documentation accordingly

