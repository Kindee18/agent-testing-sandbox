import sys
import os

# Add the directory to the path
sys.path.append(os.path.join(os.getcwd(), 'agent-tests'))

from logic import mock_agent_extraction

def smoke_test():
    print("Running Smoke Test (Dependency-Free)...")
    url = "https://fragile-site.com/products/test-item"
    data = mock_agent_extraction(url)
    
    if data and data['price'] == "$49.99" and data['availability'] == "In Stock":
        print("✅ Core Extraction Logic Verified!")
    else:
        print("❌ Core Extraction Logic Failed!")
        exit(1)

if __name__ == "__main__":
    smoke_test()
