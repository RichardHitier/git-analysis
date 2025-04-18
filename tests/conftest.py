import os
import pytest


@pytest.fixture
def pomofocus_file():
    return os.path.join(os.path.dirname(__file__), 'resources-tests', 'pomo-tests.csv')
