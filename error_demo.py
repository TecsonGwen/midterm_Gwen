import sys
import requests
from registry_client import RegistryClient

def run_test(desc, action):
    print(f"\n--- {desc} ---")
    try:
        action()
    except requests.exceptions.HTTPError as exc:
        code = exc.response.status_code if exc.response is not None else None
        print(f"HTTP Error {code}: {exc}")
    except requests.exceptions.RequestException as err:
        print(f"Connection failed: {err}")

def main():
    run_test("1. Triggering HTTP 401 Unauthorized", 
             lambda: RegistryClient(api_key="wrong-key").get_services())
    run_test("2. Triggering HTTP 404 Not Found", 
             lambda: RegistryClient().get_service(9999))
    sys.exit(0)

if __name__ == "__main__":
    main()