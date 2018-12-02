import os

from classes.ResourceFile import ResourceFile

import progressbar

file_list = []
ResourceFile_list = []

# Find all files
for root, dirs, files in os.walk("./ResFiles", topdown=False):
	for name in files:
		file_path = os.path.join(root, name)
		file_list.append(file_path)

print("Creating ResourceFile objects...")
current_resource_file_iterator = 0
for file in progressbar.progressbar(file_list):
	new_ResourceFile = ResourceFile(file)
	ResourceFile_list.append(new_ResourceFile)
	current_resource_file_iterator += 1

print("Parsing files...")
for current_resource_file in progressbar.progressbar(ResourceFile_list):
	current_resource_file.parse_file()
