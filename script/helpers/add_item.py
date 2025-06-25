#!/usr/bin/env python3
import json
import sys
import os
import subprocess
import urllib.parse
from models import ContainerType, ItemType, ActionType

def create_things_url(item_type, container_type, container_id, title, notes, when=None):
    
    # Base Parameter
    params = {"title": title}

    if notes:
        params["notes"] = notes
    
    # Command
    if item_type == ItemType.PROJECT:
        command = "add-project"
    else:
        command = "add"
    
    # List-Parameter setzen
    if container_type == ContainerType.AREA and item_type == ItemType.PROJECT:
        # Projekt in Area
        params["area-id"] = container_id
    elif container_type == ContainerType.PROJECT:
        # Task in Projekt
        params["list-id"] = container_id
    elif container_type == ContainerType.AREA:
        # Task in Area
        params["list-id"] = container_id
    # INBOX und TODAY brauchen keine list-id
    
    # Spezielle Parameter
    if container_type == ContainerType.TODAY or when == "today":
        params["when"] = "today"
    
    # URL bauen
    url_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"things:///{command}?{url_params}"

def main():

    input_text = os.environ.get("input_text", "")
    notes = os.environ.get("notes", "")
    action = ActionType(os.environ.get("action", "add"))
    item_type = ItemType(os.environ.get("item_type", "task"))
    container_type = ContainerType(os.environ.get("container_type", "inbox"))
    container_id = os.environ.get("container_id", "")
    container_title = os.environ.get("container_title", "")
    
    # Validation
    if action == ActionType.ADD:
        if container_type == ContainerType.INBOX and item_type == ItemType.PROJECT:
            print("Projects cannot be created in the Inbox")
            sys.exit(1)
    
        if container_type == ContainerType.PROJECT and item_type == ItemType.PROJECT:
            print("Projects cannot be created in Projects")
            sys.exit(1)
    else:
        print("Unsupported action type")
        sys.exit(1)
    
    # Create URL
    url = create_things_url(
        item_type=item_type,
        container_type=container_type,
        container_id=container_id,
        title=input_text,
        notes=notes,
        when="today" if container_type == ContainerType.TODAY else None
    )
    
    # Run Things URL
    subprocess.run(["open", url])
    
    # # Feedback
    item_type = "Project" if item_type == ItemType.PROJECT else "Task"

    # Add A Switch for Success Message
    if container_type == ContainerType.INBOX:
        success_title = f"Added to Inbox 📥"
        success_subtitle = f"\"{input_text}\" has been added to your Inbox."
    elif container_type == ContainerType.TODAY:
        success_title = f"Added to Today 📅"
        success_subtitle = f"{item_type} \"{input_text}\" has been added to your Today list."
    elif container_type == ContainerType.AREA:
        success_title = f"Added to Area 📦"
        success_subtitle = f"{item_type} \"{input_text}\" added to {container_title}."
    else:
        success_title = f"Added to Project 📂"
        success_subtitle = f"{item_type} \"{input_text}\" added to {container_title}."

    result = {
        "alfredworkflow": {
            "variables": {
                "success_title": success_title,
                "success_subtitle": success_subtitle
            }
        }
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()