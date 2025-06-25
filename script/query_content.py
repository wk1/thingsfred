#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import os
from helpers.things_db import find_things_db
from helpers.theming import get_icon_theme
from helpers.models import ContainerType, ActionType, Queries
from helpers.alfred import (
    alfred_error,
    alfred_back_button,
    alfred_area_item,
    alfred_project_item,
    alfred_add_item
)

# Icon Theme bestimmen
theme = get_icon_theme()

def main():
    
    action = os.environ.get("action")
    input_text = os.environ.get("input_text", "")
    notes = os.environ.get("notes", "")
    container_type = os.environ.get("container_type", "")
    container_id = os.environ.get("container_id", "")
    container_title = os.environ.get("container_title", "")

    db_path = find_things_db()
    if not db_path:
        print(
            alfred_error(
                "Things 3 Database not found",
                "Please make sure Things 3 is installed"
            )
        )
        return
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        items = []
        
        items.append(
            alfred_back_button(
                input_text=input_text,
                theme=theme,
                subtitle="Back to Menu"
            )
        )
        
        items.append(
            alfred_add_item(
                title=input_text,
                notes=notes,
                container_type=ContainerType.AREA,
                container_title=container_title,
                container_id=container_id,
                theme=theme
            )
        )
        
        # Projekte der Area
        cursor.execute(Queries.PROJECTS_IN_AREA, (container_id,))
        
        for project_id, project_title in cursor.fetchall():
            items.append(
                alfred_add_item(
                    title=input_text,
                    notes=notes,
                    container_type=ContainerType.PROJECT,
                    container_title=project_title,
                    container_id=project_id,
                    theme=theme
                )
            )
        
        conn.close()
        print(json.dumps({"items": items}))
        
    except Exception as e:
        print(json.dumps({
            "items": [{
                "title": "Error reading database",
                "subtitle": str(e),
                "valid": False
            }]
        }))

if __name__ == "__main__":
    main()