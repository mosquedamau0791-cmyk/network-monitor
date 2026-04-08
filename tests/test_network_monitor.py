import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from network_monitor import NetworkMonitor


class TestNetworkMonitor:
    """Test suite for NetworkMonitor class"""
    
    def test_initialization(self, sample_hosts):
        """Test NetworkMonitor initialization"""
        monitor = NetworkMonitor(sample_hosts)
        assert monitor.hosts == sample_hosts
        assert monitor.config_file == "config.json"
        assert monitor.results == []
    
    def test_initialization_with_custom_config(self, sample_hosts):
        """Test NetworkMonitor initialization with custom config file"""
        monitor = NetworkMonitor(sample_hosts, "custom_config.json")
        assert monitor.config_file == "custom_config.json"
    
    def test_load_config_file_exists(self, monitor_with_config):
        """Test loading config when file exists"""
        config = monitor_with_config.config
        assert isinstance(config, dict)
        assert "email_enabled" in config
    
    def test_load_config_file_not_exists(self, monitor):
        """Test loading config when file doesn't exist"""
        config = monitor.config
        assert isinstance(config, dict)
        assert config["email_enabled"] is False
    
    def test_get_ping_command_windows(self, monitor):
        """Test ping command for Windows"""
        with patch.object(monitor, 'os_type', 'Windows'):
            command = monitor._get_ping_command("8.8.8.8")
            assert "ping -n 1" in command
            assert "8.8.8.8" in command
    
    def test_get_ping_command_linux(self, monitor):
        """Test ping command for Linux"""
        with patch.object(monitor, 'os_type', 'Linux'):
            command = monitor._get_ping_command("8.8.8.8")
            assert "ping -c 1" in command
            assert "8.8.8.8" in command
    
    def test_get_ping_command_macos(self, monitor):
        """Test ping command for macOS"""
        with patch.object(monitor, 'os_type', 'Darwin'):
            command = monitor._get_ping_command("8.8.8.8")
            assert "ping -c 1" in command
    
    @patch('os.system')
    def test_ping_host_up(self, mock_system, monitor):
        """Test pinging a host that's up"""
        mock_system.return_value = 0
        is_up, response = monitor.ping_host("8.8.8.8")
        assert is_up is True
        assert response == 0
    
    @patch('os.system')
    def test_ping_host_down(self, mock_system, monitor):
        """Test pinging a host that's down"""
        mock_system.return_value = 1
        is_up, response = monitor.ping_host("8.8.8.8")
        assert is_up is False
        assert response == 1
    
    @patch('os.system')
    def test_ping_host_exception(self, mock_system, monitor):
        """Test ping_host when exception occurs"""
        mock_system.side_effect = Exception("Ping failed")
        is_up, response = monitor.ping_host("8.8.8.8")
        assert is_up is False
        assert response == -1
    
    @patch('smtplib.SMTP')
    def test_send_alert_email_enabled(self, mock_smtp, monitor_with_config):
        """Test sending email alert when enabled"""
        config = monitor_with_config.config
        config["email_enabled"] = True
        config["sender_email"] = "test@gmail.com"
        config["sender_password"] = "password"
        config["recipient_email"] = "recipient@gmail.com"
        
        monitor_with_config.send_alert_email("8.8.8.8", "DOWN")
        mock_smtp.assert_called()
    
    def test_send_alert_email_disabled(self, monitor_with_config):
        """Test email not sent when disabled"""
        with patch('smtplib.SMTP') as mock_smtp:
            monitor_with_config.send_alert_email("8.8.8.8", "DOWN")
            mock_smtp.assert_not_called()
    
    @patch('os.system')
    def test_monitor_all_hosts(self, mock_system, monitor):
        """Test monitoring all hosts"""
        mock_system.return_value = 0
        results = monitor.monitor_all_hosts()
        
        assert results["hosts_checked"] == len(monitor.hosts)
        assert results["hosts_up"] == len(monitor.hosts)
        assert results["hosts_down"] == 0
        assert len(results["details"]) == len(monitor.hosts)
    
    @patch('os.system')
    def test_monitor_all_hosts_mixed_status(self, mock_system, monitor):
        """Test monitoring with mixed host statuses"""
        mock_system.side_effect = [0, 1, 0]
        results = monitor.monitor_all_hosts()
        
        assert results["hosts_up"] == 2
        assert results["hosts_down"] == 1
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_results(self, mock_file, monitor):
        """Test saving results to file"""
        monitor.results = {
            "timestamp": "2026-04-08T10:30:00",
            "hosts_checked": 3,
            "hosts_up": 3,
            "hosts_down": 0,
            "details": []
        }
        monitor.save_results("test_results.json")
        mock_file.assert_called_with("test_results.json", 'w')
    
    @patch('os.system')
    def test_print_summary(self, mock_system, monitor, capsys):
        """Test printing summary"""
        mock_system.return_value = 0
        monitor.monitor_all_hosts()
        monitor.print_summary()
        
        captured = capsys.readouterr()
        assert "NETWORK MONITORING SUMMARY" in captured.out
        assert "Hosts Checked:" in captured.out
        assert "Hosts UP:" in captured.out
    
    @patch('os.system')
    def test_monitor_result_structure(self, mock_system, monitor):
        """Test structure of monitoring results"""
        mock_system.return_value = 0
        results = monitor.monitor_all_hosts()
        
        assert "timestamp" in results
        assert "hosts_checked" in results
        assert "hosts_up" in results
        assert "hosts_down" in results
        assert "details" in results
        
        for detail in results["details"]:
            assert "host" in detail
            assert "status" in detail
            assert "response_code" in detail
            assert "checked_at" in detail


class TestNetworkMonitorIntegration:
    """Integration tests for NetworkMonitor"""
    
    @patch('os.system')
    def test_full_monitoring_cycle(self, mock_system, monitor, tmp_path):
        """Test full monitoring cycle"""
        mock_system.return_value = 0
        
        # Monitor hosts
        monitor.monitor_all_hosts()
        
        # Save results
        output_file = str(tmp_path / "results.json")
        monitor.save_results(output_file)
        
        # Verify results were saved
        assert Path(output_file).exists()
        with open(output_file, 'r') as f:
            data = json.load(f)
            assert data["hosts_up"] == len(monitor.hosts)
