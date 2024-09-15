"""
	Description:\n
					Handles themes, data and references.

	Provides:\n
					style = _settings["theme-data"] ; print(theme.border_left)	\n
					list = themes.list()	\n
					themes.set(NAME)		\n
					
	========================================================

	Created on:		2023 Nov. 09

	Created by:		Simon Arjuna Erat

	License:		MIT

	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Imports
#
import requests
import re

#
#	Verify proper import
#
try:
	from bs4 import BeautifulSoup

except:
	print("You are missing BeautifulSoup")
	print("pip install beautifulsoup4 /OR/ python -m pip install beautifulsoup4")

	
#
#	Check for Update functions
#

def update_from_github(current_version: str, URL: str):
	"""
Checks for a higher version than "current_version" on "URL"

URL must be a valid GitHub address (not gist), leading to the tag page.

--> https://github.com/<user>/<project>/tags <--
	"""


	# Check valid URL
	try:
		# Validate and parse the URL
		match = re.match(r'https://github\.com/([^/]+)/([^/]+)/tags', URL)
		if not match:
			print("Invalid GitHub tags URL format.")
			return
		
		user, project = match.groups()

		# Fetch the content of the page
		response = requests.get(URL)
		response.raise_for_status()  # Raise an exception for HTTP errors

		# Parse the HTML with BeautifulSoup
		soup = BeautifulSoup(response.text, 'html.parser')

		# Generate the regex pattern using the parsed user and project
		pattern = rf'/ {user} / {project} /releases/tag/v\d+(\.\d+)*(-\w+)?'

		# Find all version tags using the dynamically generated pattern
		version_links = soup.find_all('a', href=re.compile(pattern))

		# Extract version numbers
		versions = [link['href'].split('/')[-1][1:] for link in version_links]

		# Sort the versions to find the latest one
		versions.sort(key=lambda s: [int(u) if u.isdigit() else u for u in re.split(r'(\d+)', s)])

		# Get the latest version from sorted versions
		latest_version = versions[-1] if versions else None

		# Compare with the current version
		if latest_version and latest_version > current_version:
			print(f"An update is available: {latest_version}. Your current version: {current_version}.")
		else:
			print("You are using the latest version.")

	except requests.RequestException as e:
		print(f"Error checking for updates: {e}")
