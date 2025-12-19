# EDGAR Explorer

A web application to explore SEC EDGAR filing data using FastAPI backend and Vue.js frontend.

## Features

- Search companies by ticker or name
- View company filings and financial statements
- Browse recent filings across all companies
- Interactive Vue.js frontend with Vuetify UI components
- SQLite caching for improved performance
- Built with FastAPI and edgartools

## Prerequisites

- Python 3.10+
- UV package manager

## Installation

1. Install UV if you haven't already:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Clone and setup the project:
```bash
git clone <repository-url>
cd edgar-explorer
uv sync
```

3. Set your EDGAR identity (required by SEC):
```bash
# Linux/Mac
export EDGAR_IDENTITY="Your Name your.email@example.com"

# Windows Command Prompt
set EDGAR_IDENTITY=Your Name your.email@example.com

# Windows PowerShell
$env:EDGAR_IDENTITY="Your Name your.email@example.com"
```

## Running the Application

1. Start the application:
```bash
uv run python run.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

The application will automatically create a SQLite database (`edgar_cache.db`) for caching data.

## Development

Run tests:
```bash
uv run pytest
```

Add new dependencies:
```bash
uv add <package-name>
```

Add development dependencies:
```bash
uv add --dev <package-name>
```

## API Endpoints

- `GET /` - Serve the main HTML page
- `GET /api/search/companies?q={query}` - Search companies
- `GET /api/company/{ticker}` - Get company information
- `GET /api/company/{ticker}/filings` - Get company filings
- `GET /api/company/{ticker}/financials` - Get financial statements
- `GET /api/filing/{accession_no}` - Get filing details
- `GET /api/recent-filings` - Get recent filings
- `GET /api/form-types` - Get available form types

## Project Structure

```
edgar-explorer/
├── main.py              # FastAPI application
├── index.html           # Vue.js frontend
├── pyproject.toml       # UV project configuration
├── edgar_cache.db       # SQLite cache (created automatically)
└── README.md           # This file
```

## License

MIT License