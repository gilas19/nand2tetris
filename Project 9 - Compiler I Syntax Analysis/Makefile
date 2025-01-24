# Makefile for JackAnalyzer

# Variables
PYTHON := python3
JACK_ANALYZER := JackAnalyzer.py
TEST_DIR := Tests

# Get a list of all .jack files in the test directory and subdirectories
JACK_FILES := $(shell find $(TEST_DIR) -name "*.jack")

# Define XML output files by replacing .jack with .xml
XML_FILES := $(JACK_FILES:.jack=.xml)

# Default target
all: test

# Run the analyzer on all test files
analyze: $(XML_FILES)

%.xml: %.jack
	$(PYTHON) $(JACK_ANALYZER) $<

# Compare generated files with reference files
.PHONY: compare
compare: analyze
	@for file in $(XML_FILES); do \
		ref_file="$${file%.*}.ref.xml"; \
		if [ -f $$ref_file ]; then \
			if diff -w $$file $$ref_file > /dev/null; then \
				echo "✓ $$file matches reference"; \
			else \
				echo "✗ $$file differs from reference"; \
				diff -w $$file $$ref_file; \
			fi \
		fi; \
	done

# Shortcut for testing
.PHONY: test
test: compare

# Clean the output directory
.PHONY: clean
clean:
	rm -f $(XML_FILES)
