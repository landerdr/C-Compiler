# C-Compiler
Custom C compiler for compilers course

Run basic antrl: 

    > java -Xmx500M -cp java/antlr-4.8-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 Hello.g4  
    > python3 main.py  -i <INPUT> --dot <DOT_FILE_OUTEPUT> --llvm <LLVM OUTPUT>
  
Run clang:
    
    > clang main.c -S -emit-llvm -o main.ll
    > clang main.ll -o main
    > ./main