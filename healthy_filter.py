import json
import yaml
with open("service_catalog.yaml", "r") as f: 
    docs = list(yaml.safe_load_all(f))
    data = docs[0] if docs else {}
services = data.get("services", [])
status_counts = {"healthy": 0, "unhealthy": 0, "maintenance": 0}
healthy_services = []
for svc in services:
    status = str(svc.get("status", "")).lower()
    if status in status_counts:
        status_counts[status] += 1
    if status == "healthy":
        healthy_services.append(svc)
healthy_names = sorted([svc["name"] for svc in healthy_services])
healthy_catalog = dict(data)
healthy_catalog["services"] = healthy_services

with open("healthy_services.json", "w") as f:
    json.dump(healthy_catalog, f, indent=4)
print(
    f"Healthy: {status_counts['healthy']} | "
    f"Unhealthy: {status_counts['unhealthy']} | "
    f"Maintenance: {status_counts['maintenance']}\n"
)
print(f"Healthy services: {', '.join(healthy_names)}")