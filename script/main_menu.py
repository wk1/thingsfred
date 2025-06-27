#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import subprocess
import os
from helpers.theming import get_icon_theme
from helpers.models import ItemType, ContainerType, ActionType
from helpers.input import processInput


def main():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  update_script = os.path.join(script_dir, "helpers/theming.py")
  subprocess.run([sys.executable, update_script], capture_output=True)

  theme = get_icon_theme()
  input_text, notes = processInput()

  items = []

  # if input_text:
  items.append({
    "title": f"Inbox",
    "subtitle": f"Create Task \"{input_text}\" in Inbox",
    "arg": input_text,
    "variables": {
      "input_text": input_text,
      "notes": notes,
      "action": ActionType.ADD.value,
      "item_type": ItemType.TASK.value,
      "container_type": ContainerType.INBOX.value,
      "container_title": "📥 Inbox",
    },
    "icon": {"path": f"icons/{theme}/inbox.png"},
    "valid": bool(input_text),
    "mods": {
      "cmd": {
        "variables": {
          "input_text": input_text,
          "notes": notes,
          "action": ActionType.ADD.value,
          "item_type": ItemType.TASK.value,
          "container_type": ContainerType.INBOX.value,
          "container_title": "📥 Inbox",
          "batch": 1
        },
        "subtitle": f"Batch create Task \"{input_text}\" in Inbox"
      }
    }
  })

  items.append({
    "title": f"Today",
    "subtitle": f"Create Task \"{input_text}\" in Today",
    "arg": input_text,
    "variables": {
      "input_text": input_text,
      "notes": notes,
      "action": ActionType.ADD.value,
      "item_type": ItemType.TASK.value,
      "container_type": ContainerType.TODAY.value,
      "container_title": "📆 Today",
    },
    "icon": {"path": f"icons/{theme}/today.png"},
    "valid": bool(input_text),
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
          "container_title": "📆 Today",
        },
        "subtitle": f"Create Project \"{input_text}\" for Today"
      },
      "cmd": {
        "valid": bool(input_text),
        "arg": input_text,
        "variables": {
          "input_text": input_text,
          "notes": notes,
          "action": ActionType.ADD.value,
          "item_type": ItemType.TASK.value,
          "container_type": ContainerType.TODAY.value,
          "container_title": "📆 Today",
          "batch": 1
        },
        "subtitle": f"Batch create Task \"{input_text}\" for Today"
      }
    }
  })

  items.append({
    "title": f"→ Browse...",
    "subtitle": "Browse Areas / Projects to create Task",
    "arg": input_text,
    "variables": {
      "input_text": input_text,
      "notes": notes,
      "action": ActionType.BROWSE.value,
    },
    "icon": {"path": f"icons/{theme}/list.png"},
    "valid": True
  })
# else:
  items.append({
    "title": "Thingsfred",
    "subtitle": "Type ++name to create a new item",
    "icon": {"path": f"icons/{theme}/icon.png"},
    "valid": False
  })

  print(json.dumps({"items": items}, ensure_ascii=False))


if __name__ == "__main__":
  main()