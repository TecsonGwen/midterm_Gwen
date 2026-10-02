import argparse
import sys
from registry_client import RegistryClient

def fetch_all(client, status=None):
    collected, offset, limit = [], 0, 10
    while True:
        page = client.get_services(limit=limit, offset=offset, status=status)
        collected.extend(page["results"])
        offset += limit
        if offset >= page["count"]:
            break
    return collected
def main():
    parser = argparse.ArgumentParser(description="Generate Inventory Report")
    parser.add_argument("--status", help="Filter services by status", default=None)
    args = parser.parse_args()
    try:
        client = RegistryClient()
        services = fetch_all(client, status=args.status)
        header = f"{'ID':<5} | {'NAME':<20} | {'VERSION':<10} | {'STATUS':<10} | {'ENVIRONMENT':<12}"
        print(header)
        print("-" * len(header))
        for svc in services:
            print(
                f"{str(svc.get('id', '')):<5} | "
                f"{str(svc.get('name', '')):<20} | "
                f"{str(svc.get('version', '')):<10} | "
                f"{str(svc.get('status', '')):<10} | "
                f"{str(svc.get('environment', '')):<12}"
            )
    except Exception as e:
        print("Error: Unable to connect to the service registry or invalid API key.")
        sys.exit(0)
if __name__ == "_main_" :
     main()