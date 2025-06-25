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
separator = os.environ.get("NOTES_SEPARATOR", "///")

batch_context = os.environ.get("batch_context", "false") == "true"

# Try to load batch context from file if not in environment
if not batch_context:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    batch_file = os.path.join(script_dir, ".batch_context.json")
    
    if os.path.exists(batch_file):
        try:
            with open(batch_file, 'r') as f:
                batch_data = json.load(f)
                batch_context = True
                batch_container_type = ContainerType(batch_data.get("container_type", "inbox"))
                batch_container_id = batch_data.get("container_id", "")
                batch_container_title = batch_data.get("container_title", "")
                batch_item_type = ItemType(batch_data.get("item_type", "task"))
            # Remove the file after reading
            os.remove(batch_file)
        except:
            batch_context = False

if batch_context and 'batch_container_type' not in locals():
    batch_container_type = ContainerType(os.environ.get("container_type", "inbox"))
    batch_container_id = os.environ.get("container_id", "")
    batch_container_title = os.environ.get("container_title", "")
    batch_item_type = ItemType(os.environ.get("item_type", "task"))

if separator in query:
    parts = query.split(separator, 1)
    input_text = parts[0].strip()
    notes = parts[1].strip()
else:
    input_text = query.strip()
    notes = ""


items = []

if input_text:
    if batch_context:
        # In batch mode, show direct option for the same location
        if batch_container_type == ContainerType.INBOX:
            location_title = "Inbox"
            location_icon = "inbox.png"
        elif batch_container_type == ContainerType.TODAY:
            location_title = "Today"
            location_icon = "today.png"
        elif batch_container_type == ContainerType.AREA:
            location_title = f"Area: {batch_container_title}"
            location_icon = "area.png"
        else:
            location_title = f"Project: {batch_container_title}"
            location_icon = "project.png"
            
        items.append({
            "title": f"{location_title}",
            "subtitle": f"Create \"{input_text}\" in {location_title}",
            "arg": input_text,
            "variables": {
                "input_text": input_text,
                "notes": notes,
                "action": ActionType.ADD.value,
                "item_type": batch_item_type.value,
                "container_type": batch_container_type.value,
                "container_id": batch_container_id,
                "container_title": batch_container_title,
            },
            "icon": {"path": f"icons/{theme}/{location_icon}"},
            "valid": True,
            "mods": {
                "cmd": {
                    "valid": True,
                    "arg": input_text,
                    "variables": {
                        "input_text": input_text,
                        "notes": notes,
                        "action": ActionType.ADD.value,
                        "item_type": batch_item_type.value,
                        "container_type": batch_container_type.value,
                        "container_id": batch_container_id,
                        "container_title": batch_container_title,
                        "batch_mode": "true"
                    },
                    "subtitle": f"Create \"{input_text}\" in {location_title} (⌘ to add more)"
                }
            }
        })
    else:
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
            "valid": True,
            "mods": {
                "cmd": {
                    "valid": True,
                    "arg": input_text,
                    "variables": {
                        "input_text": input_text,
                        "notes": notes,
                        "action": ActionType.ADD.value,
                        "item_type": ItemType.TASK.value,
                        "container_type": ContainerType.INBOX.value,
                        "batch_mode": "true"
                    },
                    "subtitle": f"Create \"{input_text}\" in Inbox (⌘ to add more)"
                }
            }
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
                },
                "cmd": {
                    "valid": True,
                    "arg": input_text,
                    "variables": {
                        "input_text": input_text,
                        "notes": notes,
                        "action": ActionType.ADD.value,
                        "item_type": ItemType.TASK.value,
                        "container_type": ContainerType.TODAY.value,
                        "batch_mode": "true"
                    },
                    "subtitle": f"Create \"{input_text}\" in Today (⌘ to add more)"
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
