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
import re as _re
#import string as _string
#from pathlib import Path as _Path
#
#	Internals
# 
#from . import IS_WINDOWS
from . import tui as _tui
from . import StringUtils as _stew

#################################################################################################################
#####                                           Crashlog Class Container                                    #####
#################################################################################################################
#
#	Sub-Sections
#
class Section:
	"""
	In case of need, provides the literal string of the section _name_ within the crashlog.		\n
	And of course, all the _lines_ of this section.		\n
	\n
	Each sub section of the crashlog has a "lines" list of all lines of that section that could not be assigned a predefined class attribute.
	"""
	def __init__(self, name, lines):
		self.name = name
		self.lines = lines

class SectionSystemSpec:
	"""
	Predefined system specs.
	"""
	def __init__(self):
		self.GPU = []
		self.GPU_MEM = ""
		self.CPU = []
		self.MEM = ""
		self.OS = ""
		self.Pagefile = ""
		self.PagefileSize = ""
		self.lines = []

class SectionUnhandled:
	"""
	The "Unhandled" line split up.
	"""
	def __init__(self):
		self.Type = ""
		self.Memory = ""
		self.Unhandled_File = ""
		self.Assembler = ""
		self.Extra = ""
		self.lines = []

class SectionHeading:
	"""
	Data that should be in headings.
	"""
	def __init__(self):
		self.Chrashlogger_Name = ""
		self.Chrashlogger_Version = ""
		self.App_Name = ""
		self.App_Version = ""
		self.Unhandled = SectionUnhandled()
		self.lines = []

#
#	Root Section
#
class CrashLog:
	def __init__(self, filename, bVerbose=True, bLOG=True, sLOG_File=f"{_stew.logtime()}.log"):
		self.filename = filename
		self.Heading = SectionHeading()
		self.Stack_Call = Section()
		self.Call = Section()
		self.Plugins = Section()
		#self.Plugins_XSE = Section()
		self.Registers = Section()
		self.Modules = Section()
		self.SystemSpec = SectionSystemSpec()

		# Prepare additional tasks
		if bLOG:
			from . import FileUtils as _FileUtils
			log = _FileUtils.log(sLOG_File)
			log.Settings.bVerbose = bVerbose

		# Get the raw data
		tmp = self._crashlog_parse(filename)
		if bVerbose:
			for section in tmp["sections"]:
				print("Section:\t", section)
		
		# Make it accessable
		self._crashlog_sort(tmp)
	
	# Prepare raw data
	def _crashlog_parse(filename) -> dict:
		"""
		Parses _filename_ and prepares data for basic structure into a dict for easier sorting.
		"""
		with open(filename, 'r', encoding='utf-8') as file:
			content = file.readlines()

		# Find the start of the sections
		#section_start = next((i for i, line in enumerate(content) if re.match(r"[A-Z]*:|\{", line)), None)
		section_start = next((i for i, line in enumerate(content) if _re.match(r"[A-Z]*:|\{\n", line)), None)

		# Parse heading
		heading = content[:section_start]
		heading = [line.rstrip('\n') for line in heading if line.strip()]

		# Parse sections
		sections = []
		current_section = None
		for line in content[section_start:]:
			if _re.match(r"[A-Z]*:|\{", line):
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
	
	# Set attributes to values
	def _crashlog_sort(self, this: dict):
		"""
		Decide which sections shall be used for the predefined ones.
		"""
		# Parse predefined list to retrive possible candidates
		pre_list = [ "register", "stack call", "call", "plugins", "module", "system",  ]
		for item in pre_list:
			# Init variables, per round
			worklist_raw = []
			# Get all options
			for section in this["sections"]:
				if item in section:
					worklist_raw.append(section)
			# Check if multiple options were detcted
			if item = pre_list[0]:
				# Register
				if len(worklist_raw) == 1:
					self.Registers.name = worklist_raw[0]
					self.Registers.lines = this[self.Registers.name]
				else:
					pass

"""
PLUGINS:
SKSE PLUGINS:
MODULES:
STACK:
REGISTERS:
PROBABLE CALL STACK:
SYSTEM SPECS:
"""
