from checksum import generate_checksums_for_directory

# Directory to scan, adjust to your requirement
directory_path = '.'

# Folders to exclude from the scan
excluded_folders = ['node_modules', 'env']

def main():
    generate_checksums_for_directory(directory_path, excluded_folders)
