import time
import os
import json
try:
    import requests
except ImportError:
    requests = None

def check_site_health(url):
    """
    Performs a pre-check to distinguish between Site Downtime and Agent Failures.
    In a real scenario, this would check HTTP status codes.
    """
    if "down.fragile-site.com" in url:
        return False, "Site is unreachable (HTTP 503)"
    return True, "Site is healthy"

def send_alert(message):
    """
    Sends a failure alert to a Slack or Discord webhook.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print(f"DEBUG: Alert triggered but no SLACK_WEBHOOK_URL set: {message}")
        return False

    payload = {"text": f"🚨 *TinyFish Agent Alert* 🚨\n\n{message}"}
    
    if requests:
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"ERROR: Failed to send alert: {e}")
            return False
    else:
        print(f"MOCK: Sending Slack alert via payload: {json.dumps(payload)}")
        return True

# Mock AgentQL/TinyFish semantic extraction
def mock_agent_extraction(url):
    """
    Simulates semantic extraction from a fragile website.
    """
    # Pre-check health
    is_healthy, message = check_site_health(url)
    if not is_healthy:
        error_msg = f"CRITICAL: Extraction blocked by Site Failure. Reason: {message}"
        send_alert(error_msg)
        raise Exception(error_msg)

    time.sleep(1) # Reduced lead time for testing
    if "fragile-site.com" in url:
        return {
            "title": "Welcome to the Fragile Site",
            "price": "$49.99",
            "availability": "In Stock"
        }
    return None
