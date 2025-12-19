from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sqlite3
import json
import os
from datetime import datetime, date
import logging

# Edgar imports
try:
    from edgar import *
except ImportError:
    print("EdgarTools not installed. Run: uv add edgartools")
    raise

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EDGAR Explorer", description="Explore SEC EDGAR filings data")

# Database setup
DB_PATH = "edgar_cache.db"

def init_db():
    """Initialize SQLite database for caching"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Companies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            ticker TEXT PRIMARY KEY,
            cik TEXT,
            name TEXT,
            data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Filings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filings (
            accession_no TEXT PRIMARY KEY,
            ticker TEXT,
            form TEXT,
            filing_date TEXT,
            data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Financial data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            statement_type TEXT,
            data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Set EDGAR identity
edgar_identity = os.getenv("EDGAR_IDENTITY", "edgar-explorer@example.com")
try:
    set_identity(edgar_identity)
    logger.info(f"EDGAR identity set to: {edgar_identity}")
except Exception as e:
    logger.warning(f"Could not set EDGAR identity: {e}")
    logger.warning("Please set EDGAR_IDENTITY environment variable or update main.py")

# Pydantic models
class CompanyInfo(BaseModel):
    ticker: str
    cik: Optional[str] = None
    name: Optional[str] = None

class FilingInfo(BaseModel):
    accession_no: str
    form: str
    filing_date: str
    company_name: str
    ticker: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    form_types: Optional[List[str]] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None

# Database helper functions
def get_cached_company(ticker: str) -> Optional[Dict]:
    """Get cached company data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM companies WHERE ticker = ?", (ticker,))
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None

def cache_company(ticker: str, data: Dict):
    """Cache company data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO companies (ticker, cik, name, data)
        VALUES (?, ?, ?, ?)
    """, (ticker, data.get('cik'), data.get('name'), json.dumps(data)))
    conn.commit()
    conn.close()

