# standard imports
import argparse

# copyriot imports
from .copyriot import add_header_to_file, process_directory

def main():
    parser = argparse.ArgumentParser(description='Add headers to files in a directory.')
    parser.add_argument('--header', '-t', type=str, nargs='+', required=True, help='One or more header texts to add.')
    parser.add_argument('--file', '-f', type=str, nargs='+', help='The path to the file.')
    parser.add_argument('--directory', '-d', type=str, help='The path to the directory.')
    args = parser.parse_args()

    if args.file:
        for file_path in args.file:
            add_header_to_file(file_path, args.header)
    elif args.directory:
        process_directory(args.directory, args.header)
    else:
        print("Error: Please specify either a file with --file or a directory with --directory.")

if __name__ == "__main__":
    main()
