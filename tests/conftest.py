import json
import pathlib

import pytest

from wekan.client import WeKanClient

CONFIG_PATH = pathlib.Path(__file__).parent.parent / "test_config.json"


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: end-to-end tests against live WeKan server"
    )


@pytest.fixture(scope="session")
def test_config():
    print(CONFIG_PATH)
    if not CONFIG_PATH.exists():
        pytest.skip(
            "tests/test_config.json not found - copy test_config.json.example and fill in credentials"
        )
    return json.loads(CONFIG_PATH.read_text())


@pytest.fixture(scope="session")
def client(test_config):
    c = WeKanClient(
        test_config["url"], test_config["username"], test_config["password"]
    )
    c.login()
    return c
