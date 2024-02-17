A python library allowing discord to be used unlimited cloud storage. 

## What's the purpose?

Cloud storage is expensive even if you have a 10 USD and 20 USD laying around. Social media platforms like Instagram, YouTube, Discord offers unlimited storage to upload attachments and files. Though being limited to certain file extensions in some instances. 

With careful planning, we can take advantage of that and upload data from our local storage to those platforms and use them as cloud storages. In this library, I have implemented the required functions to achieve that.

### Examples

**How to split a file into small chunks**

```Python
from woahdiscord import split_file

chunk_size_mb = 20  # Set your desired chunk size in megabytes

file_or_folder_path = 'woahdiscord\Wireshark-4.2.2-x64.exe'

if os.path.isfile(file_or_folder_path):

    split_file(file_or_folder_path, chunk_size_mb, add_metadata=True)

elif os.path.isdir(file_or_folder_path):

    split_files_in_folder(file_or_folder_path, chunk_size_mb, add_metadata=True)

else:

    print('Invalid file or folder path.')
```

**How to merge the chunks**

```Python
from woahdiscord import merge_files
folder_path = "Wireshark-4.2.2-x64_chunks"

merge_files(folder_path)
```

**How to convert a file into jpg/jpeg**

```Python
from woahdiscord import file_jpg

input_path = 'woahdiscord\Wireshark-4.2.2-x64.exe'  # Can be a file or a directory

file_jpg(input_path)
```

Reconstructing jpg into original

```Python
from woahdiscord import osmosis

folder_path = 'CXh2bgPY'  # Provide the folder path here

osmosis(folder_path)
```

**Setting up discord bot to upload files automatically**

```Python
from woahdiscord import auto_upload

auto_upload_files("your/folder/path", "<Your Bot Token>")
```