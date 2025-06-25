import json
from typing import Optional
from helpers.models import ActionType, ContainerType, ItemType

def alfred_error(title: str, subtitle: Optional[str] = None):
  return {
    "items": [{
      "title": title,
      "subtitle": subtitle or "",
      "valid": False
    }]
  }

def alfred_back_button(input_text: str, theme: str, subtitle: Optional[str] = None):
  item = {
    "title": "Back",
    "arg": input_text,
    "variables": {
      "action": ActionType.BACK.value,
    },
    "icon": {"path": f"icons/{theme}/back.png"},
    "valid": True
  }

  if subtitle:
    item["subtitle"] = subtitle

  return item

def alfred_area_item(area_title: str, area_id: str, input_text: str, notes: str, theme: str):
  return {
    "title": area_title,
    "subtitle": "→ Show area content",
    "arg": "",
    "variables": {
      "input_text": input_text,
      "notes": notes,
      "action": ActionType.SHOW_CONTENT.value,
      "item_type": ItemType.TASK.value,
      "container_type": ContainerType.AREA.value,
      "container_id": area_id,
      "container_title": area_title,
    },
    "icon": {"path": f"icons/{theme}/area.png"},
    "valid": True
  }

def alfred_project_item(title: str, id: str, input_text: str, theme: str):
  return {
    "title": title,
    "subtitle": "Add task to project",
    "arg": json.dumps({
      "input_text": input_text,
      "action": ActionType.ADD.value,
      "container_type": ContainerType.PROJECT.value,
      "container_id": id,
      "container_title": title,
    }),
    "icon": {"path": f"icons/{theme}/project.png"},
    "valid": True
  }

def alfred_add_item(title: str, notes: str, container_type: ContainerType, container_title: str, container_id: str, theme: str):
  # add a function that returns a dictionary for adding an item

  def variables(type: ItemType):
    return {
      "input_text": title,
      "notes": notes,
      "action": ActionType.ADD.value,
      "item_type": type.value,
      "container_type": ContainerType.AREA.value,
      "container_id": container_id,
      "container_title": container_title,
    }
  
  def mods(type: ContainerType):
    return {
      "option": {
        "arg": "",
        "variables": variables(ItemType.PROJECT),
        "subtitle": f"Add project '{title}' to {container_type.value} {container_title}",
        "icon": {"path": f"icons/{theme}/project_add.png"},
        "valid": True
      }
    } if type == ContainerType.AREA or type == ContainerType.TODAY else {}


  return {
      "title": f"{container_title}",
      "subtitle": f"Add task '{title}' to {container_type.value} {container_title}",
      "arg": "",
      "variables": variables(ItemType.TASK),
      "icon": {"path": f"icons/{theme}/task_add.png"} if container_type == ContainerType.AREA else {"path": f"icons/{theme}/project.png"},
      "valid": True,
      "mods": mods(container_type)
  }