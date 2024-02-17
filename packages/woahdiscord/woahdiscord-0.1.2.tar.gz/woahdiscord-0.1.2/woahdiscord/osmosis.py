import base64
import json
import os

def osmosis(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return
    
    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a JSON metadata file
        if file_name.endswith('_metadata.json'):
            metadata_file_path = os.path.join(folder_path, file_name)
            # Read metadata from the JSON file
            with open(metadata_file_path, 'r') as json_file:
                metadata = json.load(json_file)
            
            # Get the original and output file paths
            original_file_path = os.path.join(folder_path, metadata['original_filename'])
            output_file_path = os.path.join(folder_path, metadata['output_filename'])
            
            # Read base64 data from metadata
            encoded_data = metadata['data']
            
            # Decode base64 data and write it back to the original file format
            original_extension = metadata['original_file_extension']
            restored_file_path = os.path.splitext(output_file_path)[0] + original_extension
            with open(restored_file_path, 'wb') as restored_file:
                restored_file.write(base64.b64decode(encoded_data))
            
            print(f"File '{output_file_path}' has been reconstructed to '{restored_file_path}'.")

"""
# Example usage:
folder_path = 'CXh2bgPY'  # Provide the folder path here
osmosis(folder_path)
"""
