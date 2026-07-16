import json

KEY_FILE = "/home/franc/GitHub/sensible-docs/.claude/webflow-update/find-replace-key-config-library.json"
REMOVE = {"local_path", "upload_url", "webflow_url"}

with open(KEY_FILE) as f:
    data = json.load(f)

for entry in data:
    for field in REMOVE:
        entry.pop(field, None)

with open(KEY_FILE, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print(f"Stripped fields from {len(data)} entries.")
