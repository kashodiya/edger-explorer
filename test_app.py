"""
Simple test to verify the application setup
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    """Test that the main page loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert "EDGAR Explorer" in response.text

def test_form_types():
    """Test that form types endpoint works"""
    response = client.get("/api/form-types")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(form["value"] == "10-K" for form in data)

def test_search_companies():
    """Test company search endpoint"""
    response = client.get("/api/search/companies?q=AAPL")
    assert response.status_code == 200
    # Note: This might fail if EDGAR is not accessible or identity not set
    # In a real test environment, you'd mock the EDGAR API calls

if __name__ == "__main__":
    pytest.main([__file__])