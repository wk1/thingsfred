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

    batch_mode = os.environ.get("batch_mode", "false") == "true"
    
    if batch_mode:
        # Write container info to a file for the batch script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        batch_file = os.path.join(os.path.dirname(script_dir), ".batch_info")
        
        with open(batch_file, 'w') as f:
            f.write(f"{container_type.value}\n")
            f.write(f"{container_id}\n") 
            f.write(f"{container_title}\n")
            f.write(f"{item_type.value if isinstance(item_type, ItemType) else item_type}\n")
        
        # Trigger the batch mode through workflow variables instead
        result = {
            "alfredworkflow": {
                "variables": {
                    "success_title": success_title + " - Batch Mode", 
                    "success_subtitle": "Continue adding items",
                    "trigger_batch": "true"
                }
            }
        }
    else:
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