#!/usr/bin/env bash

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
  echo "Run test prop ${INPUT}"
  python3 Source/main.py -i ${INPUT} -llvm main.ll -prop
  confirm
  return
}


confirm()
{
  clang main.ll -o main
  ./main
  if [ $? -eq ${OUTPUT} ]
    then
      echo "Test successvol."
      return
  fi
    echo "Test failed."
    return
}


# Test section

INPUT="Source/Test/simple_assignments.txt"
OUTPUT=0
runtest
runtestprop

