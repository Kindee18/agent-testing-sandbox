from logic import mock_agent_extraction

def test_price_extraction():
    """
    Validate that the agent can still extract prices accurately.
    """
    url = "https://fragile-site.com/products/test-item"
    data = mock_agent_extraction(url)
    
    assert data is not None
    assert "price" in data
    assert data["price"] == "$49.99"
    print(f"Price extraction test passed: {data['price']}")

def test_availability_extraction():
    """
    Validate that the agent can still extract availability status.
    """
    url = "https://fragile-site.com/products/test-item"
    data = mock_agent_extraction(url)
    
    assert data is not None
    assert "availability" in data
    assert data["availability"] == "In Stock"
    print(f"Availability extraction test passed: {data['availability']}")

if __name__ == "__main__":
    # For manual local testing
    pytest.main([__file__])
