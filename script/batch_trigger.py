#!/usr/bin/env python3
import json
import os
import tempfile

# Get the batch context variables
container_type = os.environ.get("container_type", "")
container_id = os.environ.get("container_id", "")
container_title = os.environ.get("container_title", "")
item_type = os.environ.get("item_type", "")

# Write batch context to a temporary file
batch_data = {
    "batch_context": "true",
    "container_type": container_type,
    "container_id": container_id,
    "container_title": container_title,
    "item_type": item_type
}

# Write to temp file in script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
batch_file = os.path.join(script_dir, ".batch_context.json")

with open(batch_file, 'w') as f:
    json.dump(batch_data, f)

# Output for Alfred - trigger the ReChooseList to restart the workflow
result = {
    "alfredworkflow": {
        "arg": "",
        "variables": {
            "batch_context": "true",
            "container_type": container_type,
            "container_id": container_id,
            "container_title": container_title,
            "item_type": item_type
        }
    }
}

print(json.dumps(result))