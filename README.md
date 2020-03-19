# C-Compiler
Custom C compiler for compilers course
[Online generator for reference](http://ellcc.org/demo/index.cgi)

Run basic antrl: 

    > java -Xmx500M -cp java/antlr-4.8-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 Hello.g4  
    > python3 main.py  -i <INPUT> --dot <DOT_FILE_OUTEPUT> -llvm <LLVM OUTPUT>
  
Run clang:
    
    > clang main.c -S -emit-llvm -o main.ll
    > clang main.ll -o main
    > ./main
    
## Features
#### Project 1
- [x] (mandatory) Binary operations +, -, *, and /
- [x] (mandatory) Binary operations >, <, and ==
- [x] (mandatory) Unary operators + and -
- [x] (mandatory) Brackets to overwrite the order of operations
- [x] (optional) Binary operator %
- [x] (optional) Comparison operators >= ,<= , and !=
- [x] (optional) Logical operators &&, ||, and !
- [x] (mandatory) AST
- [x] (mandatory) Dot language representation
- [x] (optional) Constant folding

#### Project 2
- [x] (mandatory) Types:
    - [x] char
    - [x] int
    - [x] float
    - [x] pointer types
- [x] (mandatory) Reserved words (const)
- [x] (mandatory) Variables
    - [x] variable declarations
    - [x] variable definitions
    - [x] assignment statements
    - [x] identifiers appearing in expressions
- [x] (optional) Identifier Operations 
    - [x] unary operator ++ 
    - [x] unary operator --
- [ ] (optional) Conversions
    - [x] Warning implicit casts
    - [x] Implicit casts
    - [ ] Explicit casts
- [x] (optional) Constant propagation
- [x] (mandatory) Syntax Errors
- [x] (mandatory) Semantic Errors
    - [x] Use of an undefined or uninitialized variable
    - [x] Redeclaration or redefinition of an existing variable
    - [x] Operations or assignments of incompatible types
    - [x] Assignment to an rvalue
    - [x] Assignment to a const variable

#### Project 3
- [ ] Comments
    - [x] (mandatory) Comment support in language
    - [ ] (optional) Put comments in generated LLVM code
    - [ ] (optional) Put original line in generated LLVM code
- [x] (mandatory) Printf
    - [x] Printf char
    - [x] Printf int
    - [x] Printf float
    - [x] Printf pointer
- [x] (mandatory) Code generation LLVM

## Extra features
- [x] Scope support in symbol table
- [x] Assignment operators
    - [x] +=
    - [x] -=
    - [x] *=
    - [x] /=
    - [x] %=

#### Supported in CFG but not (completely) in LLVM yet
- [x] (multidimensional) Arrays
- [x] Functions
- [x] return statement
- [x] Loops
    - [x] For
    - [x] While
- [x] continue
- [x] break
- [x] if / else statements
- [x] ternary operators
