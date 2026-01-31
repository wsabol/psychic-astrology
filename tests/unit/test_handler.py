import json
import pytest
from src import handler

def test_lambda_handler_basic():
    # Test a simple request that doesn't require heavy calculations if possible
    # or mock the calculations.
    event = {
        "request_type": "moon_phase"
    }
    
    # We might need to mock swisseph as it requires C extensions
    # but let's see if we can at least test the structure
    context = {}
    response = handler.lambda_handler(event, context)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "success" in body

def test_calculate_birth_chart_missing_data():
    event = {
        "request_type": "birth_chart"
        # missing birth_date, birth_time
    }
    response = handler.lambda_handler(event, context={})
    assert response["statusCode"] == 200 # The handler returns 200 even with logic errors in body
    body = json.loads(response["body"])
    assert body["success"] is False
    assert "error" in body
