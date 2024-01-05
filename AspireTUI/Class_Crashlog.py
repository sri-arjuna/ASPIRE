"""
	Description:
					Split up Crashlogs into different sections.
	Provides:
					from AspireTUI.Class_Crashlog import CrashLog as _CrashLog
					
					
	========================================================
	Created on:		2024 Jan. 04
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Essential imports
#
#import os as _os
#import sys as _sys
#import re as _re
#import string as _string
#from pathlib import Path as _Path
#from . import IS_WINDOWS
#################################################################################################################
#####                                           Crashlog Class Container                                    #####
#################################################################################################################
#
#	Sub-Sections
#
class Section:
	def __init__(self, name, lines):
		self.name = name
		self.lines = lines

class SectionSystemSpec:
	def __init__(self):
		self.GPU = []
		self.GPU_MEM = ""
		self.CPU = []
		self.MEM = ""
		self.OS = ""
		self.Pagefile = ""
		self.PagefileSize = ""

class SectionHeading:
	def __init__(self):
		self.Chrashlog_Name = ""
		self.Chrashlog_Version = ""
		self.App_Name = ""
		self.App_Version = ""
		self.Unhandled_Type = ""
		self.Unhandled_Memory = ""
		self.Unhandled_File = ""
		self.Unhandled_Assembler = ""
		self.Unhandled_Extra = ""

#
#	Root Section
#
class CrashLog:
	def __init__(self, filename, DEBUG=True):
		self.filename = filename
		self.Heading = SectionHeading()
		self.Stack_Call = []
		self.Call = []
		self.Plugins = []
		self.Plugins_XSE = []
		self.Registers = []
		self.Modules = []
		self.SystemSpec = SectionSystemSpec()

		tmp = self._parse_crashlog(filename)
		if DEBUG:
			for section in tmp["sections"]:
				print("Section:\t", section)


	def _parse_crashlog(filename):
		with open(filename, 'r', encoding='utf-8') as file:
			content = file.readlines()

		# Find the start of the sections using a regular expression
		#section_start = next((i for i, line in enumerate(content) if re.match(r"[A-Z]*:|\{", line)), None)
		section_start = next((i for i, line in enumerate(content) if re.match(r"[A-Z]*:|\{\n", line)), None)

		# Parse heading
		heading = content[:section_start]
		heading = [line.rstrip('\n') for line in heading if line.strip()]

		# Parse sections
		sections = []
		current_section = None
		for line in content[section_start:]:
			if re.match(r"[A-Z]*:|\{", line):
				if current_section:
					sections.append(current_section)
				current_section = Section(line.rstrip('\n'), [])
			elif current_section:
				current_section.lines.append(line.rstrip('\n'))

		# Add the last section
		if current_section:
			sections.append(current_section)

		# Create a data container
		data_container = {'heading': heading}
		for section in sections:
			section_name = section.name.replace(' ', '')
			data_container[section_name] = section.lines

		# Add a method to retrieve a list of sections
		data_container['sections'] = [section.name for section in sections]

		return data_container
