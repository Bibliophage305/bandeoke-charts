MSCORE := "mscore"

MSCX_FILES = $(shell find . -name "*.mscx")
MSCZ_FILES = $(shell find . -name "*.mscz")
JOB_FILES = $(shell find . -name "*.json")

PDFS = $(MSCX_FILES:.mscx=.pdf) $(MSCZ_FILES:.mscz=.pdf)
MP3S = $(MSCX_FILES:.mscx=.mp3) $(MSCZ_FILES:.mscz=.mp3)
JOB_OUTS = $(JOB_FILES:.json=.job)

.PHONY: all
all: $(PDFS) $(MP3S) $(JOB_OUTS)

%.pdf: %.mscx
	$(MSCORE) -o $@ $<

%.mp3: %.mscx
	$(MSCORE) -o $@ $<

%.pdf: %.mscz
	$(MSCORE) -o $@ $<

%.mp3: %.mscz
	$(MSCORE) -o $@ $<

.SECONDARY:%.job
%.job: %.json
# Create a file at the beginning of the job
# Add to it a list of any files which were created in this
# directory after the job is done running. This allows for
# a full clean of the directory
#
# CAVEAT: This does not work well for parrallel builds using make
	touch $@.tmp
	cd $(dir $(abspath $<)) && $(MSCORE) -j $(notdir $<)
	find "$(dir $(abspath $<))" -type f -newer "$@.tmp" >> $@
	rm $@.tmp

.PHONY: clean
clean:
# Remove all files referenced by job files
	-for job_file in ${JOB_OUTS}; do cat $$job_file | xargs rm; done
	-rm -r $(JOB_OUTS)
	-rm -r $(PDFS) $(MP3S)
