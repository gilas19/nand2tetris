# Directories
TOOLS_DIR = ../tools
CPU_EMULATOR = $(TOOLS_DIR)/CPUEmulator.sh

# Test directories
FUNCTION_CALLS_DIR = FunctionCalls
PROGRAM_FLOW_DIR = ProgramFlow

# All test targets
TESTS = SimpleFunction FibonacciElement StaticsTest NestedCall BasicLoop FibonacciSeries

.PHONY: all clean $(TESTS)

all: $(TESTS)

# Function Calls tests
SimpleFunction: $(FUNCTION_CALLS_DIR)/SimpleFunction/SimpleFunction.tst
	./VMtranslator $(FUNCTION_CALLS_DIR)/SimpleFunction/SimpleFunction.vm
	$(CPU_EMULATOR) $(FUNCTION_CALLS_DIR)/SimpleFunction/SimpleFunction.tst

FibonacciElement: $(FUNCTION_CALLS_DIR)/FibonacciElement
	./VMtranslator $(FUNCTION_CALLS_DIR)/FibonacciElement
	$(CPU_EMULATOR) $(FUNCTION_CALLS_DIR)/FibonacciElement/FibonacciElement.tst

StaticsTest: $(FUNCTION_CALLS_DIR)/StaticsTest
	./VMtranslator $(FUNCTION_CALLS_DIR)/StaticsTest
	$(CPU_EMULATOR) $(FUNCTION_CALLS_DIR)/StaticsTest/StaticsTest.tst

NestedCall: $(FUNCTION_CALLS_DIR)/NestedCall
	./VMtranslator $(FUNCTION_CALLS_DIR)/NestedCall
	$(CPU_EMULATOR) $(FUNCTION_CALLS_DIR)/NestedCall/NestedCall.tst

# Program Flow tests
BasicLoop: $(PROGRAM_FLOW_DIR)/BasicLoop/BasicLoop.tst
	./VMtranslator $(PROGRAM_FLOW_DIR)/BasicLoop/BasicLoop.vm
	$(CPU_EMULATOR) $(PROGRAM_FLOW_DIR)/BasicLoop/BasicLoop.tst

FibonacciSeries: $(PROGRAM_FLOW_DIR)/FibonacciSeries/FibonacciSeries.tst
	./VMtranslator $(PROGRAM_FLOW_DIR)/FibonacciSeries/FibonacciSeries.vm
	$(CPU_EMULATOR) $(PROGRAM_FLOW_DIR)/FibonacciSeries/FibonacciSeries.tst

# Clean generated files
clean:
	rm -f $(FUNCTION_CALLS_DIR)/*/*.asm
	rm -f $(PROGRAM_FLOW_DIR)/*/*.asm
	rm -f $(FUNCTION_CALLS_DIR)/*/*.out
	rm -f $(PROGRAM_FLOW_DIR)/*/*.out
