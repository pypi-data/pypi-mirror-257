import os
import json
import string
import random

def generate_random_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def split_file(file_path, chunk_size_mb, add_metadata=False):
    chunk_size_bytes = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    output_folder = f'{file_name}_chunks'
    os.makedirs(output_folder, exist_ok=True)

    chunk_ids = []  # Initialize list to store chunk IDs

    with open(file_path, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size_bytes)
            if not chunk:
                break
            chunk_number += 1
            random_chunk_name = generate_random_name()
            chunk_ids.append(random_chunk_name)  # Add chunk ID to the list
            chunk_file_path = os.path.join(output_folder, f'{random_chunk_name}.woah')
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
        
        if add_metadata:
            metadata = {
                'file_name': file_name,
                'file_extension': file_extension,
                'total_chunks': chunk_number,
                'chunk_size_mb': chunk_size_mb,
                'chunk_ids': chunk_ids  # Add chunk IDs to the metadata
            }
            with open(os.path.join(output_folder, f'{file_name}_metadata.json'), 'w') as meta_file:
                json.dump(metadata, meta_file)
        
        print(f'Split complete. {chunk_number} chunks created in folder {output_folder}.')

def split_files_in_folder(folder_path, chunk_size_mb, add_metadata=False):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for file in files:
        file_path = os.path.join(folder_path, file)
        split_file(file_path, chunk_size_mb, add_metadata)

"""
# Example usage:
chunk_size_mb = 20  # Set your desired chunk size in megabytes
file_or_folder_path = 'woahdiscord\Wireshark-4.2.2-x64.exe'

if os.path.isfile(file_or_folder_path):
    split_file(file_or_folder_path, chunk_size_mb, add_metadata=True)
elif os.path.isdir(file_or_folder_path):
    split_files_in_folder(file_or_folder_path, chunk_size_mb, add_metadata=True)
else:
    print('Invalid file or folder path.')
"""