def get_cached_filings(ticker: str, form: Optional[str] = None) -> List[Dict]:
    """Get cached filings for a company"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if form:
        cursor.execute("""
            SELECT data FROM filings 
            WHERE ticker = ? AND form = ?
            ORDER BY filing_date DESC
        """, (ticker, form))
    else:
        cursor.execute("""
            SELECT data FROM filings 
            WHERE ticker = ?
            ORDER BY filing_date DESC
        """, (ticker,))
    
    results = cursor.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in results]

def cache_filing(filing_data: Dict):
    """Cache filing data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO filings (accession_no, ticker, form, filing_date, data)
        VALUES (?, ?, ?, ?, ?)
    """, (
        filing_data['accession_no'],
        filing_data.get('ticker'),
        filing_data['form'],
        filing_data['filing_date'],
        json.dumps(filing_data)
    ))
    conn.commit()
    conn.close()

# API Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/search/companies")
async def search_companies(q: str = Query(..., description="Company name or ticker to search")):
    """Search for companies by name or ticker"""
    try:
        # Try to find company directly first
        try:
            company = Company(q.upper())
            company_data = {
                "ticker": q.upper(),
                "cik": company.cik,
                "name": company.name,
                "sic": getattr(company, 'sic', None),
                "industry": getattr(company, 'industry', None)
            }
            cache_company(q.upper(), company_data)
            return [company_data]
        except:
            # If direct lookup fails, try search
            results = find_company(q)
            if hasattr(results, 'companies'):
                companies = []
                for comp in results.companies[:10]:  # Limit to 10 results
                    company_data = {
                        "ticker": comp.ticker,
                        "cik": comp.cik,
                        "name": comp.name,
                        "sic": getattr(comp, 'sic', None),
                        "industry": getattr(comp, 'industry', None)
                    }
                    companies.append(company_data)
                    cache_company(comp.ticker, company_data)
                return companies
            else:
                return []
    except Exception as e:
        logger.error(f"Error searching companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/company/{ticker}")
async def get_company_info(ticker: str):
    """Get detailed company information"""
    try:
        # Check cache first
        cached = get_cached_company(ticker.upper())
        if cached:
            return cached
        
        # Fetch from EDGAR
        company = Company(ticker.upper())
        company_data = {
            "ticker": ticker.upper(),
            "cik": company.cik,
            "name": company.name,
            "sic": getattr(company, 'sic', None),
            "industry": getattr(company, 'industry', None),
            "description": getattr(company, 'description', None)
        }
        
        cache_company(ticker.upper(), company_data)
        return company_data
        
    except Exception as e:
        logger.error(f"Error getting company info: {e}")
        raise HTTPException(status_code=404, detail=f"Company {ticker} not found")

@app.get("/api/company/{ticker}/filings")
async def get_company_filings(
    ticker: str,
    form: Optional[str] = None,
    limit: int = Query(20, description="Number of filings to return")
):
    """Get filings for a company"""
    try:
        # Check cache first
        cached_filings = get_cached_filings(ticker.upper(), form)
        if cached_filings and len(cached_filings) >= limit:
            return cached_filings[:limit]
        
        # Fetch from EDGAR
        company = Company(ticker.upper())
        if form:
            filings = company.get_filings(form=form)
        else:
            filings = company.get_filings()
        
        filings_data = []
        for filing in filings.head(limit):
            filing_data = {
                "accession_no": filing.accession_no,
                "form": filing.form,
                "filing_date": str(filing.filing_date),
                "company_name": filing.company,
                "ticker": ticker.upper(),
                "description": getattr(filing, 'description', ''),
                "size": getattr(filing, 'size', 0)
            }
            filings_data.append(filing_data)
            cache_filing(filing_data)
        
        return filings_data
        
    except Exception as e:
        logger.error(f"Error getting filings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/company/{ticker}/financials")
async def get_company_financials(ticker: str):
    """Get financial statements for a company"""
    try:
        company = Company(ticker.upper())
        financials = company.get_financials()
        
        result = {}
        
        # Get balance sheet
        try:
            balance_sheet = financials.balance_sheet()
            if balance_sheet is not None and not balance_sheet.empty:
                result["balance_sheet"] = balance_sheet.to_dict('records')
        except Exception as e:
            logger.warning(f"Could not get balance sheet: {e}")
            result["balance_sheet"] = []
        
        # Get income statement
        try:
            income_statement = financials.income_statement()
            if income_statement is not None and not income_statement.empty:
                result["income_statement"] = income_statement.to_dict('records')
        except Exception as e:
            logger.warning(f"Could not get income statement: {e}")
            result["income_statement"] = []
        
        # Get cash flow statement
        try:
            cash_flow = financials.cashflow_statement()
            if cash_flow is not None and not cash_flow.empty:
                result["cash_flow"] = cash_flow.to_dict('records')
        except Exception as e:
            logger.warning(f"Could not get cash flow: {e}")
            result["cash_flow"] = []
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting financials: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filing/{accession_no}")
async def get_filing_details(accession_no: str):
    """Get detailed information about a specific filing"""
    try:
        filing = get_by_accession_number(accession_no)
        
        filing_data = {
            "accession_no": filing.accession_no,
            "form": filing.form,
            "filing_date": str(filing.filing_date),
            "company_name": filing.company,
            "cik": filing.cik,
            "description": getattr(filing, 'description', ''),
            "size": getattr(filing, 'size', 0),
            "has_xbrl": filing.xbrl() is not None,
            "attachments": []
        }
        
        # Get attachments info
        try:
            for attachment in filing.attachments:
                att_data = {
                    "filename": attachment.document,
                    "description": getattr(attachment, 'description', ''),
                    "type": getattr(attachment, 'type', ''),
                    "size": getattr(attachment, 'size', 0)
                }
                filing_data["attachments"].append(att_data)
        except Exception as e:
            logger.warning(f"Could not get attachments: {e}")
        
        return filing_data
        
    except Exception as e:
        logger.error(f"Error getting filing details: {e}")
        raise HTTPException(status_code=404, detail=f"Filing {accession_no} not found")

@app.get("/api/recent-filings")
async def get_recent_filings(
    form: Optional[str] = None,
    limit: int = Query(50, description="Number of recent filings to return")
):
    """Get recent filings across all companies"""
    try:
        if form:
            filings = get_filings(form=form)
        else:
            filings = get_filings()
        
        filings_data = []
        for filing in filings.head(limit):
            filing_data = {
                "accession_no": filing.accession_no,
                "form": filing.form,
                "filing_date": str(filing.filing_date),
                "company_name": filing.company,
                "cik": filing.cik,
                "description": getattr(filing, 'description', ''),
                "size": getattr(filing, 'size', 0)
            }
            filings_data.append(filing_data)
        
        return filings_data
        
    except Exception as e:
        logger.error(f"Error getting recent filings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/form-types")
async def get_form_types():
    """Get list of common SEC form types"""
    return [
        {"value": "10-K", "text": "10-K - Annual Report"},
        {"value": "10-Q", "text": "10-Q - Quarterly Report"},
        {"value": "8-K", "text": "8-K - Current Report"},
        {"value": "DEF 14A", "text": "DEF 14A - Proxy Statement"},
        {"value": "13F-HR", "text": "13F-HR - Institutional Holdings"},
        {"value": "4", "text": "Form 4 - Insider Transactions"},
        {"value": "3", "text": "Form 3 - Initial Insider Ownership"},
        {"value": "5", "text": "Form 5 - Annual Insider Summary"},
        {"value": "S-1", "text": "S-1 - Registration Statement"},
        {"value": "424B4", "text": "424B4 - Prospectus"},
        {"value": "NPORT-P", "text": "NPORT-P - Fund Portfolio Holdings"}
    ]

@app.get("/api/filing/{accession_no}/attachment/{filename}")
async def download_attachment(accession_no: str, filename: str):
    """Download a specific attachment from a filing"""
    try:
        filing = get_by_accession_number(accession_no)
        
        # Find the attachment
        attachment = None
        for att in filing.attachments:
            if att.document == filename:
                attachment = att
                break
        
        if not attachment:
            raise HTTPException(status_code=404, detail=f"Attachment {filename} not found")
        
        # Get the content
        content = attachment.download()
        
        # Determine content type based on file extension
        content_type = "application/octet-stream"
        filename_lower = filename.lower()
        if filename_lower.endswith(('.html', '.htm')):
            content_type = "text/html"
        elif filename_lower.endswith('.xml'):
            content_type = "application/xml"
        elif filename_lower.endswith('.txt'):
            content_type = "text/plain"
        elif filename_lower.endswith('.pdf'):
            content_type = "application/pdf"
        elif filename_lower.endswith(('.xls', '.xlsx')):
            content_type = "application/vnd.ms-excel"
        elif filename_lower.endswith(('.doc', '.docx')):
            content_type = "application/msword"
        elif filename_lower.endswith('.csv'):
            content_type = "text/csv"
        elif filename_lower.endswith('.json'):
            content_type = "application/json"
        
        from fastapi.responses import Response
        return Response(
            content=content,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(content))
            }
        )
        
    except Exception as e:
        logger.error(f"Error downloading attachment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filing/{accession_no}/attachment/{filename}/view")
async def view_attachment(accession_no: str, filename: str):
    """View a specific attachment from a filing (inline display)"""
    try:
        filing = get_by_accession_number(accession_no)
        
        # Find the attachment
        attachment = None
        for att in filing.attachments:
            if att.document == filename:
                attachment = att
                break
        
        if not attachment:
            raise HTTPException(status_code=404, detail=f"Attachment {filename} not found")
        
        # Get the content
        content = attachment.download()
        
        # For text-based files, return as text for inline viewing
        filename_lower = filename.lower()
        if filename_lower.endswith(('.html', '.htm', '.xml', '.txt', '.csv', '.json')):
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            
            # Determine content type
            if filename_lower.endswith(('.html', '.htm')):
                content_type = "text/html"
            elif filename_lower.endswith('.xml'):
                content_type = "application/xml"
            elif filename_lower.endswith('.csv'):
                content_type = "text/csv"
            elif filename_lower.endswith('.json'):
                content_type = "application/json"
            else:
                content_type = "text/plain"
            
            from fastapi.responses import Response
            return Response(
                content=content,
                media_type=content_type,
                headers={"Content-Disposition": "inline"}
            )
        else:
            # For binary files, still allow download
            content_type = "application/octet-stream"
            if filename.lower().endswith('.pdf'):
                content_type = "application/pdf"
            elif filename.lower().endswith('.xls') or filename.lower().endswith('.xlsx'):
                content_type = "application/vnd.ms-excel"
            
            from fastapi.responses import Response
            return Response(
                content=content,
                media_type=content_type,
                headers={"Content-Disposition": "inline"}
            )
        
    except Exception as e:
        logger.error(f"Error viewing attachment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filing/{accession_no}/attachments")
async def get_filing_attachments(accession_no: str):
    """Get list of attachments for a filing with metadata"""
    try:
        filing = get_by_accession_number(accession_no)
        
        attachments = []
        for attachment in filing.attachments:
            att_data = {
                "filename": attachment.document,
                "description": getattr(attachment, 'description', ''),
                "type": getattr(attachment, 'type', ''),
                "size": getattr(attachment, 'size', 0),
                "is_viewable": attachment.document.lower().endswith(('.html', '.htm', '.xml', '.txt', '.pdf', '.csv', '.json')),
                "download_url": f"/api/filing/{accession_no}/attachment/{attachment.document}",
                "view_url": f"/api/filing/{accession_no}/attachment/{attachment.document}/view"
            }
            attachments.append(att_data)
        
        return attachments
        
    except Exception as e:
        logger.error(f"Error getting attachments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)