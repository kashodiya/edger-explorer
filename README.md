# EDGAR Explorer

A web application to explore SEC EDGAR filing data using FastAPI backend and Vue.js frontend.

## Features

- Search companies by ticker or name
- View company filings and financial statements
- **Download and view filing attachments** (HTML, XML, PDF, TXT, CSV, JSON)
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
git clone https://github.com/kashodiya/edger-explorer.git
cd edger-explorer
uv sync
```

3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and set your EDGAR identity (required by SEC)
# EDGAR_IDENTITY=Your Name your.email@example.com
```

**Alternative**: Set environment variable directly:
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

### Core Endpoints
- `GET /` - Serve the main HTML page
- `GET /api/search/companies?q={query}` - Search companies
- `GET /api/company/{ticker}` - Get company information
- `GET /api/company/{ticker}/filings` - Get company filings
- `GET /api/company/{ticker}/financials` - Get financial statements
- `GET /api/filing/{accession_no}` - Get filing details
- `GET /api/recent-filings` - Get recent filings
- `GET /api/form-types` - Get available form types

### Attachment Endpoints
- `GET /api/filing/{accession_no}/attachments` - Get filing attachments list
- `GET /api/filing/{accession_no}/attachment/{filename}` - Download attachment
- `GET /api/filing/{accession_no}/attachment/{filename}/view` - View attachment inline

## Project Structure

```
edger-explorer/
├── main.py              # FastAPI application with attachment endpoints
├── run.py               # Application startup script
├── index.html           # Vue.js frontend with attachment viewer
├── pyproject.toml       # UV project configuration
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (create from .env.example)
├── edgar_cache.db       # SQLite cache (created automatically)
└── README.md           # This file
```

## Environment Variables

The application requires the following environment variables:

- `EDGAR_IDENTITY` - Your identity for SEC EDGAR API (required by SEC regulations)
  - Format: "Your Name your.email@example.com"
  - Example: "John Doe john.doe@company.com"

## Usage

### Viewing Attachments
1. Search for a company (e.g., "AAPL")
2. Click on the company to view details
3. Navigate to the "Filings" tab
4. Click on any filing to view details
5. Scroll down to see "Attachments" section
6. Use "View" button to open supported files inline
7. Use "Download" button to save files locally

### Supported File Types for Viewing
- HTML/HTM files
- XML files  
- TXT files
- PDF files
- CSV files
- JSON files

## License

MIT License