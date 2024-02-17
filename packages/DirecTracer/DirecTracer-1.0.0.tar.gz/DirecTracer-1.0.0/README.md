# DirecTracer

DirecTracer is a Python script that generates a directory structure in both text and Markdown formats. It can be used to visualize the hierarchy of folders and files in a given directory, while also excluding specific folders and file extensions.

## Features

- Generates a directory structure in text and Markdown formats.
- Supports ignoring specific directories and file extensions.
- Outputs clickable links in the Markdown file for easy navigation.

## Demonstration Video

Click on the thumbnail below to watch the demonstration video on YouTube.

[![DirecTracer](./demo/thumbnail2.png)](https://youtu.be/FqMauKiTvVs?si=FJlBiQBwpZb7_IPm)

## Usage

1. Ensure you have Python installed on your system.

2. Clone this repository or download the `DirecTracer.py` file.

3. Modify the `main` function in `DirecTracer.py` to set your preferred configuration options:

   - `current_directory`: The root directory you want to generate the structure for.
   - `text_output_file`: The name of the text output file.
   - `markdown_output_file`: The name of the Markdown output file.
   - `ignored_directories`: List of directories to ignore.
   - `ignored_extensions`: List of file extensions to ignore.

4. Run the script using the following command:

   ```bash
   python DirecTracer.py
   ```

5. Once the script completes, you'll find the generated text and Markdown files in the same directory.

## Output Example

To have a look at the current directory structure of this repository, check out the [directory_structure.md](./directory_structure.md) file.
