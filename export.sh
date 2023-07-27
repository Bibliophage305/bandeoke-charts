#!/bin/bash

mkdir -p exports # Create the 'exports' subdirectory if it doesn't exist

failures=()

for file in *.mscz; do
  filename=$(basename "$file") # Extract the filename without the extension

  echo $filename

  output_file="exports/${filename%.*}.pdf" # Replace the extension with '.pdf' and prepend 'exports/'
  mscore -o "$output_file" "$file" > /dev/null 2>&1 # Run the 'mscore' command with the updated output filename

  if [ ! -f "$output_file" ]; then
    failures+=("$filename") # Add the filename to the failure array
    echo "failure!"
  fi
done

# Check if the array is not empty
if [ ${#failures[@]} -gt 0 ]; then
  # Print the filenames in the array
  echo "The following files failed to export:"
  for filename in "${failures[@]}"; do
    echo "$filename"
  done
else
  echo "All the files exported successfully"
fi
