import os
import sys
import time

def get_file_times(file_path):
    try:
        # Get file statistics
        stats = os.stat(file_path)

        # Extract times
        atime = stats.st_atime
        mtime = stats.st_mtime
        ctime = stats.st_ctime

        # Convert times to a readable format
        formatted_atime = time.ctime(atime)
        formatted_mtime = time.ctime(mtime)
        formatted_ctime = time.ctime(ctime)

        return formatted_atime, formatted_mtime, formatted_ctime

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None, None, None
    except OSError as e:
        print(f"OS error occurred: {e}")
        return None, None, None

# Replace this with the path of the file you want to check
file_path = '/dev/pts/0'

while 1:
    atime, mtime, ctime = get_file_times(file_path)
    if atime and mtime and ctime:
        print(f"Access Time: {atime}")
        print(f"Modification Time: {mtime}")
        print(f"Change Time: {ctime}")
    else:
        print("Failed to retrieve file times.")
    time.sleep(5)
