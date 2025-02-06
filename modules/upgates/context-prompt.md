🚀 Upgatescz API - System Prompt for Python 3.12 Development 🚀

📌 Project Overview

Upgatescz API is an asynchronous, fully automated system designed to sync products, customers, orders, and parameters from the Upgates.cz e-commerce platform. It utilizes DuckDB caching, Pydantic AI for structured AI-driven translations, and OpenAI GPT-4o-mini for product language translation.

The project supports webhooks, scheduled jobs, CLI-based management, batch syncing, configurable storage paths, and optimized API request handling to minimize external requests while keeping the system up-to-date efficiently.

🛠️ Development & Environment
	•	Python Version: 3.12+
	•	Database: DuckDB (for caching, analytics, and API efficiency)
	•	Async API Calls: aiohttp (ensuring parallel request execution)
	•	CLI Framework: Click
	•. Pydantic 2+ Datamodels
	•	AI-Powered Translation: Pydantic AI using GPT-4o-mini (default, but customizable)
	•	Logging: Pydantic Logfire (structured logs for debugging, info, and warnings)
         logfire.configure() configurable default project name: neven-agents (pyproject.toml)
         prefix debug messages ℹ️ for info ⚠️ for warn ❌ for Error
         Use all levels appropriately for inspection and clarity: debug info notice error fatal
	•	Package Management: UV (astral-sh) (preferred over pip for performance)
	•	Containerization: Docker (ensuring consistent execution across environments)
	•	Configurable Storage: .config/config.toml (stored separately from code)
	•	mkdirs automatically if not exists (eg, data, cache paths)

🔹 Current Features & Functionalities

✅ Data Sync & Storage
	•	Supports full synchronization of:
	•	Products
	•	Customers
	•	Orders
	•	Parameters
	•	Uses DuckDB caching for efficient API query management.
	•	Batch syncing with parallel execution (configurable batch size & concurrency).
	•	Incremental sync (updates only new or modified items).

✅ AI-Powered Product Translation
	•	Uses OpenAI GPT-4o-mini for structured product description translation.
	•	Default translation fields:
	•	Long Description
	•	Short Description
	•	SEO Title
	•	SEO Description
	•	SEO Keywords
	•	Default Source Language: CZ 🇨🇿 (configurable per product).
	•	Default Target Language: SK 🇸🇰 (configurable by user).
	•	Translation context includes: Product Title + Long Description + Selected Fields for accuracy.
	•	AI model selection is dynamic:
	•	If the model starts with "gpt-", then OpenAI API key is loaded.
	•	Otherwise, the OpenAI key is not used.

✅ CLI & Webhook Support
    CLI Options: 
	•	debug level ('debug', 'info', 'warning')
	CLI Commands:
	•	sync_all → Syncs all supported data.
	•	sync_products → Syncs products and parameters.
	•	sync_customers → Syncs customers.
	•	sync_orders → Syncs orders.
	•	translate_product → Translates product descriptions for a given language.
	•	start_webhook → Starts webhook server.
	•	start_scheduler → Starts scheduled auto-sync.
	•	init_config → Prompts user for missing config values and saves to .config/config.toml.
	
     Webhook Event Handling:
	•	product.updated → S yncs product changes.
	•	customer.updated → Syncs customer changes.
	•	order.updated → Syncs order updates.

✅ Optimized API Handling
	•	Authentication: Uses HTTP Basic Auth (login + api_key).
	•	Retries on failed API calls with exponential backoff.
	•	SSL verification is configurable (default: enabled, but can be disabled via config).
	•	Logs API call statistics to DuckDB for monitoring and performance analysis.

✅ Configurable Paths & Storage
	•	Default storage path: ./data (configurable via .env).
	•	Parallel batch processing configurable in config.toml.
	•	Backups stored in ./data/backups/.
	•	Configuration file stored separately in .config/config.toml.
	•	User prompted to initialize missing config values (CLI init_config ensures all values are set).

📌 Development Preferences & Coding Style
	•	Keep all features intact when refactoring – prioritize retention of existing logic.
	•	Prefer modular, object-oriented design with clear separation of concerns.
	•	Minimize unnecessary comments but ensure logs and debug messages are meaningful.
	•	Use Pydantic AI models for structured API responses and validation. Use Pydantic Tools,  Dependency Injection, @systemprompt decorators. 
	•	Avoid excessive API calls by caching results in DuckDB.
	•	Ensure all CLI commands work asynchronously.
	•	Enable debugging logs selectively using logfire.
	•	Ensure OpenAI API key is only used if a GPT model is selected.
	•	Always update version numbers in pyproject.toml and # path/filename v0.0.0 footer comments.
	•	The VERSION in upgates_client.py and pyproject.toml should always be updated to match.
	•   Simple docstrings and inline comments to explain less obvious details. 
	•   Prefer using type declarations.

🚀 Future Enhancements & Priorities
	1.	Improve AI translation accuracy (fine-tune prompt construction).
	2.	Enhance DuckDB indexing for faster queries.
	3.	Add full CI/CD pipeline (automated testing, deployment, and monitoring).
	4.	Support API pagination (efficient retrieval of large datasets).
	5.	Integrate webhook event storage for auditing and debugging.
	6.	Dynamic API rate-limiting handling to avoid request failures.

📌 Final Guidelines

This system prompt defines all existing features, configurations, and future development goals for Upgatescz API. Before implementing any new changes, validate against this baseline to ensure consistency.

⚠️ Never remove essential features like:
	•	DuckDB caching
	•	AI translations
	•	Webhook processing
	•	Configurable batch syncs
	•	API logging & retry mechanisms
	•	Existing CLI commands

References:
	•	Pydantic AI (latest v: 0.0.21+) : 
         https://ai.pydantic.dev/
         https://github.com/pydantic/pydantic-ai/tree/main/docs
	•	Pydantic Firelog (latest v3.4+ ) : https://logfire.pydantic.dev/docs/
	•	Upgates.cz API Apiary Documentation : https://upgatesapiv2.docs.apiary.io/
	•	Upgates.cz CSV Documentation : https://www.upgates.cz/a/dokumentace-csv-produktu
	•	Upgates.cz XML Documentation : https://www.upgates.cz/dokumentace-xml

Other Preferences: 
	•	Requires all file versions to be incremented in # path/filename v0.0.0 footer comments.
	•	Prefers modular programming with replaceable functions and objects.
	•	Requires tight formatting with minimal extra lines unless necessary.
	•	Prefers emojis in responses.
	•	Prefers using up-to-date package versions and refactoring to use optimizations added in Python 3.10-3.12.
	•	Prefer sharing a full updated copy of the latest version of the project as a .zip file and explain the updates and any additional instructions required to complete the migration to the latest version.

📌 Use this as the foundation for future improvements and optimizations. 🚀