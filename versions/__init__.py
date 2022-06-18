#!/usr/bin/python3
import json

HANDLERS = []

def register(func):
	HANDLERS.append(func)

# Load all handlers
from versions.services import *

def update():
	metadata = []
	for handler in HANDLERS:
		meta = handler()
		metadata.append(meta)
	return json.dumps(metadata)
