import os
import glob

def get_things_db_pattern():
  """
  Returns the glob pattern to locate the Things 3 database.
  Uses workflow environment variable 'THINGS_DB_PATH_PATTERN' if available,
  otherwise falls back to default.
  """
  return os.getenv(
    "THINGS_DB_PATH_PATTERN",
    "~/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-*/Things Database.thingsdatabase/main.sqlite"
  )

def find_things_db():
  """
  Returns the path to the most recent Things 3 database file.
  Returns None if no match is found.
  """
  pattern = os.path.expanduser(get_things_db_pattern())
  db_paths = glob.glob(pattern)
  if not db_paths:
    return None
  return max(db_paths, key=os.path.getmtime)