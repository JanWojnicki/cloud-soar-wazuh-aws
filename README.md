# Autonomous Cloud SOAR System: AWS Incident Response Automation with Wazuh SIEM
Authors: Jan Wojnicki, Adrian Sajdak

An enterprise-grade, event-driven SOAR (Security Orchestration, Automation, and Response) system deployed in public cloud infrastructure (AWS). The system independently correlates telemetry data, detects early-stage network attacks (reconnaissance, multi-stage vectors), and executes automated mitigation at the network perimeter in real time without human intervention.

## 🚀 Key Features
* **Proactive & Reactive Defense:** Supports immediate block on stealth scanning or advanced time-correlated incident response (e.g., Reconnaissance followed by SSH brute-force simulation).
* **API-Driven Infrastructure Security:** Integrates third-party containerized SIEM with cloud native APIs.
* **Serverless Execution Playbook:** Uses AWS API Gateway and AWS Lambda (Python/Boto3) to build stateless mitigation streams.
* **Algorithmic Constraint Handling:** Implements dynamic Network ACL rule number allocation (`random` distribution) to bypass cloud architecture limits and avoid rule collision.
* **Data Normalization Engine:** Cascading JSON parser capable of handling disparate log schemas (standard SIEM fields vs. native AWS VPC Flow Logs formats).

## 🛠️ Architecture & Data Pipeline
1. **Telemetry Generation:** AWS VPC Flow Logs monitor EC2 instance interfaces and dump compressed metadata into Amazon S3 buckets.
2. **Ingestion & Analysis:** A containerized Wazuh Manager fetches logs via the `wazuh-aws` module, normalizes payloads, and triggers custom correlation rules.
3. **Orchestration:** `wazuh-integratord` executes a `custom-webhook` script sending critical alerts (JSON format) to AWS API Gateway.
4. **Automated Response:** AWS Lambda executes a Python script that parses the attacker's IP and injects a high-priority `DENY` rule into the VPC Network ACL.

## 📂 Repository Structure
* `/aws/lambda/`: Production-ready Lambda execution script using `boto3`.
* `/wazuh/rules/`: Custom XML correlation rules mapping to MITRE ATT&CK tactics.
* `/wazuh/config/`: Configuration mapping for cloud integration modules.
* `/docker/`: Single-node deployment recipe.

## 📊 Detection Engineering (Custom Rules)
The core analytical capabilities rely on custom correlation logic inside `local_rules.xml`:
* **Rule 100002:** Critical visibility warning - detection of public security group openings (`0.0.0.0/0`).
* **Rule 100003:** Port scanning detection based on frequency aggregation of `REJECT` packets.
* **Rule 100011:** Detection of SSH connection attempt. 
* **Rule 100004:** Multi-stage correlation. Connects early reconnaissance with targeted SSH authentication attempts within an elastic time window, compensating for cloud logging latency.

## 🧪 Simulation & E2E Validation
The architecture was stress-tested using a remote Kali Linux machine in a black-box scenario:
1. **Reconnaissance phase:** Triggered via aggressive `nmap -p 1-1000 -T4 -Pn <Target_IP>`.
2. **Exploitation attempt:** Multi-threaded target connection attempts on port 22.
3. **Mitigation verification:** System executed a full lifecycle response under 10 minutes (AWS S3 buffer constraint), effectively isolating the threat actor. Real-world botnets scanning the infrastructure were also autonomously blocked during the operational window.
