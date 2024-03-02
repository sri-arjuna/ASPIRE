import os, sys
file_output = "TODO-Found.md"

import glob
search_list =  ["OS.py", "Demo.py"] # ["File_1.py", "File_2.py", "File_3.py"]
file_list = glob.glob(f'**/*.py', recursive=True)

for item in file_list:
	for search in search_list:
		if search in item:
			print("Found: ", item)
sys.exit()


import json

def find_todos(directory: str):
	"""
	Recursively search for "TODO: " in all files within the given directory.
	Create a markdown file ("TODO-Found.md") with the formatted output.
	"""
	todo_messages = {}
	prefix = "./" + directory.replace("../", "") + " -/- "

	def process_file(file_path):
		nonlocal todo_messages
		file_messages = []
		with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
			lines = file.readlines()
			for line_number, line in enumerate(lines, start=1):
				if 'TODO: ' in line:
					file_messages.append(f"- {line_number}: {line.strip()}")
		if file_messages:
			todo_messages[file_path] = file_messages

	for root, dirs, files in os.walk(directory):
		for file_name in files:
			if not file_name.startswith("_") and file_name.endswith(".py"):
				file_path = os.path.join(root, file_name)
				process_file(file_path)

	# Write TODO messages to a markdown file
	with open(file_output, 'w', encoding='utf-8') as output_file:
		for file_path, messages in todo_messages.items():
			output_file.write(f"\n# {prefix}{file_name}\n")
			for message in messages:
				output_file.write(message + '\n')
		print("TODO messages written to TODO-Found.md")

# RUN
find_todos("../AspireTUI")
