#!/usr/bin/env python3
"""
Network Monitor - A professional network monitoring application
Pings hosts and logs their status with error handling and configuration
"""

import os
import sys
import json
import logging
import smtplib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NetworkMonitor:
    """Monitor network hosts and their connectivity status"""
    
    def __init__(self, hosts: List[str], config_file: str = "config.json"):
        """
        Initialize the network monitor
        
        Args:
            hosts: List of host IPs or domains to monitor
            config_file: Configuration file path
        """
        self.hosts = hosts
        self.config_file = config_file
        self.results = []
        self.os_type = platform.system()
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load config file: {str(e)}")
        return {
            "email_enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "",
            "sender_password": "",
            "recipient_email": "",
            "alert_on_down": True
        }
    
    def _get_ping_command(self, host: str) -> str:
        """Generate OS-specific ping command"""
        if self.os_type == "Windows":
            return f"ping -n 1 {host}"
        else:  # Linux, macOS
            return f"ping -c 1 {host}"
    
    def ping_host(self, host: str) -> Tuple[bool, int]:
        """
        Ping a single host
        
        Args:
            host: IP address or domain to ping
            
        Returns:
            Tuple of (is_up: bool, response_time: int)
        """
        try:
            command = self._get_ping_command(host)
            response = os.system(command + " > /dev/null 2>&1")
            is_up = response == 0
            return is_up, response
        except Exception as e:
            logger.error(f"Error pinging {host}: {str(e)}")
            return False, -1
    
    def send_alert_email(self, host: str, status: str):
        """
        Send email alert when host status changes
        
        Args:
            host: Host that changed status
            status: Current status (UP/DOWN)
        """
        if not self.config.get("email_enabled"):
            return
        
        try:
            sender = self.config.get("sender_email")
            password = self.config.get("sender_password")
            recipient = self.config.get("recipient_email")
            
            if not all([sender, password, recipient]):
                logger.warning("Email configuration incomplete")
                return
            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = f"Network Alert: {host} is {status}"
            
            body = f"""
            Network Monitoring Alert
            
            Host: {host}
            Status: {status}
            Time: {datetime.now().isoformat()}
            
            Please check the host immediately if it's DOWN.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config.get("smtp_server"), self.config.get("smtp_port"))
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Alert email sent for {host}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
    
    def monitor_all_hosts(self) -> Dict:
        """
        Monitor all hosts and return results
        
        Returns:
            Dictionary containing monitoring results
        """
        logger.info(f"Starting network monitoring for {len(self.hosts)} hosts")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "hosts_checked": len(self.hosts),
            "hosts_up": 0,
            "hosts_down": 0,
            "details": []
        }
        
        for host in self.hosts:
            is_up, response_code = self.ping_host(host)
            status = "UP" if is_up else "DOWN"
            
            host_info = {
                "host": host,
                "status": status,
                "response_code": response_code,
                "checked_at": datetime.now().isoformat()
            }
            
            results["details"].append(host_info)
            
            if is_up:
                results["hosts_up"] += 1
                logger.info(f"✓ {host} is UP")
            else:
                results["hosts_down"] += 1
                logger.warning(f"✗ {host} is DOWN")
                if self.config.get("alert_on_down"):
                    self.send_alert_email(host, "DOWN")
        
        self.results = results
        return results
    
    def save_results(self, output_file: str = "monitoring_results.json"):
        """Save monitoring results to JSON file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
    
    def print_summary(self):
        """Print a formatted summary of monitoring results"""
        if not self.results:
            logger.warning("No results to display")
            return
        
        print("\n" + "="*50)
        print("NETWORK MONITORING SUMMARY")
        print("="*50)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Hosts Checked: {self.results['hosts_checked']}")
        print(f"Hosts UP: {self.results['hosts_up']}")
        print(f"Hosts DOWN: {self.results['hosts_down']}")
        print("-"*50)
        
        for detail in self.results['details']:
            status_symbol = "✓" if detail['status'] == "UP" else "✗"
            print(f"{status_symbol} {detail['host']:<20} {detail['status']}")
        
        print("="*50 + "\n")


def main():
    """Main entry point"""
    # Default hosts to monitor
    hosts = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
    
    # Allow command-line host specification
    if len(sys.argv) > 1:
        hosts = sys.argv[1:]
    
    # Create and run monitor
    monitor = NetworkMonitor(hosts)
    monitor.monitor_all_hosts()
    monitor.print_summary()
    monitor.save_results()
    
    logger.info("Network monitoring completed")


if __name__ == "__main__":
    main()
