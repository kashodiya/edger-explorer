# EdgarTools - Comprehensive Usage Guide

## Overview

**EdgarTools** is an AI-native Python library for accessing and analyzing SEC EDGAR filing data. It's designed to be the fastest, most powerful open-source library for SEC data extraction, built specifically for financial analysts, data scientists, and AI developers.

### Key Features

- **Lightning Fast**: 10-30x faster than alternatives, optimized with lxml & PyArrow
- **AI Native**: Built-in MCP server for Claude, LLM-optimized text extraction
- **Production Quality**: 1000+ tests, comprehensive type hints
- **XBRL Native**: Full XBRL standardization for cross-company comparisons
- **Rich Data Objects**: Smart parsing for every form type, Pandas-ready DataFrames
- **Open Source**: MIT license, free forever, no API keys required

## Installation

```bash
# Basic installation
pip install edgartools

# With AI capabilities (MCP server, skills)
pip install "edgartools[ai]"

# With cloud storage support
pip install "edgartools[s3]"      # AWS S3, Cloudflare R2, MinIO
pip install "edgartools[gcs]"     # Google Cloud Storage
pip install "edgartools[azure]"   # Azure Blob Storage
```

## Quick Start

### 1. Set Your Identity (Required by SEC)

The SEC requires you to identify yourself when accessing their data.

```python
from edgar import *

# Method 1: In Python
set_identity("your.name@example.com")

# Method 2: Environment variable (Linux/Mac)
# export EDGAR_IDENTITY="your.name@example.com"

# Method 3: Environment variable (Windows)
# set EDGAR_IDENTITY="your.name@example.com"

# Method 4: Environment variable (PowerShell)
# $env:EDGAR_IDENTITY="your.name@example.com"
```

### 2. Get Company Financials in 1 Line

```python
# Get Apple's balance sheet
balance_sheet = Company("AAPL").get_financials().balance_sheet()

# Get Microsoft's income statement
income_statement = Company("MSFT").get_financials().income_statement()
```

### 3. Explore Insider Transactions

```python
company = Company("AAPL")
filings = company.get_filings(form="4")
form4_filing = filings[0]
form4 = form4_filing.obj()
```

## Core Concepts

### 1. Working with Filings

#### Getting Filings

```python
# Get filings for the year to date
filings = get_filings()

# Get filings for a specific year
filings = get_filings(2020)

# Get filings for a specific quarter
filings = get_filings(2020, 1)

# Get filings for multiple years
filings = get_filings([2020, 2021])

# Get filings for a range of years
filings = get_filings(year=range(2010, 2020))

# Get only XBRL filings
filings = get_filings(index="xbrl")

# Get the latest filings (just released)
filings = get_latest_filings()
```

#### Filtering Filings

```python
# Filter by form type
filings.filter(form="10-K")

# Filter by multiple forms
filings.filter(form=["10-K", "10-Q"])

# Include amendments
filings.filter(form="10-K", amendments=True)

# Filter by ticker
filings.filter(ticker="AAPL")

# Filter by multiple tickers
filings.filter(ticker=["AAPL", "MSFT"])

# Filter by CIK
filings.filter(cik="0000320193")

# Filter by date
filings.filter(date="2020-01-01")

# Filter between dates
filings.filter(date="2020-01-01:2020-03-01")

# Filter before a date
filings.filter(date=":2020-03-01")

# Filter after a date
filings.filter(date="2020-03-01:")

# Combine multiple filters
filings.filter(form="10-K", date="2020-01-01:", ticker="AAPL")
```

#### Viewing and Manipulating Filings

```python
# Show the next page of filings
filings.next()

# Show the previous page of filings
filings.previous()

# Get the first n filings
filings.head(20)

# Get the last n filings
filings.tail(20)

# Get the latest n filings by date
filings.latest(20)

# Get a random sample of filings
filings.sample(20)

# Convert to pandas DataFrame
df = filings.to_pandas()
```

### 2. Working with a Single Filing

#### Accessing a Filing

