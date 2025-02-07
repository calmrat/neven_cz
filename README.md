# Neven 7 s.r.o Project

This repository contains the codebase for the Neven 7 s.r.o project. The project integrates with the Upgates.cz API to synchronize product, customer, and order data while leveraging robust logging and configuration management.

## Project Overview

- **API Integration**: Synchronization of data from Upgates.cz.
- **Logging**: Structured logging using Logfire.
- **Configuration**: Flexible and modular configuration with sample files in `.config/`.
- **Caching**: Caching support using DuckDB for efficient queries.

## Modules

- **abra**:  
  - Contains core API logic, webhook processing, and configuration examples.  

- **upgates**:  
  - Provides deployment support (Docker, CLI commands) and additional configuration management.  

## Getting Started

1. **Clone the repository**.
2. **Setup Environment**:  
   - Install dependencies using `pip install -r requirements.txt`.  
   - Configure your environment using the sample configuration located at `.config/upgates/config.toml.sample`.
3. **Run the Application**:  
   - Depending on which task you are working on, run either `bin/abra` or `bin/upgates` CLI applications.
4. **Testing**:  
   - Run tests with `pytest` to ensure that all functionalities work as expected.

## License

Copyright - Chris Ward <chris@calmrat.com>