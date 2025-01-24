// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(INIT)
    @SCREEN
    D=A
    @i
    M=D
    @color
    M=0
(LISTEN)
    @KBD
    D=M
    @BLACK
    D;JGT
    @WHITE
    D;JEQ
    @LISTEN
    0;JMP
(BLACK)
    @color
    M=-1
    @CHANGE
    0;JMP
(WHITE)
    @color
    M=0
    @CHANGE
    0;JMP
(CHANGE)
    @color
    D=M
    @i
    A=M
    M=D
    @i
    D=M
    M=M+1
    @KBD
    D=A-D
    @KBD
    D=M
    @color
    D=M+D
    @INIT
    D;JLE
    @CHANGE
    0;JMP



