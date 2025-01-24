echo "MemoryTest: "
./VMtranslator tests/MemoryAccess/BasicTest/BasicTest.vm
echo "MemoryTest: "
./VMtranslator tests/MemoryAccess/PointerTest/PointerTest.vm
echo "MemoryTest: "
./VMtranslator tests/MemoryAccess/StaticTest/StaticTest.vm
echo "StackTest: "
./VMtranslator tests/StackArithmetic/SimpleAdd/SimpleAdd.vm
echo "StackTest: "
./VMtranslator tests/StackArithmetic/StackTest/StackTest.vm
echo "StackOverflow: "
./VMtranslator tests/StackOverflowTest/StackTestOverflow.vm
echo "T1:"
./VMtranslator tests/T1/T1.vm
echo "T2:"
./VMtranslator tests/T2/T2.vm
echo "T3:"
./VMtranslator tests/T2/T3/T3.vm
echo "ShiftTest:"
./VMtranslator tests/ShiftTest/ShiftTest.vm
echo "SimpleFunction: "
./VMtranslator tests/FunctionCalls/SimpleFunction/SimpleFunction.vm
echo "ProgramFlowTest: "
./VMtranslator tests/ProgramFlow/BasicLoop/BasicLoop.vm
echo "ProgramFlowTest: "
./VMtranslator tests/ProgramFlow/FibonacciSeries/FibonacciSeries.vm
# check the output of the VMtranslator
cd ../../tools
echo "BasicTest: "
./CPUEmulator.sh ../projects/07/tests/MemoryAccess/BasicTest/BasicTest.tst
echo "PointerTest: "
./CPUEmulator.sh ../projects/07/tests/MemoryAccess/PointerTest/PointerTest.tst
echo "StaticTest: "
./CPUEmulator.sh ../projects/07/tests/MemoryAccess/StaticTest/StaticTest.tst
echo "SimpleAdd: "
./CPUEmulator.sh ../projects/07/tests/StackArithmetic/SimpleAdd/SimpleAdd.tst
echo "StackTest: "
./CPUEmulator.sh ../projects/07/tests/StackArithmetic/StackTest/StackTest.tst
echo "StackOverflow: "
./CPUEmulator.sh ../projects/07/tests/StackOverflowTest/StackTestOverflow.tst
echo "T1: "
./CPUEmulator.sh ../projects/07/tests/T1/T1.tst
echo "T2: "
./CPUEmulator.sh ../projects/07/tests/T2/T2.tst
echo "T3: "
./CPUEmulator.sh ../projects/07/tests/T2/T3/T3.tst
echo "ShiftTest: "
./CPUEmulator.sh ../projects/07/tests/ShiftTest/ShiftTest.tst
echo "SimpleFunction: "
./CPUEmulator.sh ../projects/07/tests/FunctionCalls/SimpleFunction/SimpleFunction.tst
echo "BasicLoop: "
./CPUEmulator.sh ../projects/07/tests/ProgramFlow/BasicLoop/BasicLoop.tst
echo "FibonacciSeries: "
./CPUEmulator.sh ../projects/07/tests/ProgramFlow/FibonacciSeries/FibonacciSeries.tst

# echo "FibonacciElement: "
# ./VMtranslator tests/FunctionCalls/FibonacciElement
# echo "NestedCall: "
# ./VMtranslator tests/FunctionCalls/NestedCall
# echo "StaticsTest: "
# ./VMtranslator tests/FunctionCalls/StaticsTest
# cd ../../tools
# echo "FibonacciElement: "
# ./CPUEmulator.sh ../projects/07/tests/FunctionCalls/FibonacciElement/FibonacciElement.tst
# echo "NestedCall: "
# ./CPUEmulator.sh ../projects/07/tests/FunctionCalls/NestedCall/NestedCall.tst
# echo "StaticsTest: "
# ./CPUEmulator.sh ../projects/07/tests/FunctionCalls/StaticsTest/StaticsTest.tst


# echo "Reversi2: "
# ./VMtranslator tests/Reversi2
# echo "Snake: "
# ./VMtranslator tests/Snake
# echo "Pong: "
# ./VMtranslator tests/Pong
# echo "test: "
# ./VMtranslator tests/test
# echo "test2: "
# ./VMtranslator tests/test2
# echo "T3: "
# ./VMtranslator tests/T3
# cd ../../tools
# echo "Reversi2: "
# ./CPUEmulator.sh ../projects/07/tests/Reversi2/Reversi2.tst
# echo "Snake: "
# ./CPUEmulator.sh ../projects/07/tests/Snake/Snake.tst
# echo "Pong: "
# ./CPUEmulator.sh ../projects/07/tests/Pong/Pong.tst
# echo "test: "
# ./CPUEmulator.sh ../projects/07/tests/test/test.tst
# echo "test2: "
# ./CPUEmulator.sh ../projects/07/tests/test2/test2.tst
# echo "T3: "
# ./CPUEmulator.sh ../projects/07/tests/T3/T3.tst