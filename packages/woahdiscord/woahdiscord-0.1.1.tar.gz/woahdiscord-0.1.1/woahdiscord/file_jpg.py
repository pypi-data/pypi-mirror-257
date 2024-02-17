import base64
import json
import os
import random
import string

def generate_random_string(length=8):
    """Generate a random string of letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def file_jpg(input_path):
    # If input_path is a file, convert it to a list with a single element
    if os.path.isfile(input_path):
        files = [input_path]
    # If input_path is a directory, get all files within the directory
    elif os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
    else:
        print("Invalid input path.")
        return

    # Generate a random folder name
    output_folder = generate_random_string()
    os.makedirs(output_folder, exist_ok=True)

    for input_file in files:
        # Read the contents of the input file
        with open(input_file, 'rb') as f:
            data = f.read()

        # Convert the file data to base64
        encoded_data = base64.b64encode(data).decode('utf-8')

        # Save the base64 data to a JSON metadata file
        file_name, input_extension = os.path.splitext(os.path.basename(input_file))
        output_jpg = os.path.join(output_folder, file_name + '.jpg')
        metadata_file = os.path.join(output_folder, file_name + '_metadata.json')
        output_extension = '.jpg'
        metadata = {
            'original_filename': os.path.basename(input_file),
            'original_file_extension': input_extension,
            'output_filename': os.path.basename(output_jpg),
            'output_file_extension': output_extension,
            'data': encoded_data
        }
        with open(metadata_file, 'w') as json_file:
            json.dump(metadata, json_file)

        # Convert the base64 data to bytes and save it as a .jpg file
        with open(output_jpg, 'wb') as jpg_file:
            jpg_file.write(base64.b64decode(encoded_data))

        print(f"File '{input_file}' has been converted to '{output_jpg}' and metadata saved to '{metadata_file}'.")

"""
# Example usage:
input_path = 'woahdiscord\Wireshark-4.2.2-x64.exe'  # Can be a file or a directory
file_jpg(input_path)
"""