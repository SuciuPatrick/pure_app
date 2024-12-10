import logging

import pytest
from rest_framework.test import APIClient


# Disable logging for tests
@pytest.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def api_client():
    return APIClient()
