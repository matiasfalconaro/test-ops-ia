# CHANGELOG

## Versioning System
This project follows Semantic Versioning 2.0.0:
- MAJOR version (x): Breaking changes, major functionality shifts, and
  significant refactoring
- MINOR version (y): New features, important improvements, and substantial
  enhancements
- PATCH version (z): Bug fixes, minor improvements, documentation updates,
  and hot-fixes

### Version Format
[x.y.z] - yyyy-mm-dd - [ENVIRONMENT/TYPE]

Where:
`x.y.z`: Semantic version number (MAJOR.MINOR.PATCH)
`yyyy-mm-dd`: Date when the version was released

`[ENVIRONMENT/TYPE]`: Deployment context or deliverable type:
[POC]: Proof-of-Concept
[MVP]: Minimum-Viable-Product
[DEV]: Development-environment
[QAS]: Quality-Assurance/Testing
[UAT]: User-Acceptance-Testing
[PRD]: Production-environment
[ALPHA]: Alpha-release
[BETA]: Beta-release
[RC]: Release-Candidate

## Branching
1. Crear un issue con el nombre de la versión
   #1 "vw.y.z"
2. Crear la rama con el nombre de la versión
   `git branch vx.y.z`
3. Commits durante el desarrollo
4. Squash con rebase antes del merge
   (commits) ──► "vx.y.z"
5. Actualizar el changelog
6. Pull Request de la versión
7. Merge a main
8. Tag en Git
   "vx.y.z"
9. Push del tag a GitHub

```
 Issue ──► Branch ──► Commits ──► Squash ──► Changelog ──► PR ──► Merge ──► Tag
 vx.y.z    vx.y.z                 vx.y.z                  vx.y.z            vx.y.z   
```

### Change Types
- `Added`: New features, endpoints, models, or functionality
- `Changed`: Modifications to existing functionality
- `Deprecated`: Features that will be removed in future releases
- `Removed`: Features that have been deleted
- `Fixed`: Bug fixes and error corrections
- `Security`: Vulnerability patches and security improvements

# #############################################################################

## [0.1.1] - 2025-09-17 - [POC]
### Changed
- `docker.sh` script refactored and optimized:
 - Replaced repetitive error handling with a unified `run_cmd()` helper.
 - Consolidated container actions (start, stop, rm) into a single
   `container_action()` function.
 - Eliminated individual boolean flags for options, enabling direct execution
   from command-line arguments.
 - Added Docker installation check and portable color support for terminals
   without ANSI codes.
 - Improved readability and maintainability, while keeping all previous
   functionalities intact.
- Refactored `Dockerfile` commands to improve readability.

## [0.1.0] - 2025-09-16 - [POC]
### Added
- Version Management: Added `version.txt` file and version property in Settings
  class to read version from file
- New API Endpoints:
    - `/scrape/custom/` - Custom scraping with extraction rules
    - `/scrape/batch/` - Batch processing of multiple scrape requests
- Data Models: Created new Pydantic models in `./app/models/`:
    - `ExtractionRule` - Defines CSS selectors and extraction types
    - `CustomScrapeRequest` - Request model for custom scraping
    - `BatchScrapeRequest` - Request model for batch operations
    - `ExtractType Enum` - Defines extraction types (text, attribute, html)
- Screenshot Features:
    - Added save_screenshot option to save screenshots as PNG files
    - Automatic screenshot directory creation (`./app/screenshots/`)
    - Filename generation with timestamp and sanitized URL
- Enhanced Scraping Capabilities:
    - `extract_with_rules()` method for custom data extraction
    - Support for text, attribute, and HTML extraction
    - Batch processing with parallel execution option
- Docker Management Script: Added comprehensive `docker.sh` script with:
    - Color-coded output for better visibility
    - Complete container lifecycle management (build, run, start, stop, remove)
    - Log viewing and container execution capabilities
    - File copying functionality from container to host
    - Image management and cleanup utilities
    - Help system with usage examples

### Changed
- Configuration: Updated Settings class with cached property for version reading
- API Structure: Refactored routes to use centralized models from app.models
- Scraper Service: Enhanced SeleniumScraper class with:
    - Improved screenshot handling with file saving
    - New `custom_scrape()` method for rule-based extraction
    - Reusable `_get_page_data()` internal method
    - Better error handling and logging
- Request Models: Added save_screenshot field to scrape requests
- Response Format: Extended response data with screenshot paths and extracted
  data

### Fixed
- Improved error handling throughout the application
- Better resource management for screenshot storage
- Enhanced URL parsing and filename sanitization

### Technical Details
- Added cached_property dependency for efficient version reading
- Implemented `base64` decoding for PNG file saving
- Added timestamp-based filename generation to prevent conflicts
- Created modular model structure with `__all__` exports for clean imports

## [0.0.0] - Initial Release - [POC]
### Basic FastAPI application with Selenium integration
- Simple scraping endpoint with basic page data extraction
- Health check and screenshot endpoints
- Configuration management with environment variables
- Headless Chrome driver setup for Linux environments

### Features
- Single endpoint scraping with URL and CSS selector waiting
- Basic page data extraction (title, links, text content)
- Base64 screenshot capture
- Environment-based configuration
- Proper driver lifecycle management
