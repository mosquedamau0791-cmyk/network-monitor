import pytest
from unittest.mock import Mock, patch, MagicMock
from network_monitor import NetworkMonitor


@pytest.fixture
def sample_hosts():
    """Fixture providing sample hosts for testing"""
    return ["8.8.8.8", "1.1.1.1", "google.com"]


@pytest.fixture
def monitor(sample_hosts):
    """Fixture providing a NetworkMonitor instance"""
    return NetworkMonitor(sample_hosts)


@pytest.fixture
def mock_config(tmp_path):
    """Fixture providing a mock config file"""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"email_enabled": false, "alert_on_down": true}')
    return str(config_file)


@pytest.fixture
def monitor_with_config(sample_hosts, mock_config):
    """Fixture providing a NetworkMonitor with config file"""
    return NetworkMonitor(sample_hosts, mock_config)