```python
# Get a single filing from a collection
filing = filings[3]

# Get a filing by accession number
filing = get_by_accession_number("0000320193-20-34576")

# Get the filing homepage
filing.homepage

# Open a filing in the browser
filing.open()

# Open homepage in the browser
filing.homepage.open()

# View the filing in the terminal
filing.view()
```

#### Extracting Filing Content

```python
# Get the HTML of the filing
html = filing.html()

# Get the XBRL of the filing
xbrl = filing.xbrl()

# Get the filing as markdown
markdown = filing.markdown()

# Get the full submission text
text = filing.full_text_submission()

# Get and parse filing data object
obj = filing.obj()

# Get filing header
header = filing.header
```

#### Searching Inside a Filing

```python
# Search within the filing
results = filing.search("revenue growth")

# Search with regex
results = filing.search(r"\d+\.\d+%", regex=True)

# Get filing sections
sections = filing.sections()
```

#### Working with Attachments

```python
# Get all filing attachments
attachments = filing.attachments

# Get a single attachment
attachment = filing.attachments[0]

# Open attachment in browser
attachment.open()

# Download an attachment
content = attachment.download()
```

### 3. Working with Companies

```python
# Get a company by ticker
company = Company("AAPL")

# Get a company by CIK
company = Company("0000320193")

# Get company facts
facts = company.get_facts()

# Get company facts as a pandas DataFrame
df = company.get_facts().to_pandas()

# Get company filings
filings = company.get_filings()

# Get company filings by form
filings = company.get_filings(form="10-K")

# Get the latest 10-Q
filing = company.latest("10-Q")

# Get the last 5 10-Q's
filings = company.get_filings(form="10-Q").head(5)

# Get a company filing by accession number
filing = company.get_filing(accession_number="0000320193-21-000139")
```

### 4. Working with Financials

```python
# Get the company's financials
financials = company.get_financials()

# Get the balance sheet
balance_sheet = financials.balance_sheet()

# Get the income statement
income_statement = financials.income_statement()

# Get the cash flow statement
cashflow = financials.cashflow_statement()

# All statements are returned as pandas DataFrames
print(balance_sheet.head())
```

### 5. Working with XBRL Data

EdgarTools provides comprehensive XBRL support for extracting structured financial data:

```python
# Get XBRL from a filing
filing = Company("AAPL").latest("10-K")
xbrl = filing.xbrl()

# Access financial statements
balance_sheet = xbrl.balance_sheet
income_statement = xbrl.income_statement
cash_flow = xbrl.cash_flow_statement

# Get specific facts
revenue = xbrl.get_fact("Revenues")

# Get facts by concept
assets = xbrl.get_facts_by_concept("Assets")

# Convert to DataFrame
df = xbrl.to_dataframe()
```

### 6. Working with Insider Transactions (Forms 3, 4, 5)

```python
# Get Form 4 filings (insider transactions)
company = Company("AAPL")
form4_filings = company.get_filings(form="4")

# Get the data object from a Form 4
filing = form4_filings[0]
form4 = filing.obj()

# Access transaction details
print(form4.issuer)
print(form4.reporting_owner)
print(form4.non_derivative_transactions)
print(form4.derivative_transactions)
```

### 7. Working with 13F Filings (Institutional Holdings)

```python
# Get 13F filings
filings = get_filings(form="13F-HR")

# Get a specific 13F filing
filing = filings[0]
thirteenf = filing.obj()

# Access holdings
holdings = thirteenf.holdings
print(holdings.head())

# Convert to DataFrame
df = thirteenf.to_dataframe()
```

### 8. Working with Funds

```python
# Find a fund by ticker
fund = find_fund("VFIAX")

# Get fund filings
filings = fund.get_filings()

# Get fund portfolio holdings (NPORT-P)
nport_filings = get_filings(form="NPORT-P")
filing = nport_filings[0]
fund_report = filing.obj()

# Access portfolio holdings
holdings = fund_report.holdings
```

### 9. Working with Proxy Statements

```python
# Get proxy statements (DEF 14A)
company = Company("AAPL")
proxy_filings = company.get_filings(form="DEF 14A")

# Get the data object
filing = proxy_filings[0]
proxy = filing.obj()

# Access executive compensation data
compensation = proxy.executive_compensation
```

