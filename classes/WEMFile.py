from extractaudioglobals import export_directory_path


class WEMFile:

	def __init__(self, start_position_input, end_position_input, WEM_File_index_input):
		self.start_position = start_position_input
		self.end_position = end_position_input
		self.WEM_File_index = WEM_File_index_input

	def extract_WEM(self, parsed_bytes_input, original_file_name_input):
		byte_slice = parsed_bytes_input[self.start_position:self.end_position]
		file_to_save = open(f"{export_directory_path}{original_file_name_input}{self.WEM_File_index}.wem", "wb")
		file_to_save.write(byte_slice)
		file_to_save.close()
