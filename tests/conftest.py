import os
import sys
import pytest


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables and paths."""
    # Add the src directory to Python path for test imports
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Set up test environment variables
    os.environ["BUCKET_NAME"] = "test-bucket"
    os.environ["TABLE_NAME"] = "test-table"
    os.environ["API_KEY"] = "test-api-key"
    os.environ["API_ENDPOINT"] = "https://test-api.example.com"

    yield

    # Clean up environment variables after tests
    del os.environ["BUCKET_NAME"]
    del os.environ["TABLE_NAME"]
    del os.environ["API_KEY"]
    del os.environ["API_ENDPOINT"]
