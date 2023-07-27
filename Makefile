MSCORE := "mscore"

MSCX_FILES = $(shell find . -name "*.mscx")
MSCZ_FILES = $(shell find . -name "*.mscz")
JOB_FILES = $(shell find . -name "*.json")

PDFS = $(MSCX_FILES:.mscx=.pdf) $(MSCZ_FILES:.mscz=.pdf)
MP3S = $(MSCX_FILES:.mscx=.mp3) $(MSCZ_FILES:.mscz=.mp3)
JOB_OUTS = $(JOB_FILES:.json=.job)

.PHONY: all
all:
	mkdir -p chart-exports # Create the 'exports' subdirectory if it doesn't exist

	failures=()

	for file in musescore-charts/*.mscz; do
		filename=$(basename "$file") # Extract the filename without the extension

		echo $filename

		output_file="chart-exports/${filename%.*}.pdf" # Replace the extension with '.pdf' and prepend 'chart-exports/'
		flatpak run org.musescore.MuseScore -o "$output_file" "$file" # Run the 'mscore' command via flatpak with the updated output filename

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

# .SECONDARY:%.job
# %.job: %.json
# # Create a file at the beginning of the job
# # Add to it a list of any files which were created in this
# # directory after the job is done running. This allows for
# # a full clean of the directory
# #
# # CAVEAT: This does not work well for parrallel builds using make
# 	touch $@.tmp
# 	cd $(dir $(abspath $<)) && $(MSCORE) -j $(notdir $<)
# 	find "$(dir $(abspath $<))" -type f -newer "$@.tmp" >> $@
# 	rm $@.tmp
