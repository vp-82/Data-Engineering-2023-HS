#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Get the directory path from the argument
dir_path="$1"

# Check if the specified directory exists
if [ ! -d "$dir_path" ]; then
    echo "Error: Directory $dir_path does not exist."
    exit 1
fi

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null
then
    echo "Error: pandoc could not be found. Please install pandoc and try again."
    exit 1
fi

# Iterate over all .md files in the specified directory
for md_file in "$dir_path"/*.md; do
    # Check if there are no .md files in the directory
    if [ ! -f "$md_file" ]; then
        echo "No .md files found in $dir_path."
        exit 1
    fi

    # Get the filename without the extension
    filename=$(basename -- "$md_file")
    filename_no_ext="${filename%.md}"

    # Define the output PDF file path
    pdf_file="$dir_path/$filename_no_ext.pdf"

    # Convert .md to .pdf using pandoc
    echo "Converting $md_file to $pdf_file..."
    pandoc -s "$md_file" -o "$pdf_file" --pdf-engine=xelatex --template=templates/custom-template.tex -V colorlinks=true \
    -V linkcolor=red \
    -V urlcolor=blue \
    -V toccolor=gray
done

echo "Conversion completed!"