# Define the directory where the .mscz files are located
SOURCE_DIR := musescore-charts

EXPORT_DIR := chart-exports

# Get a list of all .mscz files in the directory (including filenames with spaces)
MSZC_FILES := $(shell find $(SOURCE_DIR) -type f -name "*.mscz")

# Generate the corresponding list of filenames without the .mscz extension
FILES := $(patsubst $(SOURCE_DIR)/%.mscz,%,$(MSZC_FILES))

# Default target to build all PDF files
all: $(FILES)

# Rule to generate PDF from .mscz files
$(SOURCE_DIR)/%:
	mscore -o "$(EXPORT_DIR)/$(patsubst $(SOURCE_DIR)/%,%,$@).pdf" "$@.mscz"

# Clean up generated PDF files
clean:
	rm -f $(PDF_FILES)



# .PHONY: all
# all:
# 	mkdir -p chart-exports # Create the 'exports' subdirectory if it doesn't exist
# # 	failures :=
# 	MSCZ_FILES = $(shell find musescore-charts -name "*.mscz")
#
# 	for file in musescore-charts/*.mscz; do
# 		filename=$(basename "$file") # Extract the filename without the extension
#
# 		echo $filename
#
# 		output_file="chart-exports/${filename%.*}.pdf" # Replace the extension with '.pdf' and prepend 'chart-exports/'
# # 		flatpak run org.musescore.MuseScore -o "$output_file" "$file" # Run the 'mscore' command via flatpak with the updated output filename
# 		mscore -o "$output_file" "$file" # Run the 'mscore' command via flatpak with the updated output filename
#
# # 		if [ ! -f "$output_file" ]; then
# # 			failures+=("$filename") # Add the filename to the failure array
# # 			echo "failure!"
# # 		fi
# 	done
#
# 	# Check if the array is not empty
# 	if [ ${#failures[@]} -gt 0 ]; then
# 		# Print the filenames in the array
# 		echo "The following files failed to export:"
# 		for filename in "${failures[@]}"; do
# 			echo "$filename"
# 		done
# 	else
# 		echo "All the files exported successfully"
# 	fi

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
