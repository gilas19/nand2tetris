# Compiler and source files
PY_FILES := CodeWriter.py Main.py Parser.py
VM_TRANSLATOR := VMtranslator

# Test directories and files
MEMORY_ACCESS_DIR := MemoryAccess
STACK_ARITHMETIC_DIR := StackArithmetic
MEMORY_ACCESS_TESTS := BasicTest PointerTest StaticTest
STACK_ARITHMETIC_TESTS := SimpleAdd StackTest

# Tool paths
CPU_EMULATOR := ../tools/CPUEmulator.sh
TEXT_COMPARATOR := ../tools/TextComparer.sh

# Generate full paths for test files
MEMORY_VM_FILES := $(foreach test,$(MEMORY_ACCESS_TESTS),$(MEMORY_ACCESS_DIR)/$(test)/$(test).vm)
STACK_VM_FILES := $(foreach test,$(STACK_ARITHMETIC_TESTS),$(STACK_ARITHMETIC_DIR)/$(test)/$(test).vm)
ALL_VM_FILES := $(MEMORY_VM_FILES) $(STACK_VM_FILES)
ALL_ASM_FILES := $(ALL_VM_FILES:.vm=.asm)

.PHONY: all clean test tools memory_tests stack_tests

all: $(VM_TRANSLATOR) $(ALL_ASM_FILES)

# Pattern rule for VM to ASM conversion
%.asm: %.vm $(VM_TRANSLATOR)
	./$(VM_TRANSLATOR) $<

# Create VM translator executable
$(VM_TRANSLATOR): $(PY_FILES)
	chmod +x $(VM_TRANSLATOR)
	touch $(VM_TRANSLATOR)

# Set up tools
tools:
	chmod +x $(PY_FILES) $(VM_TRANSLATOR)
	chmod +x $(CPU_EMULATOR) $(TEXT_COMPARATOR)

# Memory access tests
memory_tests: $(VM_TRANSLATOR) tools
	@for test in $(MEMORY_ACCESS_TESTS); do \
		echo "Running memory access test: $$test"; \
		$(MAKE) $(MEMORY_ACCESS_DIR)/$$test/$$test.asm; \
		$(CPU_EMULATOR) $(MEMORY_ACCESS_DIR)/$$test/$$test.tst || exit 1; \
		$(TEXT_COMPARATOR) $(MEMORY_ACCESS_DIR)/$$test/$$test.cmp \
			$(MEMORY_ACCESS_DIR)/$$test/$$test.out || exit 1; \
	done

# Stack arithmetic tests
stack_tests: $(VM_TRANSLATOR) tools
	@for test in $(STACK_ARITHMETIC_TESTS); do \
		echo "Running stack arithmetic test: $$test"; \
		$(MAKE) $(STACK_ARITHMETIC_DIR)/$$test/$$test.asm; \
		$(CPU_EMULATOR) $(STACK_ARITHMETIC_DIR)/$$test/$$test.tst || exit 1; \
		$(TEXT_COMPARATOR) $(STACK_ARITHMETIC_DIR)/$$test/$$test.cmp \
			$(STACK_ARITHMETIC_DIR)/$$test/$$test.out || exit 1; \
	done

# Run all tests
test: memory_tests stack_tests

# Clean generated files
clean:
	rm -f $(ALL_ASM_FILES)
	rm -f $(MEMORY_ACCESS_DIR)/*/*.out
	rm -f $(STACK_ARITHMETIC_DIR)/*/*.out