import os
import requests
import argparse
import logging
from uuid import UUID

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def post_scan(api_key, test_uuid, assets):
    if not is_valid_uuid(api_key):
        logging.error("Invalid API Key")
        return

    if test_uuid and not is_valid_uuid(test_uuid):
        logging.error("Invalid TEST_UUID")
        return

    url = "https://api.informer.io/trigger"
    data = {
        "api_key": api_key,
        "assets": assets.split(',')
    }
    if test_uuid:
        data["test_uuid"] = test_uuid

    timeout = 10  # seconds

    try:
        response = requests.post(url, json=data, timeout=timeout)
        response.raise_for_status()
        logging.info(f"Scan triggered successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description='Trigger a scan with Informer.io.')
    parser.add_argument('--api_key', required=True, help='API Key for authorization')
    parser.add_argument('--test_uuid', help='UUID of the test object (optional)')
    parser.add_argument('--assets', required=True, help='Comma-separated list of assets to scan')

    args = parser.parse_args()

    api_key = args.api_key or os.getenv('API_KEY_ENV')
    test_uuid = args.test_uuid or os.getenv('TEST_UUID_ENV')

    if not api_key:
        logging.error("API Key must be provided either as an argument or as an environment variable.")
        return

    post_scan(api_key, test_uuid, args.assets)


if __name__ == "__main__":
    main()
