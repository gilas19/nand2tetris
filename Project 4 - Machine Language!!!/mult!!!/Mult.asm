// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

//i=0
    @i
    M=0
//R2=0
    @R2
    M=0
//if R0=0, than END
    @R0
    D=M
    @END
    D;JEQ
//if R1=0, than END
    @R1
    D=M
    @END
    D;JEQ
//for i=0..R1: R2+=R0
(LOOP)
//R2+=R0
    @R0
    D=M
    @R2
    M=D+M
//i++
    @i
    M=M+1
    @R1
    D=M
    @i
    D=D-M
    @END
    D;JEQ
    @LOOP
    0;JMP
(END)
    0;JMP
