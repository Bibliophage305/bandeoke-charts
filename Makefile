# Define the default target, which will be executed when you run 'make' without any arguments.
all: export_charts

# Target to export charts using the shell script
export_charts:
	mkdir -p chart-exports
	failures=(); \
	for file in musescore-charts/*.mscz; do \
		filename=$$(basename "$$file"); \
		echo "$$filename"; \
		output_file="chart-exports/$${filename%.*}.pdf"; \
		flatpak run org.musescore.MuseScore -o "$$output_file" "$$file"; \
		if [ ! -f "$$output_file" ]; then \
			failures+=("$$filename"); \
			echo "failure!"; \
		fi; \
	done; \
	if [ $${failures[@]} -gt 0 ]; then \
		echo "The following files failed to export:"; \
		for filename in "$${failures[@]}"; do \
			echo "$$filename"; \
		done; \
	else \
		echo "All the files exported successfully"; \
	fi

# Add a target to clean up generated files (if necessary)
clean:
	rm -rf chart-exports
