import time

def check_site_health(url):
    """
    Performs a pre-check to distinguish between Site Downtime and Agent Failures.
    In a real scenario, this would check HTTP status codes.
    """
    if "down.fragile-site.com" in url:
        return False, "Site is unreachable (HTTP 503)"
    return True, "Site is healthy"

# Mock AgentQL/TinyFish semantic extraction
def mock_agent_extraction(url):
    """
    Simulates semantic extraction from a fragile website.
    """
    # Pre-check health
    is_healthy, message = check_site_health(url)
    if not is_healthy:
        raise Exception(f"CRITICAL: Extraction blocked by Site Failure. Reason: {message}")

    time.sleep(1) # Reduced lead time for testing
    if "fragile-site.com" in url:
        return {
            "title": "Welcome to the Fragile Site",
            "price": "$49.99",
            "availability": "In Stock"
        }
    return None
