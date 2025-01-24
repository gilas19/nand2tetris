# Program files and tools
PROGRAM := Main.py Parser.py Code.py SymbolTable.py Assembler
SUBDIRS := $(wildcard */)
ASM_FILES := $(foreach dir,$(SUBDIRS),$(wildcard $(dir)*.asm))
HACK_FILES := $(ASM_FILES:.asm=.hack)
REFERENCE_HACK_FILES := $(ASM_FILES:.asm=.reference.hack)
TOOL_ASSEMBLER := ../tools/Assembler.sh
TEXT_COMPARATOR := ../tools/TextComparer.sh

.PHONY: all clean test tools

# Default target
all: $(HACK_FILES) test

# Make tools executable
tools:
	chmod +x $(PROGRAM)
	chmod +x $(TOOL_ASSEMBLER) $(TEXT_COMPARATOR)

# Create our assembler executable
Assembler: $(PROGRAM)
	chmod +x Assembler
	touch Assembler

# Pattern rule to create .hack files using our Assembler
%.hack: %.asm Assembler
	./Assembler $<

# Pattern rule to create reference .hack files using the tool assembler
%.reference.hack: %.asm
	$(TOOL_ASSEMBLER) $<
	mv $(basename $<).hack $@ 

# Test target - generates and compares all files
test: tools $(REFERENCE_HACK_FILES) $(HACK_FILES) 
	@for asm in $(ASM_FILES); do \
		echo "Testing assembly of $${asm}..."; \
		hack_file="$${asm%.asm}.hack"; \
		ref_file="$${asm%.asm}.reference.hack"; \
		$(TEXT_COMPARATOR) "$$hack_file" "$$ref_file" || exit 1; \
		echo "✓ Assembly matches for $${asm}"; \
	done
	@echo "All assemblies matched successfully!"

# Clean generated files
clean:
	rm -f $(HACK_FILES) $(REFERENCE_HACK_FILES)
