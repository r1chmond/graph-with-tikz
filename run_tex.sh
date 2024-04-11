#!/bin/sh

#!/bin/bash

# Define a function to handle errors
handle_error() {
  echo "ERR" > "$output_file"

  echo "<!!!> ERR: An error occurred in the script"

    exit 1
}

# Set up a trap to catch errors
trap 'handle_error' ERR

# Main script logic
echo "Starting compilation..."

# Create a file to store command output
output_file="lastln_output.txt"

# Compile the LaTeX file with pdflatex
pdflatex -interaction=nonstopmode tester.tex 

# Check if compilation failed
if [ $? -ne 0 ]; then
  echo "pdflatex compilation failed"
  exit 1
fi

# Execute the Python script
python3 run_tex.py

# Check if Python execution failed
if [ $? -ne 0 ]; then
  echo "Python execution failed"
  exit 1
fi

echo "Script completed successfully"




