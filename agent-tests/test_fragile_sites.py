import time
import concurrent.futures
import pytest
from logic import mock_agent_extraction, SiteFailure
from unittest.mock import patch

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

def test_alert_triggering(mock_alerts):
    """
    Validate that an alert is triggered when a site failure occurs.
    """
    url = "https://down.fragile-site.com/products/test-item"
    
    with pytest.raises(SiteFailure):
        mock_agent_extraction(url)
    
    mock_alerts.assert_called_once()
    args, kwargs = mock_alerts.call_args
    assert "Site is unreachable" in args[0]
    print("Alert triggering verified via mock.")

def test_parallel_extractions():
    """
    Validate that the agent can extract data from multiple sites in parallel.
    Uses ThreadPoolExecutor to run 5 mock extractions concurrently.
    The mock extraction has a 1 second sleep, so 5 parallel calls should finish in ~1-1.5 seconds, not 5.
    """
    urls = [
        "https://fragile-site.com/products/item-1",
        "https://fragile-site.com/products/item-2",
        "https://fragile-site.com/products/item-3",
        "https://fragile-site.com/products/item-4",
        "https://fragile-site.com/products/item-5",
    ]
    
    start_time = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(mock_agent_extraction, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
                results.append(data)
            except SiteFailure as e:
                pytest.skip(f"Skipping parallel extraction test due to site failure: {e}")
    
    end_time = time.time()
    
    assert len(results) == 5
    for data in results:
        assert data is not None
        assert "price" in data
    
    duration = end_time - start_time
    assert duration < 3.0, f"Parallel execution took too long: {duration:.2f}s, expected < 3.0s"
    print(f"Parallel extraction of 5 sites completed successfully in {duration:.2f}s")

@pytest.fixture(autouse=True)
def mock_alerts():
    """Automatically mock send_alert for all tests to prevent log noise."""
    with patch("logic.send_alert") as mock:
        yield mock

if __name__ == "__main__":
    # For manual local testing
    pytest.main([__file__])
