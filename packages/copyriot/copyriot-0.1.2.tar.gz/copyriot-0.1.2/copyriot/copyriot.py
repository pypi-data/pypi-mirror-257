import os
import argparse

headers = {
    '.py': '#', '.sh': '#', # Python and Shell scripts might have shebangs
    '.conf': '#', '.bst': '#', '.yml': '#', '.yaml': '#', '.toml': '#',
    '.build': '#', '.lock': '#', '.resource': '#', '.service': '#',
    '.network': '#', '.preset': '#', '.slice': '#', '.cmake': '#',
    'dockerfile': '#', 'Dockerfile': '#', '.bzl': '#', '.bazel': '#',
    'CMakeLists.txt': '#',
    '.rs': '//', '.c': '//', '.cpp': '//', '.h': '//', '.hpp': '//',
    '.lua': '--',
    '.xml': '<!--', '.md': '<!--'
}

def add_header_to_file(filepath, header_texts):
    def header_present_in_start(start_of_file, keywords):
        return any(keyword.lower() in start_of_file.lower() for keyword in keywords)

    filename = os.path.basename(filepath)
    # Determine the header based on file extension or special cases
    header_prefix = None
    for ext, prefix in headers.items():
        if filename.endswith(ext) or filename == ext:
            header_prefix = prefix
            break

    if header_prefix is None:
        print(f"{filepath} does not have a recognized extension, skipped")
        return  # Skip files without a matching extension

    # Build the appropriate header based on file type
    if header_prefix == '<!--':
        full_header = '\n'.join([header_prefix + " " + header for header in header_texts]+ " -->") + '\n'
        full_header = f"{header_prefix} {header_text} -->\n"
    else:
         full_header = '\n'.join([header_prefix + " " + header for header in header_texts]) + '\n'

    with open(filepath, 'r+', encoding='utf-8') as file:
        start_of_file = file.read(1024)
        if header_present_in_start(start_of_file, ['license', 'copyright']):
            print(f"{filepath} skipped")
            return  # Skip file if header already exists

    with open(filepath, 'r+', encoding='utf-8') as file:
        original_content = file.read()

        # Determine if a shebang line is present
        lines = original_content.splitlines(True)
        if lines and lines[0].startswith('#!'):
            content = lines[0] + full_header + ''.join(lines[1:])
        else:
            content = full_header + original_content

        # Reset file pointer and overwrite the file
        file.seek(0)
        file.write(content)
        file.truncate()  # Ensure file is not longer than new content
        print(f"{filepath} is updated")

def process_directory(directory, header_texts):
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            add_header_to_file(filepath, header_texts)
