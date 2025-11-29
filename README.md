<p align="center">
  <h1 align="center">David Hill - Docs Automation</h1>
  <p align="center">
    <strong>Google Docs Integration for Inspection Reports</strong>
  </p>
  <p align="center">
    Google Docs API | Automation | Report Generation | Python
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google-Docs_API-green?logo=google&logoColor=white" alt="Google Docs">
  <img src="https://img.shields.io/badge/License-Private-gray" alt="License">
</p>

---

## Overview

Automation tool for generating Google Docs reports from inspection data. Integrates with the David Hill racking inspection system to automatically create formatted inspection reports in Google Docs.

---

## Key Features

### Automation
- **Document Creation**: Automatically create Google Docs from templates
- **Data Population**: Populate reports with inspection data
- **Formatting**: Apply standard formatting and styling

### Integration
- **Google Drive API**: Manage file storage and organization
- **Google Docs API**: content generation and formatting
- **JSON Integration**: Read inspection data from output files

---

## Quick Start

### Prerequisites
- Python 3.9+
- Google Cloud Project credentials (JSON)
- Inspection data output

### Installation
```bash
git clone https://github.com/badkirked/david-hill.git
cd david-hill
pip install -r requirements.txt
```

### Usage
```bash
python3 create_google_doc.py
```

---

## Project Structure

```
david-hill/
├── create_google_doc.py  # Main automation script
├── config.json           # API configuration
└── form_config.json      # Report structure
```

---

## License

Private repository - All rights reserved.

---

## Author

**badkirked**

- GitHub: [@badkirked](https://github.com/badkirked)

---

<p align="center">
  <sub>Built for automated reporting</sub>
</p>
