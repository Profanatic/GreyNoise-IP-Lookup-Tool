#!/usr/bin/env python3
"""
GreyNoise IP Lookup 

"""

import requests
import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import time

# Configuration and cache files
CONFIG_FILE = Path.home() / ".greynoise.conf"
CACHE_FILE = Path.home() / ".greynoise_cache.json"
API_URL = "https://api.greynoise.io/v3/community/"
CACHE_EXPIRY = 86400  # 24 hours

class Config:
    def __init__(self):
        self.api_key = self._load_config()
        self.cache = self._load_cache()
        self.headers = {"Accept": "application/json", "key": self.api_key}

    def _load_config(self) -> str:
        """Load the API key from environment or config file"""
        if "GN_API_KEY" in os.environ:
            return os.environ["GN_API_KEY"]

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f).get("api_key", "")
            except (json.JSONDecodeError, IOError):
                pass

        print("⚠️ GreyNoise API key not found.")
        api_key = input("Enter your GreyNoise API key: ").strip()
        self._save_config(api_key)
        return api_key

    def _save_config(self, api_key: str):
        """Save the API key to the config file"""
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"api_key": api_key}, f)
            os.chmod(CONFIG_FILE, 0o600)
        except IOError as e:
            print(f"⚠️ Error saving configuration: {e}")

    def _load_cache(self) -> Dict[str, Any]:
        """Load cached responses"""
        if not CACHE_FILE.exists():
            return {}
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
                return {
                    k: v for k, v in cache.items()
                    if time.time() - v.get("timestamp", 0) < CACHE_EXPIRY
                }
        except (json.JSONDecodeError, IOError):
            return {}

    def save_cache(self):
        """Persist cache to disk"""
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(self.cache, f)
        except IOError as e:
            print(f"⚠️ Error saving cache: {e}")

def lookup_ip(ip_address: str, config: Config) -> Optional[Dict[str, Any]]:
    """Query GreyNoise API for the given IP address"""
    try:
        response = requests.get(
            API_URL + ip_address,
            headers=config.headers,
            timeout=15
        )

        if response.status_code == 200:
            return response.json()

        print(f"⚠️ API returned error [{response.status_code}]: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Connection error: {e}")
    return None

def print_json(data: Any, indent: int = 0):
    """Recursively print dictionary or list in a readable tree format"""
    prefix = ' ' * indent
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{prefix}📌 {k}:", end=" ")
            if isinstance(v, (dict, list)):
                print()
                print_json(v, indent + 4)
            else:
                print(v)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{prefix}- [{i}]")
            print_json(item, indent + 4)
    else:
        print(f"{prefix}{data}")

def extract_name(data: Dict[str, Any]) -> str:
    """Extract the 'name' field from any common location in the API response"""
    return (
        data.get("name") or
        data.get("metadata", {}).get("name") or
        data.get("metadata", {}).get("organization", {}).get("name") or
        "N/A"
    )

def format_output(data: Dict[str, Any]) -> str:
    """Format and display the full output from the GreyNoise API"""
    if not data:
        return "⛔ No data available for this IP"
    
    name = extract_name(data)

    print(f"\n{'='*60}")
    print(f"🛰️  Full result for IP: {data.get('ip', 'Unknown')}")
    print(f"🔖 Associated Name: {name}")
    print(f"{'='*60}")
    print_json(data)
    print(f"\n🔗 Visualization: https://viz.greynoise.io/ip/{data.get('ip', '')}")
    print(f"🔗 API Endpoint: {API_URL}{data.get('ip', '')}")
    print(f"{'='*60}\n")
    return ""

def validate_ip(ip_address: str) -> bool:
    """Basic IPv4 address format validation"""
    parts = ip_address.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser(
        description="GreyNoise IP Intelligence Lookup (Complete Version)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("ips", nargs="+", help="IP address(es) to lookup")
    parser.add_argument("--no-cache", action="store_true", help="Ignore cache and force fresh lookup")

    args = parser.parse_args()
    config = Config()

    for ip in args.ips:
        if not validate_ip(ip):
            print(f"⚠️ Invalid IP address: {ip}")
            continue

        if not args.no_cache and ip in config.cache:
            print(f"✅ [CACHE] Result for {ip}")
            print(format_output(config.cache[ip]))
            continue

        data = lookup_ip(ip, config)
        if data:
            print(format_output(data))
            if not args.no_cache:
                config.cache[ip] = data | {"timestamp": time.time()}

    if not args.no_cache:
        config.save_cache()

if __name__ == "__main__":
    main()

