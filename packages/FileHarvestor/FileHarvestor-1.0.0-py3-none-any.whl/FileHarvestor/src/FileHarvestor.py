import os
import time


def read_files(file_list=None, output_text_file='./output/contents.txt', output_markdown_file='./output/contents.md'):
    """Reads the contents of the files in the list and writes them to the output text and markdown files. If the file does not exist, it is added to the list of not found files.

    Args:
        file_list (list, optional): List of files to read. Defaults to None.
        output_text_file (str, optional): Output text file. Defaults to './output/contents.txt'.
        output_markdown_file (str, optional): Output markdown file. Defaults to './output/contents.md'.
    """

    if file_list is None:
        print("❌ No files to read. Exiting.")
        return

    start_time = time.time()  # Start the timer

    directory = '.'

    # Create the output directory if it doesn't exist
    output_directory = os.path.dirname(output_text_file)
    os.makedirs(output_directory, exist_ok=True)

    not_found_files = []  # List to store files that were not found

    # Open the output files
    with open(output_text_file, 'w', encoding='utf-8') as text_output_handle, open(output_markdown_file, 'w', encoding='utf-8') as markdown_output_handle:

        # H1 heading for the markdown file
        markdown_output_handle.write("# Contents\n\n")

        for file_name in file_list:  # Iterate through the list of files

            t1 = time.time()  # Start the timer for each file

            file_path = os.path.join(directory, file_name)  # absolute path

            # Check if the file exists
            if os.path.exists(file_path):

                # Open the file with the appropriate encoding
                with open(file_path, 'r', encoding='utf-8') as input_file_handle:

                    contents = input_file_handle.read()

                    # Write the contents to the output text file
                    text_output_handle.write(f"{file_name}:\n")  # Title
                    text_output_handle.write(contents)  # Contents
                    text_output_handle.write("\n\n")  # New line

                    # Write the contents to the output markdown file
                    markdown_output_handle.write(
                        f"## {file_name}\n\n")  # H2 heading
                    markdown_output_handle.write(contents)
                    markdown_output_handle.write("\n\n")

                    t2 = time.time()  # End the timer for each file
                    elapsed_time = round(t2 - t1, 2)

                    print(
                        f"✅ '{file_path}' read successfully \033[90m({elapsed_time}s)\033[0m")

            else:
                print(f"❌ File '{file_path}' does not exist.")
                not_found_files.append(file_path)

    if not_found_files:
        print(
            f"❌ The following files were not found ({len(not_found_files)} of {len(file_list)}):")
        for file in not_found_files:
            print(f"  - {file}")
    else:
        print("\n✅ All files read successfully")

    end_time = time.time()  # End the timer
    elapsed_time = round(end_time - start_time, 2)

    print(
        f"\n✅ Output written to '{output_text_file}' and '{output_markdown_file}' \033[90m({elapsed_time}s)\033[0m")


if __name__ == "__main__":

    file_list = ["SampleDirectory/FolderA/File1.txt",
                 "SampleDirectory/FolderB/File1.txt",
                 "SampleDirectory/FolderC/File1.txt",
                 "SampleDirectory/FolderA/File2.txt",
                 "SampleDirectory/FolderB/File2.txt",
                 "SampleDirectory/FolderC/File2.txt",
                 "SampleDirectory/FolderA/File3.txt",
                 "SampleDirectory/FolderB/File3.txt",
                 "SampleDirectory/FolderC/File3.txt",
                 ]

    read_files(file_list=file_list,
               output_text_file='./output/contents.txt',
               output_markdown_file='./output/contents.md')
