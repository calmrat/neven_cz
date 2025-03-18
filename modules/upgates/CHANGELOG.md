# CHANGELOG

## v0.1.3 (Latest - In Progress)
### Added
- Changelog :) Backfilled previous releases.
- Results validators to pydantic ai classes to ensure fields are filled.
- Improved loggings; added more logfire debug/info calls in upgates.
- Support for dynamically selecting target languages.
- CLI: upgates sync-parameters
  
### Fixed
- Bug: Multiple ssues with data synchronization.
- Bug: Application crash on startup.
- Bug: Double translating product due to invalid arguments

---

## v0.1.2 (Legacy)
### Added
- Implemented caching mechanisms to improve performance.

---

## v0.1.1 (Legacy)
### Added
- Enhanced logging for better debugging.
- Introduced new API endpoints for data retrieval.
  
### Fixed
- Corrected error message handling.
- Resolved session timeout issues.

---

## v0.1.0 (Legacy)
### Added
- Initial release with core functionalities.
- **Unified Configuration:**  
  Merged the previous separate config files into a single **config/__init__.py** file for centralized configuration management.
- **XMLHandler Enhancements:**  
  Integrated and refactored the new **XMLHandler** to parse Upgates XML data into our Pydantic models. Now supports nested sub‑objects (descriptions, categories, prices, images, parameters, metas, and variants).
- **New CLI Command:**  
  Added `sync_products_duckdb` in **upgates/cli.py** that triggers both the REST API sync and the XML feed import, then reports the total number of products in the DuckDB cache.
- **Translation Enhancements:**  
  Extended translation functionality by integrating asynchronous pydantic_ai support. New commands (`translate_product` and `save_translation`) allow translating product descriptions and saving updates back to the Upgates.cz API.
- **Improved Asynchronous Processing:**  
  Incorporated modern asyncio patterns (e.g., `asyncio.TaskGroup`) to concurrently fetch paginated data and reduce sync time.
- **Enhanced Logging and Error Handling:**  
  Improved log messages (using enhanced f‑string debugging) and fixed issues with translation updates in DuckDB.
- **Product Translation Commands:**  
  Introduced new CLI commands for product translation using pydantic_ai: `translate_product` and `save_translation`.
- **Async Translation Integration:**  
  Updated **upgates_client.py** to include asynchronous translation methods and integrated the pydantic_ai.Agent into the translation workflow.
- **XML Import Improvements:**  
  Enhanced the XML import process and upsert logic for product data from the XML feed.
- **Core Functionality Release:**  
  Released the initial version of Upgatescz API v0.4.0 with core features:
  - Data synchronization for products, customers, and orders via REST API.
  - Real-time updates using webhooks.
  - Periodic synchronization via a scheduler.
  - DuckDB caching for high-performance local data storage.
  - Basic CLI commands for managing sync operations, translation, and cache clearing.

### Fixed
- **Translation Update Bug:**  
  Resolved the conflict target error in DuckDB when updating translation fields.
- **Configuration Path Handling:**  
  Fixed issues related to finding and loading the configuration file.
- **Type Hinting and Task Management:**  
  Corrected minor type hinting issues and refactored asynchronous page fetches.
- **Logging Method Consistency:**  
  Replaced any unavailable logging calls (e.g. `logfire.success`) with standard `logfire.info`/`logfire.error` as appropriate.
- Applied initial bug fixes and performance improvements.
- **Logging Errors:**  
  Fixed errors related to logging (e.g. removal of non-existent `logfire.success`).
- **Minor REST Sync Bugs:**  
  Addressed issues with data retrieval and upsert operations during sync.
- **Initial Bug Fixes:**  
  Addressed several bugs and performance issues present in earlier prototype versions.

---
