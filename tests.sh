#!/bin/bash

INPUT="Default"
OUTPUT=0

runtest()
{
  echo "Run test ${INPUT}"
  python3 Source/main.py -i ${INPUT} -llvm main.ll
  confirm
  return
}


runtestprop()
{
  echo "Run test w/ prop ${INPUT}"
  python3 Source/main.py -i ${INPUT} -llvm main.ll -prop
  confirm
  return
}


confirm()
{
  echo "==============================================="
  clang main.ll -o main
  ./main
  echo "==============================================="
  if [ $? -eq ${OUTPUT} ]
    then
      echo "Test successvol."
      echo "==============================================="
      return
  fi
    echo "Test failed."
    echo "==============================================="
    return
}


# Test section

INPUT="Test/simple_assignments.txt"
OUTPUT=0
runtest
runtestprop

INPUT="Test/pointers.c"
OUTPUT=0
runtest
runtestprop

INPUT="Test/equality_opperators.txt"
OUTPUT=0
runtest
runtestprop
