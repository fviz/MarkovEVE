from extract_audio.extractaudioglobals import word_to_search
from classes.WEMFile import WEMFile
import os
import re


class ResourceFile:

	def __init__(self, input_file):
		self.data_to_parse = open(input_file, "rb")
		self.original_filename = os.path.basename(self.data_to_parse.name)
		self.parsed_bytes = self.data_to_parse.read()
		self.data_to_parse.close()
		self.WEMFiles = []

	def parse_file(self):
		previous_start_position = 0
		WEM_File_index_counter = 0
		for match in re.finditer(word_to_search, self.parsed_bytes):
			current_start_position = match.start()  # Get position of current match
			if previous_start_position is 0:  # If no previous match, set this as first position
				previous_start_position = current_start_position
				continue
			new_WEM_file = WEMFile(previous_start_position, match.start(), WEM_File_index_counter)  # Create instance of WEMFile
			self.WEMFiles.append(new_WEM_file)  # Add instance to list
			previous_start_position = match.start()  # Set starting point for next match
			WEM_File_index_counter += 1  # Increase match counter

		for wf in self.WEMFiles:
			wf.extract_WEM(self.parsed_bytes, self.original_filename)
