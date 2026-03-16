import pytest
from logic import mock_agent_extraction, SiteFailure

def test_price_extraction():
    """
    Validate that the agent can still extract prices accurately.
    """
    url = "https://fragile-site.com/products/test-item"
    try:
        data = mock_agent_extraction(url)
    except SiteFailure as e:
        pytest.skip(f"Skipping extraction test: {e}")
    
    assert data is not None
    assert "price" in data
    assert data["price"] == "$49.99"
    print(f"Price extraction test passed: {data['price']}")

def test_availability_extraction():
    """
    Validate that the agent can still extract availability status.
    """
    url = "https://fragile-site.com/products/test-item"
    try:
        data = mock_agent_extraction(url)
    except SiteFailure as e:
        pytest.skip(f"Skipping availability test: {e}")
    
    assert data is not None
    assert "availability" in data
    assert data["availability"] == "In Stock"
    print(f"Availability extraction test passed: {data['availability']}")

def test_site_health_failure():
    """
    Validate that the agent correctly identifies a Site Failure (HTTP 503).
    """
    url = "https://down.fragile-site.com/products/test-item"
    
    with pytest.raises(SiteFailure) as excinfo:
        mock_agent_extraction(url)
    
    assert "Site Failure" in str(excinfo.value)
    assert "HTTP 503" in str(excinfo.value)
    print("Site health failure correctly identified.")

def test_alert_triggering(capsys):
    """
    Validate that an alert is triggered in the logs when a site failure occurs.
    """
    url = "https://down.fragile-site.com/products/test-item"
    
    with pytest.raises(SiteFailure):
        mock_agent_extraction(url)
    
    captured = capsys.readouterr()
    assert "Alert triggered" in captured.out or "MOCK: Sending Slack alert" in captured.out
    print("Alert triggering verified in logs.")

if __name__ == "__main__":
    # For manual local testing
    pytest.main([__file__])
