# C-Compiler
Custom C _-ish_ compiler for compilers course.
[Online generator for reference](http://ellcc.org/demo/index.cgi)

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
    - [ ] (mandatory) `if`, `else`, and `while`
    – [ ] (mandatory) `for`
    – [ ] (mandatory) `break`
    – [ ] (mandatory) `continue`
    – [ ] (optional) `switch`, `case`, and `default`
- [ ] (mandatory) Scopes

## Extra features
- [x] Scope support in symbol table
- [x] Assignment operators
    - [x] `+=`
    - [x] `-=`
    - [x] `*=`
    - [x] `/=`
    - [x] `%=`

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

Generate antlr files:
_ONLY IF YOU WANT TO REGEN THE ANTLR FILES_

    > ./build.sh

Tests:

    > ./tests.sh
    