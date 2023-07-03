"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


import os
import platform
import re
import subprocess
import sys


class Environment:
	class var:
		@staticmethod
		def get(name):
			# Get the value of an environment variable
			return os.getenv(name)

		@staticmethod
		def set(name, value):
			# Set the value of an environment variable
			os.environ[name] = value

		@staticmethod
		def remove(name):
			# Remove an environment variable
			os.environ.pop(name, None)

		@staticmethod
		def list():
			# List all environment variables
			return list(os.environ.keys())

		# Get the value of an environment variable with default value
		@staticmethod
		def get_with_default(name, default_value):
			return os.getenv(name, default_value)

	class sys:
		@staticmethod
		def info():
			# Get the system information
			return platform.uname()

		@staticmethod
		def distribution():
			# Get the distribution information
			if platform.system() == "Windows":
				return platform.platform()
			elif platform.system() == "Darwin":
				mac_ver = platform.mac_ver()
				return f"macOS {mac_ver[0]} ({mac_ver[2]})"
			else:
				distro = platform.dist()
				return f"{distro[0]} {distro[1]} ({distro[2]})"

	class dir:
		@staticmethod
		def current():
			# Get the current working directory
			return os.getcwd()

		@staticmethod
		def home():
			# Get the user home directory
			return os.path.expanduser("~")

		@staticmethod
		def size(self, path):
			# Get the size of a file or directory
			if self.is_directory(path):
				return sum(
					os.path.getsize(os.path.join(dirpath, filename))
					for dirpath, dirnames, filenames in os.walk(path)
					for filename in filenames
				)
			elif self.is_file(path):
				return os.path.getsize(path)
			else:
				return 0

		@staticmethod
		def change(path):
			# Change the current working directory
			os.chdir(path)

		@staticmethod
		def temp():
			# Get the user's temporary directory
			return os.path.gettempdir()

		@staticmethod
		def exists(path):
			# Check if a file or directory exists
			return os.path.exists(path)

		@staticmethod
		def is_file(path):
			# Check if a path is a file
			return os.path.isfile(path)

		@staticmethod
		def is_directory(path):
			# Check if a path is a directory
			return os.path.isdir(path)

		@staticmethod
		def PATH():
			# Get the system path
			return os.getenv("PATH")

	class user:
		@staticmethod
		def is_admin():
			# Check if the script is running as root
			return os.geteuid() == 0

		@staticmethod
		def name():
			# Get the current username
			return os.getlogin()

		@staticmethod
		def get_uid():
			# Get the current user's UID
			return os.getuid()

		@staticmethod
		def get_gid():
			# Get the current user's GID
			return os.getgid()

		@staticmethod
		def get_groups():
			# Get the current user's groups
			return os.getgroups()

	@staticmethod
	def command_exists(cmd):
		# Check if a command exists
		return any(
			os.access(os.path.join(path, cmd), os.X_OK)
			for path in os.environ["PATH"].split(os.pathsep)
		)

	@staticmethod
	def is_package_installed(package):
		# Check if a package is installed
		if platform.system() == "Windows":
			cmd = ["where", package]
		else:
			cmd = ["which", package]
		return subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

	@staticmethod
	def get_sanity_status(self):
		# Get the system sanity status
		status = {}
		status["command_exists"] = self.command_exists
		status["get_distribution"] = self.sys.dsitribution()
		status["get_sysinfo"] = self.sys.info()
		status["is_package_installed"] = self.is_package_installed
		return status

	@staticmethod
	def is_in_virtual_environment():
		# Check if the script is running in a virtual environment
		return hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)

	@staticmethod
	def get_python_version():
		# Get the Python version
		return sys.version

	@staticmethod
	def get_python_executable():
		# Get the Python executable path
		return sys.executable

	@staticmethod
	def is_string_match(pattern, string):
		# Check if a string matches a regex pattern
		return bool(re.match(pattern, string))
