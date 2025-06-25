#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import os

# Am Anfang
from helpers.theming import get_icon_theme
from helpers.models import Queries, ContainerType
from helpers.things_db import find_things_db
from helpers.alfred import (
  alfred_error,
  alfred_back_button,
  alfred_area_item,
  alfred_add_item
)

def main():
    theme = get_icon_theme()
    db_path = find_things_db()
    
    input_text = os.environ.get("input_text", "")
    notes = os.environ.get("notes", "")
    
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
            alfred_back_button(input_text, theme, "Back to Menu")
        )

        cursor.execute(Queries.AREAS)
        for area_id, area_title in cursor.fetchall():
            items.append(
                alfred_area_item(area_title, area_id, input_text, notes, theme)
            )

        cursor.execute(Queries.PROJECTS)
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
        print(
            alfred_error(
                "Error reading database",
                str(e)
            )
        )

if __name__ == "__main__":
    main()