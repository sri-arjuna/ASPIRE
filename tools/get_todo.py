import os

def find_todos(directory):
	"""
	Recursively search for "TODO: " in all files within the given directory.
	Create a markdown file ("TODO-Found.md") with the formatted output.
	"""
	todo_messages = {}

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
			if file_name.endswith(".py"):  # Change the extension as needed
				file_path = os.path.join(root, file_name)
				process_file(file_path)

	# Write TODO messages to a markdown file
	with open("TODO-Found.md", 'w', encoding='utf-8') as output_file:
		for file_path, messages in todo_messages.items():
			output_file.write(f"# {file_path}\n")
			for message in messages:
				output_file.write(message + '\n')
		print("TODO messages written to TODO-Found.md")

# RUN
find_todos("../AspireTUI")
