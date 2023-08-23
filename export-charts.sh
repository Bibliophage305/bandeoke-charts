#!/bin/bash

mkdir temp-exports

# copy old format files first
for file in old-format-charts/*.pdf; do
  filename=$(basename "$file") # Extract the filename without the path
  cp "${file}" "temp-exports/${filename}"
done

failures=()

# make sure it sees files starting with dot (...Baby One More Time)
shopt -s dotglob

for file in musescore-charts/*.mscz; do
  filename=$(basename "$file") # Extract the filename without the path

  echo $filename

  output_file="temp-exports/${filename%.*}.pdf" # Replace the extension with '.pdf' and prepend 'exports/'
  flatpak run org.musescore.MuseScore -o "$output_file" "$file" # Run the 'mscore' command with the updated output filename

  if [ ! -f "$output_file" ]; then
    failures+=("$filename") # Add the filename to the failure array
    echo "failure!"
    echo "::warning file=$filename::Musescore chart failed to export"
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