## Advanced Features

### 1. Universal Search Function

The `find()` function is a universal search that can handle various input types:

```python
# Find by accession number -> returns Filing
filing = find("0000320193-20-000096")

# Find by CIK -> returns Entity
entity = find("0000320193")

# Find by ticker -> returns Company
company = find("AAPL")

# Find by company name -> returns CompanySearchResults
results = find("Apple Inc")

# Find fund by ticker
fund = find("VFIAX")
```

### 2. Entity Facts

Get comprehensive financial facts for a company:

```python
from edgar.enums import PeriodType

company = Company("AAPL")

# Get annual facts
annual_facts = company.get_facts(period_type=PeriodType.ANNUAL)

# Convert to DataFrame
df = annual_facts.to_dataframe()

# Filter for specific concepts
revenue_df = df[df['concept'].str.contains('Revenue', case=False, na=False)]

# Export with metadata
df_full = annual_facts.to_dataframe(include_metadata=True)

# Custom column selection
df_slim = annual_facts.to_dataframe(
    columns=['concept', 'fiscal_year', 'numeric_value', 'unit']
)
```

### 3. Text Extraction

```python
# Get clean text from a 10-K filing
company = Company("ORCL")
filing = company.latest("10-K")
text = filing.text()

# Get specific sections
sections = filing.sections()
risk_factors = sections.get("Risk Factors")
mda = sections.get("Management's Discussion and Analysis")
```

### 4. Batch Processing

```python
# Process multiple companies
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
for ticker in tickers:
    company = Company(ticker)
    financials = company.get_financials()
    balance_sheet = financials.balance_sheet()
    print(f"{ticker}: {balance_sheet.head()}")
```

### 5. Data Export

```python
# Export filings to pandas
filings = get_filings(2023, form="10-K")
df = filings.to_pandas()
df.to_csv("filings_2023.csv")

# Export financials
company = Company("AAPL")
balance_sheet = company.get_financials().balance_sheet()
balance_sheet.to_excel("aapl_balance_sheet.xlsx")
```

## Form Types and Data Objects

EdgarTools provides structured data objects for many form types:

| Form Type | Data Object | Description |
|-----------|-------------|-------------|
| 10-K | TenK | Annual report with financials |
| 10-Q | TenQ | Quarterly report with financials |
| 8-K | EightK | Current report with event details |
| 6-K | CurrentReport | Foreign issuer current report |
| 20-F | TwentyF | Foreign issuer annual report |
| 13F-HR | ThirteenF | Institutional holdings |
| SCHEDULE 13D | Schedule13D | Beneficial ownership (5%+ stake, active) |
| SCHEDULE 13G | Schedule13G | Beneficial ownership (5%+ stake, passive) |
| 3 | Form3 | Initial insider ownership |
| 4 | Form4 | Insider transaction |
| 5 | Form5 | Annual insider transaction summary |
| 144 | Form144 | Restricted stock sale notice |
| D | FormD | Private placement offering |
| C | FormC | Crowdfunding offering details |
| NPORT-P | FundReport | Fund portfolio holdings |
| N-PX | NPX | Annual proxy voting record |
| DEF 14A | ProxyStatement | Proxy statement with executive compensation |

## AI Integration

### Option 1: AI Skills (Recommended)

Install EdgarTools skills for Claude Code or Claude Desktop:

```bash
pip install "edgartools[ai]"
python -c "from edgar.ai import install_skill; install_skill()"
```

This adds SEC analysis capabilities to Claude with 3,450+ lines of API documentation and examples.

### Option 2: MCP Server

Run EdgarTools as an MCP server:

```bash
pip install "edgartools[ai]"
python -m edgar.ai
```

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "edgartools": {
      "command": "python",
      "args": ["-m", "edgar.ai"],
      "env": {
        "EDGAR_IDENTITY": "Your Name your.email@example.com"
      }
    }
  }
}
```

## Configuration

### HTTP Configuration

```python
from edgar import configure_http

# Configure SSL verification
configure_http(verify_ssl=True)

