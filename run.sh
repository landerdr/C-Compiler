
python3 Source/main.py -i Source/Test/$1 -llvm Source/Test/main2.ll -dot Source/Test/out.dot -prop
clang Source/Test/main2.ll -o Source/Test/main
./Source/Test/main
echo 'returned value:'
echo $?