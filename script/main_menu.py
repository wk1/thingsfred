#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import subprocess
import os
from helpers.theming import get_icon_theme
from helpers.models import ItemType, ContainerType, ActionType

script_dir = os.path.dirname(os.path.abspath(__file__))
update_script = os.path.join(script_dir, "helpers/theming.py")
subprocess.run([sys.executable, update_script], capture_output=True)


theme = get_icon_theme()
query = sys.argv[1] if len(sys.argv) > 1 else ""

if "///" in query:
    parts = query.split("///", 1)
    input_text = parts[0].strip()
    notes = parts[1].strip()
else:
    input_text = query.strip()
    notes = ""


items = []

if input_text:

    items.append({
        "title": f"Inbox",
        "subtitle": f"Create \"{input_text}\" in Inbox",
        "arg": input_text,
        "variables": {
            "input_text": input_text,
            "notes": notes,
            "action": ActionType.ADD.value,
            "item_type": ItemType.TASK.value,
            "container_type": ContainerType.INBOX.value,
        },
        "icon": {"path": f"icons/{theme}/inbox.png"},
        "valid": True
    })

    items.append({
        "title": f"Today",
        "subtitle": f"Create \"{input_text}\" in Today",
        "arg": input_text,
        "variables": {
            "input_text": input_text,
            "notes": notes,
            "action": ActionType.ADD.value,
            "item_type": ItemType.TASK.value,
            "container_type": ContainerType.TODAY.value,
        },
        "icon": {"path": f"icons/{theme}/today.png"},
        "valid": True,
        "mods": {
            "option": {
                "valid": True,
                "arg": input_text,
                "variables": {
                    "input_text": input_text,
                    "notes": notes,
                    "action": ActionType.ADD.value,
                    "item_type": ItemType.PROJECT.value,
                    "container_type": ContainerType.TODAY.value,
                },
                "subtitle": f"Create PROJECT \"{input_text}\" for Today"
            }
        }
    })

    items.append({
        "title": f"→ Browse...",
        "subtitle": "Browse Areas / Projects to create Task",
        "arg": input_text, #empty arg is not supported by Alfred, need to clear this in an additional "Arg & Vars" block
        "variables": {
            "input_text": input_text,
            "notes": notes,
            "action": ActionType.BROWSE.value,
        },
        "icon": {"path": f"icons/{theme}/list.png"},
        "valid": True
    })
else:
    # Hilfe anzeigen wenn kein Task-Name
    items.append({
        "title": "Thingsfred",
        "subtitle": "Type ++name to create a new item",
        # "icon": {"path": f"icons/{theme}/help.png"},
        "icon": {"path": f"icons/{theme}/icon.png"},
        "valid": False
    })

print(json.dumps({"items": items}))
