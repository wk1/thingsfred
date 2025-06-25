#!/usr/bin/env python3
import json
import sys
import os
from helpers.theming import get_icon_theme
from helpers.models import ItemType, ContainerType, ActionType

theme = get_icon_theme()
query = sys.argv[1] if len(sys.argv) > 1 else ""

# Get container context from file or environment
script_dir = os.path.dirname(os.path.abspath(__file__))
batch_file = os.path.join(script_dir, ".batch_info")

if os.path.exists(batch_file):
    try:
        with open(batch_file, 'r') as f:
            lines = f.read().strip().split('\n')
            container_type = ContainerType(lines[0])
            container_id = lines[1] if len(lines) > 1 else ""
            container_title = lines[2] if len(lines) > 2 else ""
            item_type = ItemType(lines[3] if len(lines) > 3 else "task")
        # Remove the file after reading
        os.remove(batch_file)
    except:
        # Fallback to environment variables
        container_type = ContainerType(os.environ.get("container_type", "inbox"))
        container_id = os.environ.get("container_id", "")
        container_title = os.environ.get("container_title", "")
        item_type = ItemType(os.environ.get("item_type", "task"))
else:
    # Fallback to environment variables
    container_type = ContainerType(os.environ.get("container_type", "inbox"))
    container_id = os.environ.get("container_id", "")
    container_title = os.environ.get("container_title", "")
    item_type = ItemType(os.environ.get("item_type", "task"))

items = []

if query:
    # User typed something - show the add option
    if container_type == ContainerType.INBOX:
        location_title = "Inbox"
        icon_name = "inbox.png"
    elif container_type == ContainerType.TODAY:
        location_title = "Today"
        icon_name = "today.png"
    elif container_type == ContainerType.AREA:
        location_title = f"Area: {container_title}"
        icon_name = "area.png"
    elif container_type == ContainerType.PROJECT:
        location_title = f"Project: {container_title}"
        icon_name = "project.png"
    else:
        location_title = container_title
        icon_name = "task_add.png"

    items.append({
        "title": f"Add \"{query}\" to {location_title}",
        "subtitle": f"Press Enter to add, ⌘+Enter to add more",
        "arg": query,
        "variables": {
            "input_text": query,
            "notes": "",
            "action": ActionType.ADD.value,
            "item_type": item_type.value,
            "container_type": container_type.value,
            "container_id": container_id,
            "container_title": container_title,
        },
        "icon": {"path": f"icons/{theme}/{icon_name}"},
        "valid": True,
        "mods": {
            "cmd": {
                "valid": True,
                "arg": query,
                "variables": {
                    "input_text": query,
                    "notes": "",
                    "action": ActionType.ADD.value,
                    "item_type": item_type.value,
                    "container_type": container_type.value,
                    "container_id": container_id,
                    "container_title": container_title,
                    "batch_mode": "true"
                },
                "subtitle": f"Add \"{query}\" to {location_title} and continue adding"
            }
        }
    })
else:
    # Show prompt
    if container_type == ContainerType.INBOX:
        location_title = "Inbox"
        icon_name = "inbox.png"
    elif container_type == ContainerType.TODAY:
        location_title = "Today"  
        icon_name = "today.png"
    elif container_type == ContainerType.AREA:
        location_title = f"Area: {container_title}"
        icon_name = "area.png"
    elif container_type == ContainerType.PROJECT:
        location_title = f"Project: {container_title}"
        icon_name = "project.png"
    else:
        location_title = container_title
        icon_name = "task_add.png"

    items.append({
        "title": f"Add another item to {location_title}",
        "subtitle": "Type the name of the item you want to add",
        "icon": {"path": f"icons/{theme}/{icon_name}"},
        "valid": False
    })

print(json.dumps({"items": items}))