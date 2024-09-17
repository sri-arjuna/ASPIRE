print("\nCall from Aspire project root - where the LICENSE.txt is\nLike: --> py docs/tools/get_todo.py\n")
#
#	Imports
#
import os, sys
import glob
import json

#
#	Variables
#
dir_work = "." # "..AspireTUI"
output_file = "docs/TODO-Found.md"
output_data = {}
file_list = glob.glob(f'**/*.py', recursive=True)

#
#	Start parsing
#
for file_name in file_list:
	#print("checking:", file_name)
	if file_name.endswith("pyc"):
		continue
	elif file_name.endswith("py"):
		# proper extension, lets parse
		#print("found:", file_name)
		with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
			lines = file.readlines()
			for line_number, line in enumerate(lines, start=1):
				if 'TODO: ' in line:
					output_data[file_name] = line
#
#	Write output
#
# Write TODO messages to a markdown file
with open(output_file, 'w', encoding='utf-8') as fn:
	fn.write(f"| File | Desc |\n|---|---|\n")
	for file, line in output_data.items():
		fn.write(f"| {file.strip()} | {line.strip()} |\n")
	print("TODO messages written to:", output_file)
