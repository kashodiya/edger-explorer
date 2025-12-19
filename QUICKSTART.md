# EDGAR Explorer - Quick Start Guide

## What is EDGAR Explorer?

EDGAR Explorer is a web application that makes it easy to explore SEC EDGAR filing data. It provides:

- 🔍 **Company Search**: Find companies by ticker or name
- 📊 **Financial Statements**: View balance sheets, income statements, and cash flows
- 📄 **Filing Browser**: Browse and filter SEC filings by form type and date
- ⚡ **Fast Performance**: SQLite caching for improved speed
- 🎨 **Modern UI**: Clean, responsive interface built with Vue.js and Vuetify

## Quick Setup (3 steps)

### 1. Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Setup the project

```bash
# Clone and setup
git clone <repository-url>
cd edgar-explorer
uv sync

# Or run the setup script
uv run python setup.py
```

### 3. Set your EDGAR identity and run

```bash
# Set identity (required by SEC)
export EDGAR_IDENTITY="Your Name your.email@example.com"

# Start the application
uv run python run.py
```

Open http://localhost:8000 in your browser!

## Features Overview

### 🏠 Home Page
- Search for companies by ticker (AAPL) or name (Apple Inc)
- Quick access to popular companies
- Browse recent filings across all companies

### 🏢 Company View
- **Filings Tab**: Browse all filings for a company, filter by form type
- **Financials Tab**: View financial statements (balance sheet, income statement, cash flow)
- Click on any filing to see detailed information

### 📄 Filing Details
- View filing metadata (form type, date, size, etc.)
- See all attachments and documents
- XBRL availability indicator

### ⏰ Recent Filings
- Browse the latest filings across all companies
- Filter by form type (10-K, 10-Q, 8-K, etc.)
- Click to view detailed filing information

## Common Use Cases

### 1. Analyze a Company's Financials
1. Search for company (e.g., "AAPL")
2. Click on the company card
3. Go to "Financials" tab
4. Explore balance sheet, income statement, cash flow

### 2. Track Recent 10-K Filings
1. Go to "Recent Filings"
2. Filter by "10-K - Annual Report"
3. Browse the latest annual reports

### 3. Monitor Insider Transactions
1. Search for a company
2. Filter filings by "Form 4 - Insider Transactions"
3. Click on filings to see transaction details

### 4. Research IPO Activity
1. Go to "Recent Filings"
2. Filter by "S-1 - Registration Statement"
3. See companies preparing to go public

## Technical Details

### Architecture
- **Backend**: FastAPI with Python
- **Frontend**: Vue.js 3 with Vuetify 3 and Vue Router
- **Data Source**: SEC EDGAR via edgartools library
- **Caching**: SQLite database for improved performance
- **Package Management**: UV for fast, reliable dependency management

### API Endpoints
- `GET /api/search/companies` - Search companies
- `GET /api/company/{ticker}` - Get company info
- `GET /api/company/{ticker}/filings` - Get company filings
- `GET /api/company/{ticker}/financials` - Get financial statements
- `GET /api/filing/{accession_no}` - Get filing details
- `GET /api/recent-filings` - Get recent filings
- `GET /api/form-types` - Get available form types

### Data Caching
The app automatically caches:
- Company information
- Filing metadata
- Financial statements

Cache is stored in `edgar_cache.db` (SQLite) for fast subsequent access.

## Troubleshooting

### "EDGAR identity not set" error
Set the environment variable:
```bash
export EDGAR_IDENTITY="Your Name your.email@example.com"
```

### "edgartools not found" error
Install dependencies:
```bash
uv sync
```

### Slow initial loading
First-time data fetching from SEC EDGAR can be slow. Subsequent requests use cached data.

### SSL certificate errors
If you encounter SSL issues, check the edgartools documentation for SSL troubleshooting.

## Development

### Run tests
```bash
uv run pytest
```

### Add new dependencies
```bash
uv add <package-name>
```

### Development mode (auto-reload)
```bash
uv run uvicorn main:app --reload
```

## Next Steps

- Explore different form types (10-K, 10-Q, 8-K, DEF 14A, etc.)
- Try searching for companies in different industries
- Use the financial statements for comparative analysis
- Monitor insider transactions and institutional holdings

## Support

- Check the main README.md for detailed documentation
- Review the edgartools documentation for data source details
- Open issues for bugs or feature requests

Happy exploring! 🚀