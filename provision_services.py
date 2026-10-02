import sys, requests
from registry_client import RegistryClient

def fetch_all(client):
    collected, offset, limit = [], 0, 10
    while True:
        page = client.get_services(limit=limit, offset=offset)
        results = page.get("results", [])
        collected.extend(results)
        offset += limit
        if offset >= page.get("count", 0) or not results:
            break

    return collected
def provision_services():
    client = RegistryClient()
    new_services = [
        {
            "name": "rewards-svc",
            "version": "0.1.0",
            "owner": "engagement@aeropay.io",
            "environment": "staging",
            "status": "healthy",
            "health_url": "/health/rewards",
            "dependencies": ["notification-svc"]
        },
        {
            "name": "audit-trail-svc",
            "version": "1.0.0",
            "owner": "compliance@aeropay.io",
            "environment": "production",
            "status": "healthy",
            "health_url": "/health/audit-trail",
            "dependencies": []
        },
        {
            "name": "rate-limiter",
            "version": "0.9.0",
            "owner": "platform@aeropay.io",
            "environment": "production",
            "status": "healthy",
            "health_url": "/health/rate-limiter",
            "dependencies": ["api-gateway", "auth-svc"]
        }
    ]

    try:
        existing_services = fetch_all(client)
        existing_names = {s["name"] for s in existing_services}
        for svc in new_services:
            if svc["name"] in existing_names:
                print(f"Already register: {svc['name']}")
                continue
                
            created = client.create_service(svc)
            verified = client.get_service(created["id"])
            print(f"Registered {verified['name']} with id {verified['id']}.")
            
    except requests.exceptions.RequestException:
        print("Error: Failed connect registry server.")
        sys.exit(0)
if __name__ == "_main_":
    provision_services()