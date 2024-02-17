# DirecTracer

DirecTracer is a Python script that generates a directory structure in both text and Markdown formats. It can be used to visualize the hierarchy of folders and files in a given directory, while also excluding specific folders and file extensions.

## Features

- Generates a directory structure in text and Markdown formats.
- Supports ignoring specific directories and file extensions.
- Outputs clickable links in the Markdown file for easy navigation.
- Text & loading animations while generating the directory structure.

## Demonstration Video

Click on the thumbnail below to watch the demonstration video on YouTube.

[![DirecTracer](./demo/thumbnail2.png)](https://youtu.be/FqMauKiTvVs?si=FJlBiQBwpZb7_IPm)

## Usage

Clone this repository using the following command:

```bash
git clone https://github.com/Hardvan/DirecTracer
cd DirecTracer
pip install .
```

OR

Install the DirecTracer package using the following command:

```bash
pip install DirecTracer
```

Call the `save_directory_structure` function from the `DirecTracer` module to generate the directory structure.

```python
from DirecTracer import save_directory_structure
import os


# Generate the directory structure in text and Markdown formats
save_directory_structure(
   root_dir=os.getcwd(),
   text_output_file="directory_structure.txt",
   markdown_output_file="directory_structure.md",
   animation=True
)
```

The function accepts the following parameters:

- **root_dir (str):** The root directory to start scanning from.
- **text_output_file (str):** The name of the text output file.
- **markdown_output_file (str):** The name of the Markdown output file.
- **ignored_directories (list, optional):** List of directories to ignore. Defaults to None.
- **ignored_extensions (list, optional):** List of file extensions to ignore. Defaults to None.
- **animation (bool, optional):** Enable/Disable the loading animation. Defaults to False.

## Output Example

To have a look at the current directory structure of this repository, check out the [directory_structure.md](./directory_structure.md) file.

## Run the following commands to update the package

1. Change version in `setup.py`
2. Run the following commands

   ```bash
   python setup.py bdist_wheel sdist
   twine upload dist/*
   ```
