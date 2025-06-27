#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers.input import processInput
from helpers.models import ActionType, ItemType
import json
import os

def main():
    
    input_text, notes = processInput()
    action = os.environ.get("action", ActionType.ADD.value)
    item_type = os.environ.get("item_type", ItemType.TASK.value)
    container_type = os.environ.get("container_type", "")
    container_id = os.environ.get("container_id", "")
    container_title = os.environ.get("container_title", "")

    result = {
        "items": [
            {
                "title": "Batch add...",
                "subtitle": f"Batch add {input_text} to {container_title} (⌘+⏎ to end batch)",
                "valid": True,
                "mods": {
                    "cmd": {
                        "variables": {
                            "input_text": input_text,
                            "notes": notes,
                            "action": action,
                            "item_type": item_type,
                            "container_id": container_id,
                            "container_type": container_type,
                            "container_title": container_title,
                            "batch": 1
                        },
                        "subtitle": f"Finish batch to {container_title} with {input_text}"
                    }
                }
            }
        ],
        "alfredworkflow": {
            "variables": {
                "input_text": input_text,
                "notes": notes
            }
        }
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()