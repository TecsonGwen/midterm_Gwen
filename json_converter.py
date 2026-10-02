import json, yaml
with open("service_catalog.yaml", "r") as f:
    data = yaml.safe_load(f) # a Python dict
with open("service_catalog.json", "w") as f:
    json.dump(data, f, indent=4)
print(f"Converted {len(data['services'])} services")