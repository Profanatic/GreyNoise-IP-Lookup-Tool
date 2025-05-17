# GreyNoise-IP-Lookup-Tool
A Python CLI tool to query the GreyNoise Community API for detailed intelligence about IP addresses, including their classification, associated metadata, tags, and behavioral indicators.

📌 Features

🔍 Lookup single or multiple IP addresses via GreyNoise Community API.

🧠 Full parsing and structured tree output of all fields.

📁 Caching support to reduce API usage (optional).

🔖 Automatically extracts and highlights the name field (e.g., organization or hostname).

🌐 Direct links to GreyNoise Viz and API endpoints.

🚀 Installation

1. Clone the repository


git clone https://github.com/Profanatic/greynoise-ip-lookup.git

cd greynoise-ip-lookup

2. Install dependencies
   
This script uses only the Python standard library (requests is often pre-installed). If needed:

pip install requests

 API Key Configuration
 
The script requires a GreyNoise Community API key.

First-time users will be prompted to paste it 

The key will be saved securely at ~/.greynoise.conf.

You can also export it as an environment variable:

export GN_API_KEY="your-api-key-here"

Get your key from GreyNoise Community.

Usage

Single IP lookup

Editar
python3 greynoise_lookup.py 8.8.8.8

Multiple IPs

python3 greynoise_lookup.py 1.1.1.1 8.8.8.8

Ignore cache and force fresh lookup

python3 greynoise_lookup.py 8.8.8.8 --no-cache

Example Output

🛰️  Full result for IP: 45.14.226.146

🔖 Associated Name: Contabo GmbH

📌 ip: 45.14.226.146

📌 name: Contabo GmbH

📌 classification: benign

📌 metadata:

    📌 name: Contabo GmbH
    📌 org: CONTABO
    📌 country: DE


🔗 Visualization: https://viz.greynoise.io/ip/45.14.226.146

🔗 API Endpoint: https://api.greynoise.io/v3/community/45.14.226.146

👨‍💻 Author
Developed by Profanatica 

Inspired by cybersecurity investigations using GreyNoise data.

