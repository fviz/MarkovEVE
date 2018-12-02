import os
import re

export_directory_path = "./export/WW2OGGExport/drive_c/users/vzntn/convert/"

data_to_parse = open("./ResFiles/22/226a2481f84fce54_bb8e0bac65c8509f14f40a4cf98a258a", "rb")
original_file_name = os.path.basename(data_to_parse.name)
parsed_bytes = data_to_parse.read()
word_to_search = b"RIFF"


class WEMFile:

	def __init__(self, start_position_input, end_position_input, WEM_File_index_input):
		self.start_position = start_position_input
		self.end_position = end_position_input
		self.WEM_File_index = WEM_File_index_input

	def extract_WEM(self):
		print("Slicing parsed data...")
		byte_slice = parsed_bytes[self.start_position:self.end_position]
		print("Writing to file...")
		file_to_save = open(f"{export_directory_path}{original_file_name}{self.WEM_File_index}.wem", "wb")
		file_to_save.write(byte_slice)
		file_to_save.close()
		print("Done.")


WEMFiles = []

previous_start_position = 0
WEM_File_index_counter = 0
for match in re.finditer(word_to_search, parsed_bytes):
	current_start_position = match.start()									# Get position of current match
	if previous_start_position is 0:										# If no previous match, set this as first position
		previous_start_position = current_start_position
		continue
	new_WEM_file = WEMFile(previous_start_position, match.start(), WEM_File_index_counter)			# Create instance of WEMFile
	WEMFiles.append(new_WEM_file)											# Add instance to list
	print(f"Added WEM file at {previous_start_position}")
	previous_start_position = match.start()									# Set starting point for next match
	WEM_File_index_counter += 1												# Increase match counter

for WEMFile in WEMFiles:
	WEMFile.extract_WEM()
