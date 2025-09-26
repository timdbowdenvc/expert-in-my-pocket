import pytest
import requests
from app.agent.seo_agent.tools.analyze_url import analyze_url_for_seo

def test_analyze_url_success(requests_mock):
    url = "https://www.example.com"
    requests_mock.get(url, text="<html><head><title>Test Page</title></head><body></body></html>")
    
    report = analyze_url_for_seo(url=url)
    
    assert "Placeholder suggestion 1: Improve title tag." in report
    assert "The title of the page is: Test Page" in report

def test_analyze_url_failure(requests_mock):
    url = "https://www.example.com"
    requests_mock.get(url, exc=requests.exceptions.RequestException("Test Error"))
    
    report = analyze_url_for_seo(url=url)
    
    assert "Error" in report
    assert "Failed to fetch URL: Test Error" in report