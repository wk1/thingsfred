#!/usr/bin/env python3
import json
import sys
import os
from helpers.theming import get_icon_theme
from helpers.models import ItemType, ContainerType, ActionType

theme = get_icon_theme()
query = sys.argv[1] if len(sys.argv) > 1 else ""

container_type = ContainerType(os.environ.get("container_type", "inbox"))
container_id = os.environ.get("container_id", "")  
container_title = os.environ.get("container_title", "")
item_type = ItemType(os.environ.get("item_type", "task"))

items = []

if query:
    # User has typed something, show the add option for the remembered container
    if container_type == ContainerType.INBOX:
        location_title = "Inbox"
        location_icon = "inbox.png"
    elif container_type == ContainerType.TODAY:
        location_title = "Today"
        location_icon = "today.png"
    elif container_type == ContainerType.AREA:
        location_title = f"Area: {container_title}"
        location_icon = "area.png"
    else:
        location_title = f"Project: {container_title}"
        location_icon = "project.png"
    
    items.append({
        "title": f"{location_title}",
        "subtitle": f"Create \"{query}\" in {location_title}",
        "arg": query,
        "autocomplete": query,
        "variables": {
            "input_text": query,
            "notes": "",
            "action": ActionType.ADD.value,
            "item_type": item_type.value,
            "container_type": container_type.value,
            "container_id": container_id,
            "container_title": container_title,
        },
        "icon": {"path": f"icons/{theme}/{location_icon}"},
        "valid": True,
        "mods": {
            "cmd": {
                "valid": True,
                "arg": query,
                "autocomplete": query,
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
                "subtitle": f"Create \"{query}\" in {location_title} (⌘ to add more)"
            }
        }
    })
else:
    # Show prompt
    if container_type == ContainerType.INBOX:
        location_title = "Inbox"
        location_icon = "inbox.png"
    elif container_type == ContainerType.TODAY:
        location_title = "Today"
        location_icon = "today.png"
    elif container_type == ContainerType.AREA:
        location_title = f"Area: {container_title}"
        location_icon = "area.png"
    else:
        location_title = f"Project: {container_title}"
        location_icon = "project.png"
        
    items.append({
        "title": f"Add another {item_type.value} to {location_title}",
        "subtitle": "Type the name for your next item",
        "arg": "",
        "icon": {"path": f"icons/{theme}/{location_icon}"},
        "valid": False
    })

print(json.dumps({"items": items}))