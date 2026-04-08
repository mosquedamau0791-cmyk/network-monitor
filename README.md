# Network Monitor 🌐

A professional Python application for monitoring network host availability with email alerts, logging, and configuration management.

## Features

✅ **Cross-Platform Support** - Works on Windows, Linux, and macOS  
✅ **Batch Host Monitoring** - Monitor multiple hosts simultaneously  
✅ **Email Alerts** - Receive notifications when hosts go down  
✅ **JSON Configuration** - Easy-to-use configuration file  
✅ **Comprehensive Logging** - File and console logging  
✅ **JSON Results Export** - Save monitoring results for analysis  
✅ **Unit Tests** - 12+ test cases with pytest  
✅ **Docker Support** - Containerized deployment  
✅ **CI/CD Pipeline** - Automated testing with GitHub Actions  
✅ **Type Hints** - Professional Python standards  

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/mosquedamau0791-cmyk/network-monitor.git
cd network-monitor
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Configuration

Create or edit `config.json` to customize settings:

```json
{
  "email_enabled": false,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "recipient_email": "recipient@example.com",
  "alert_on_down": true
}
```

**Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

## Usage

### Basic Usage
```bash
python network_monitor.py 8.8.8.8 1.1.1.1 google.com
```

### Monitor Default Hosts
```bash
python network_monitor.py
```

### Output
The application generates:
- **Console output** - Real-time monitoring status
- **network_monitor.log** - Detailed logging
- **monitoring_results.json** - JSON results export

## Example Output

```
==================================================
NETWORK MONITORING SUMMARY
==================================================
Timestamp: 2026-04-08T10:30:45.123456
Hosts Checked: 3
Hosts UP: 3
Hosts DOWN: 0
--------------------------------------------------
✓ 8.8.8.8             UP
✓ 1.1.1.1             UP
✓ google.com          UP
==================================================
```

## Docker Usage

### Build Docker Image
```bash
docker build -t network-monitor .
```

### Run in Docker
```bash
docker run network-monitor 8.8.8.8 1.1.1.1 google.com
```

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=. --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_network_monitor.py::TestNetworkMonitor::test_ping_host -v
```

## Project Structure

```
network-monitor/
├── network_monitor.py          # Main application
├── config.json                 # Configuration file
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .gitignore                  # Git ignore file
├── README.md                   # This file
├── network_monitor.log         # Application logs (generated)
├── monitoring_results.json     # Results export (generated)
└── tests/
    ├── conftest.py            # Pytest configuration
    └── test_network_monitor.py # Unit tests
```

## Technologies Used

- **Python 3.8+** - Core language
- **pytest** - Unit testing framework
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **SMTP** - Email notifications
- **JSON** - Configuration & data storage

## CI/CD Pipeline

The project includes automated testing on multiple Python versions (3.8, 3.9, 3.10, 3.11) via GitHub Actions.

View the workflow: `.github/workflows/tests.yml`

## Error Handling

The application includes robust error handling for:
- Network connectivity issues
- Configuration file errors
- Email sending failures
- OS-specific ping command variations

All errors are logged with detailed information.

## Contributing

Feel free to fork this repository and submit pull requests!

## License

MIT License - See LICENSE file for details

## Author

**Your Name** - Network Monitoring Application  
GitHub: [@mosquedamau0791-cmyk](https://github.com/mosquedamau0791-cmyk)

## Support

For issues, questions, or suggestions, please open a GitHub issue.

---

**Built as a professional portfolio project demonstrating Python best practices, testing, and DevOps skills.**
