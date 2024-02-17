import os
import json

def merge_files(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return
    
    # Find JSON file in the folder
    json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
    if not json_files:
        print("JSON file not found in the folder.")
        return
    
    # Assume the first JSON file found is the one to be used
    json_file_path = os.path.join(folder_path, json_files[0])
    
    # Load JSON file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    
    # Extract file name, extension, and chunk IDs
    file_name = json_data.get("file_name")
    file_extension = json_data.get("file_extension")
    chunk_ids = json_data.get("chunk_ids")
    
    # Initialize the output file path
    output_file_path = os.path.join(folder_path, f"{file_name}.{file_extension}")
    
    # Merge file chunks
    with open(output_file_path, 'wb') as output_file:
        for chunk_id in chunk_ids:
            chunk_file_path = os.path.join(folder_path, f"{chunk_id}.woah")
            if os.path.exists(chunk_file_path):
                with open(chunk_file_path, 'rb') as chunk_file:
                    output_file.write(chunk_file.read())
            else:
                print(f"Chunk file {chunk_id}.woah not found.")
    
    print("Files merged successfully.")

"""
# Example usage:
folder_path = "Wireshark-4.2.2-x64_chunks"
merge_files(folder_path)
"""