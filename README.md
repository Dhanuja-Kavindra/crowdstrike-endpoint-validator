# crowdstrike-endpoint-validator
Lightweight Python script to validate CrowdStrike endpoint visibility and reporting status via EDR API integration.

# Endpoint Coverage Validation Tool  
**Automated EDR Host Presence Checker (Python + REST API)**  

---

## Overview
This Python-based automation tool validates endpoint coverage by verifying whether specified hosts are reporting to an Endpoint Detection and Response (EDR) platform through its REST API.  
It was developed to eliminate manual verification tasks, ensuring that all endpoints listed in an input inventory are properly registered and visible in the EDR console.  

The script authenticates using OAuth2 credentials, queries host data by hostname and IP address, and outputs a structured CSV file indicating the reporting status of each endpoint.

---

## Key Features
- Secure API authentication using OAuth2.
- Automated validation of endpoints by hostname and IP address.
- Handles hostname variations with and without domain suffixes.
- Generates a CSV report summarizing EDR reporting status.
- Designed for efficiency in Security Operations Center (SOC) workflows.

---

## Technical Summary
| Component | Description |
|------------|-------------|
| **Language** | Python 3.x |
| **Libraries** | `requests`, `csv`, `json`, `time` |
| **Authentication** | OAuth2 Client Credentials |
| **API Endpoints** | `/oauth2/token`, `/devices/queries/devices/v1` |
| **Input/Output Format** | CSV |
| **Execution** | Command-line |

---

## Input File Format
- **File Type:** CSV (`.csv`)  
- **Delimiter:** Comma (`,`)  
- **Required Columns (example header):**
  ```text
  hostid,Host Name,Visible Name,Server IP,AtlasID,groupid
  ```
- The script reads:
  - `Host Name` from **column index 1**
  - `Server IP` from **column index 3**

Each record represents one endpoint to be validated against the EDR console.

You can easily **adapt the script** to match your own input file structure by updating the column indices in the section where `hostname` and `IP` values are defined.  
This flexibility allows the tool to work with custom asset lists or data exports from different systems.

---

## Output File Format
- **File Type:** CSV (`.csv`)  
- **Contains:** All original columns plus one additional field appended at the end.

| hostid | Host Name | Visible Name | Server IP | AppID | groupid | cs_report_status |
|--------|------------|--------------|------------|----------|----------|------------------|
| 11290 | sample-host | sample-host | 10.10.10.10 | APP-001 | Linux | Reporting to CS Console. |
| 15398 | sample-host | sample-host | 10.10.10.10 | APP-002 | Linux | Not Reporting to CS Console. |

**cs_report_status** indicates whether the host is reporting to the EDR console.

---

## Execution
1. Place the input CSV file (e.g., `inputfilesample.csv`) in the same directory as the script.  
2. Run the script in a Python environment:
   ```bash
   python HostChecker.py
   ```
3. The output CSV file (e.g., `sampleoutput.csv`) will be created in the same directory with updated reporting statuses.

---

## Repository Structure
```
.
├── HostChecker.py          # Main Python script
└── README.md               # Documentation
```

---

## Security and Privacy Notice
This repository is for demonstration purposes only and does not include:
- Real hostnames or IP addresses  
- API credentials or tokens  
- Any organization-specific details

---

## License
This project is intended for educational and professional demonstration use.  
Please review and adapt it responsibly according to your organization’s policies and API usage guidelines.


