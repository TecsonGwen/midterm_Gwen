import sys
import argparse
import requests
from registry_client import RegistryClient

def main():
    parser = argparse.ArgumentParser(description="Update service status to maintenance and deregister.")
    parser.add_argument("service_id", type=int, help="Target Service ID")
    args = parser.parse_args()

    client = RegistryClient()
    svc_id = args.service_id

    try:
        before = client.get_service(svc_id)
        print(f"Status before: {before.get('status')}")

        client.patch_service(svc_id, {"status": "maintenance"})

        after = client.get_service(svc_id)
        print(f"Status after: {after.get('status')}")

        name = after.get("name", "unknown")
        client.delete_service(svc_id)
        print(f"Deregistered {name} (id {svc_id})")

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            print(f"Service with id {svc_id} not found, nothing to do.")
        else:
            print(f"API Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()