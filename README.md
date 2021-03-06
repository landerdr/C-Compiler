# C-Compiler
![Python application](https://github.com/landerdr/C-Compiler/workflows/Python%20application/badge.svg)

Custom C _-ish_ compiler for compilers course.
[Online generator for reference](http://ellcc.org/demo/index.cgi)

Reference is gnu gcc compiler with flags `-ansi` and `-pedantic`.

## Project structure
`gen/`:
This folder contains all antlr4 generated files.

`Source/`:
Contains all source files for the compiler:
- `Source/main.py`:
Parses cli input and controls compiler.
- `Source/AntlrListener.py`:
Custom implementation of the antlr Listener to create the AST.
- `Source/AST.py`:
Implementation of our AST tree structure and nodes.
- `Source/TypeTable.py`:
Implementation of our symbol table.
- `Source/Types.py`:
Custom classes for types.

`Test/`:
Contains all test input files.

## Features
#### Project 1
- [x] (mandatory) Binary operations `+`, `-`, `*`, and `/`
- [x] (mandatory) Binary operations `>`, `<`, and `==`
- [x] (mandatory) Unary operators `+` and `-`
- [x] (mandatory) Brackets to overwrite the order of operations
- [x] (optional) Binary operator `%`
- [x] (optional) Comparison operators `>=` ,`<=` , and `!=`
- [x] (optional) Logical operators `&&`, `||`, and `!`
- [x] (mandatory) AST
- [x] (mandatory) Dot language representation
- [x] (optional) Constant folding

#### Project 2
- [x] (mandatory) Types:
    - [x] char
    - [x] int
    - [x] float
    - [x] pointer types (not yet pointer to pointer)
- [x] (mandatory) Reserved words `const`
- [x] (mandatory) Variables
    - [x] variable declarations
    - [x] variable definitions
    - [x] assignment statements
    - [x] identifiers appearing in expressions
- [x] (optional) Identifier Operations 
    - [x] unary operator `++` 
    - [x] unary operator `--`
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

#### Project 4
- [ ] (mandatory) Reserved words
    - [x] (mandatory) `if`, `else`, and `while`
    - [x] (mandatory) `for`
    - [x] (mandatory) `break`
    - [x] (mandatory) `continue`
    - [ ] (optional) `switch`, `case`, and `default`
- [x] (mandatory) Scopes

#### Project 5
- [x] (mandatory) Reserved words
    - [x] (mandatory) `return`
    - [x] (mandatory) `void`
- [x] (mandatory) Scopes
- [x] (mandatory) Local and global variables
- [ ] (mandatory) Functions
    - [x] (mandatory) Function calls
    - [x] (mandatory) Function definitions
    - [x] (mandatory) Forward declarations
    - [ ] (optional) Check whether all paths in a function body end with a return statement
- [x] (mandatory) Unreachable code removal
    - [ ] (optional) Do not generate code for variables that are not used
    - [ ] (optional) Do not generate code for conditionals that are never true

#### Project 6
- [ ] (mandatory) Arrays
    - [x] (mandatory) definition
    - [x] (mandatory) assignment
    - [x] (mandatory) indexing
    - [ ] (optional) multi-dimensional arrays
    - [ ] (optional) assignments of complete arrays or array rows in case of multi-dimensional arrays
    - [ ] (optional) dynamic arrays
- [x] (mandatory) Import
    - [x] `import <stdio.h>`
    - [x] `int printf(char *format, ...)` with format `%[width][code]` and codes `d`, `i`, `s` and `c`.
    - [x] `int scanf(const char*format, ...)` same as above

## Extra features
- [x] Assignment operators
    - [x] `+=`
    - [x] `-=`
    - [x] `*=`
    - [x] `/=`
    - [x] `%=`

#### Supported in CFG but not (completely) in LLVM yet
- [x] multidimensional Arrays
- [x] ternary operators

## Requirements, build process & testing
Requirements:
- Python3
- antlr4-python3-runtime (v4.8)
- antlr4

Basic run command:

    > python3 Source/main.py -i <INPUT> -llvm <LLVM OUTPUT>

Compiler options:
- `-i <INPUT>`: indicates input file
- `-dot <DOT OUTPUT>`: generates AST representation in dot language.
- `-prop`: enables constant propagation
- `-llvm <LLVM OUTPUT>`: generates llvm to output file
- `-mips <MIPS OUTPUT>`: generates mips to output file

Generate antlr files:
_ONLY IF YOU WANT TO REGEN THE ANTLR FILES_

    > ./build.sh

Tests:

    > ./tests.sh
    