# Configure proxy
configure_http(proxy="http://proxy.example.com:8080")

# Configure timeout
configure_http(timeout=30)
```

### Cache Configuration

```python
from edgar import set_cache_directory

# Set custom cache directory
set_cache_directory("/path/to/cache")

# Clear cache
from edgar import clear_cache
clear_cache()
```

### Enterprise Configuration

For corporate environments with SEC mirrors or custom rate limiting:

```python
from edgar import edgar_mode, NORMAL, CAUTION, CRAWL

# Set rate limiting mode
edgar_mode(NORMAL)   # Default: 10 requests/second
edgar_mode(CAUTION)  # Conservative: 5 requests/second
edgar_mode(CRAWL)    # Aggressive: 20 requests/second
```

## Best Practices

1. **Always set your identity**: The SEC requires it and may block requests without proper identification
2. **Use filtering**: Filter filings early to reduce data transfer and processing time
3. **Cache results**: EdgarTools caches data automatically, but you can also cache your own processed results
4. **Batch operations**: When processing multiple companies, use batch operations to improve efficiency
5. **Handle errors**: Always wrap API calls in try-except blocks for production code
6. **Respect rate limits**: The SEC has rate limits; EdgarTools handles this automatically but be mindful in loops

## Common Use Cases

### 1. Financial Analysis

```python
# Compare revenue growth across companies
companies = ["AAPL", "MSFT", "GOOGL"]
for ticker in companies:
    company = Company(ticker)
    facts = company.get_facts()
    df = facts.to_dataframe()
    revenue = df[df['concept'].str.contains('Revenue', case=False)]
    print(f"{ticker} Revenue: {revenue}")
```

### 2. Insider Trading Analysis

```python
# Find insider transactions above $1M
company = Company("TSLA")
form4_filings = company.get_filings(form="4")
for filing in form4_filings:
    form4 = filing.obj()
    for transaction in form4.non_derivative_transactions:
        if transaction.transaction_amount > 1000000:
            print(f"Large transaction: {transaction}")
```

### 3. Portfolio Holdings Analysis

```python
# Analyze 13F holdings
filings = get_filings(form="13F-HR", date="2023-01-01:")
for filing in filings:
    thirteenf = filing.obj()
    holdings = thirteenf.holdings
    # Analyze holdings
    print(f"Total holdings: {len(holdings)}")
```

### 4. Risk Factor Analysis

```python
# Extract risk factors from 10-K
company = Company("AAPL")
filing = company.latest("10-K")
sections = filing.sections()
risk_factors = sections.get("Risk Factors")
print(risk_factors)
```

## Resources

- **Documentation**: https://edgartools.readthedocs.io/
- **GitHub**: https://github.com/dgunning/edgartools
- **Blog**: https://www.edgartools.io
- **Examples**: 62 examples (28 notebooks + 9 scripts) in the repository
- **Issues**: https://github.com/dgunning/edgartools/issues
- **Discussions**: https://github.com/dgunning/edgartools/discussions

## Performance Tips

1. **Use XBRL index**: When working with financial statements, use `index="xbrl"` to get only XBRL filings
2. **Filter early**: Apply filters before iterating through filings
3. **Batch requests**: Process multiple items in batches rather than one at a time
4. **Use DataFrames**: Convert to pandas DataFrames for efficient data manipulation
5. **Cache strategically**: EdgarTools caches automatically, but consider caching your processed results

## Troubleshooting

### SSL Issues

If you encounter SSL certificate errors:

```python
from edgar import diagnose_ssl

# Run SSL diagnostics
diagnose_ssl()

# Disable SSL verification (not recommended for production)
from edgar import configure_http
configure_http(verify_ssl=False)
```

### Rate Limiting

If you're hitting rate limits:

```python
from edgar import edgar_mode, CAUTION

# Use more conservative rate limiting
edgar_mode(CAUTION)
```

### Cache Issues

If you're experiencing cache-related problems:

```python
from edgar import clear_cache

# Clear the cache
clear_cache()
```

## License

EdgarTools is distributed under the MIT License - free forever, no API keys, no rate limits beyond SEC requirements.
