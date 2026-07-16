import json

KEY_FILE = "/home/franc/GitHub/sensible-docs/.claude/webflow-update/pdf-upload-key.json"
FIELD_ORDER = ["description", "local_path", "upload_url", "original_links", "new_links", "posts", "webflow_url"]

with open(KEY_FILE) as f:
    data = json.load(f)

reordered = []
for entry in data:
    ordered = {k: entry[k] for k in FIELD_ORDER if k in entry}
    for k in entry:
        if k not in ordered:
            ordered[k] = entry[k]
    reordered.append(ordered)

with open(KEY_FILE, "w") as f:
    json.dump(reordered, f, indent=2)
    f.write("\n")

print(f"Reordered {len(reordered)} entries.")
