import sys
import os

def processInput():
  query = sys.argv[1] if len(sys.argv) > 1 else ""
  separator = os.environ.get("NOTES_SEPARATOR", "///")

  if separator in query:
      parts = query.split(separator, 1)
      input_text = parts[0].strip()
      notes = parts[1].strip()
  else:
      input_text = query.strip()
      notes = ""

  return input_text, notes