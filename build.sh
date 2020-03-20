wget -nc "https://www.antlr.org/download/antlr-4.8-complete.jar"
java -Xmx500M -cp antlr-4.8-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 Source/C.g4 -o gen
cd gen/Source
mv * ../
cd ../
rmdir Source