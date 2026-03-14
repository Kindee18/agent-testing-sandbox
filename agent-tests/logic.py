import time

# Mock AgentQL/TinyFish semantic extraction
def mock_agent_extraction(url):
    """
    Simulates semantic extraction from a fragile website.
    """
    time.sleep(1) # Reduced lead time for testing
    if "fragile-site.com" in url:
        return {
            "title": "Welcome to the Fragile Site",
            "price": "$49.99",
            "availability": "In Stock"
        }
    return None
