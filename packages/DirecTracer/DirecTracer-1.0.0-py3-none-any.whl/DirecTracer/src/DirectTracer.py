import os
import urllib.parse
import time


def print_with_loading(message, delay=0.005):
    """ Print a message with a loading animation.

    Args:
        message (str): The message to print.
        delay (float, optional): The delay between each character. Defaults to 0.005.
    """

    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)

    print("", flush=True)


def save_directory_structure(root_dir=os.getcwd(),
                             text_output_file="directory_structure.txt",
                             markdown_output_file="directory_structure.md",
                             ignored_directories=[
                                 ".git", ".vscode", "venv", ".idea", "out"],
                             ignored_extensions=[".exe"],
                             animation=False):
    """
    Save the directory structure to text and Markdown files.

    Args:
        root_dir (str): The root directory to start scanning from.
        text_output_file (str): The name of the text output file.
        markdown_output_file (str): The name of the Markdown output file.
        ignored_directories (list, optional): List of directories to ignore. Defaults to None.
        ignored_extensions (list, optional): List of file extensions to ignore. Defaults to None.
        animation (bool, optional): Enable/Disable the loading animation. Defaults to False.
    """

    with open(text_output_file, 'w', encoding='utf-8') as text_f, open(markdown_output_file, 'w', encoding='utf-8') as md_f:

        # Write the Markdown header
        md_f.write("# Directory Structure\n\n")

        # Write the format template
        md_f.write("Format:\n\n")
        md_f.write("```md\n")
        md_f.write("📂 Directory\n")
        md_f.write("  - File\n")
        md_f.write("```\n\n")

        is_first_directory = True

        print("Reading directory structure...")

        # Result parameters
        total_folders = 0
        total_files = 0

        # Walk through the directory tree
        for root, dirs, files in os.walk(root_dir):

            # Remove ignored directories from the list
            if ignored_directories:
                dirs[:] = [d for d in dirs if d not in ignored_directories]

            # Get the relative path and indentation level
            relative_path = os.path.relpath(root, root_dir)
            depth = relative_path.count(os.path.sep)
            indentation = "\t" * depth

            # Write folder information to both text and Markdown files
            if is_first_directory:
                text_f.write(
                    f"{indentation}📂 {os.path.basename(root)} (Current Directory)\n")
                md_f.write(
                    f"{'  ' * depth}- 📂 **{os.path.basename(root)} (Current Directory)**\n")
                is_first_directory = False
            else:
                text_f.write(f"{indentation}📂 {os.path.basename(root)}\n")
                md_f.write(f"{'  ' * depth}- 📂 **{os.path.basename(root)}**\n")

            print(f"✅ Read {relative_path} contents")

            # Update the folder count
            total_folders += 1

            # Loop through the files in the current directory
            for file in files:

                # Get the file extension
                _, file_extension = os.path.splitext(file)

                # Skip ignored file extensions
                if ignored_extensions and file_extension in ignored_extensions:
                    continue

                # Write file information to text file
                text_f.write(f"{indentation}  - {file}\n")

                # Generate relative file path with forward slashes
                file_path = os.path.join(
                    relative_path, file).replace(os.path.sep, '/')

                # Encode spaces in the filename for Markdown link
                encoded_file_path = urllib.parse.quote(file_path)

                # Write clickable file link to Markdown file
                md_f.write(
                    f"{'  ' * (depth + 1)}- [{file}]({encoded_file_path})\n")

                # Update the file count
                total_files += 1

        if animation:
            print_with_loading("\n🌲 Directory structure read successfully.")
            print_with_loading(f"Total folders: {total_folders}")
            print_with_loading(f"Total files: {total_files}", 0.02)
        else:
            print("\n🌲 Directory structure read successfully.")
            print(f"Total folders: {total_folders}")
            print(f"Total files: {total_files}")

    # Print the output file paths
    if animation:
        print_with_loading("\nDirectory structure saved to:")
        print_with_loading(f"📄 {text_output_file}")
        print_with_loading(f"📘 {markdown_output_file}")
    else:
        print("\nDirectory structure saved to:")
        print(f"📄 {text_output_file}")
        print(f"📘 {markdown_output_file}")


def main():

    save_directory_structure(root_dir=os.getcwd(), animation=True)

    # ? animation = True/False: Enable/Disable the loading animation


if __name__ == "__main__":
    main()
