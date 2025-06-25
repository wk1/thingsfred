#!/usr/bin/env python3
import json
import sys

data = json.loads(sys.argv[1])
input_text = data["input_text"]

sys.stdout.write(input_text)