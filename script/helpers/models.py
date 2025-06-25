from enum import Enum

class ContainerType(Enum):
    INBOX = "inbox"
    TODAY = "today"
    AREA = "area"
    PROJECT = "project"

class ItemType(Enum):
    TASK = "task"
    PROJECT = "project"

class ActionType(Enum):
    ADD = "add"
    BACK = "back"
    BROWSE = "browse"
    HELP = "help"
    SHOW_CONTENT = "show_content"

class Queries:
  AREAS = """
    SELECT uuid, title 
    FROM TMArea
    ORDER BY "index"
  """

  PROJECTS = """
    SELECT uuid, title
    FROM TMTask
    WHERE type = 1 -- type = 1 is a project
      AND status = 0  -- Only active projects
      AND area IS NULL -- Only root projects (no area)
    ORDER BY "index"
  """

  PROJECTS_IN_AREA = """
    SELECT uuid, title
    FROM TMTask
    WHERE type = 1 
    AND trashed = 0 
    AND status = 0
    AND area = ?
    ORDER BY "index"
  """