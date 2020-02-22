// Define a grammar called Hello
grammar Hello;                          // defines how the output code will be named
prog : assignment* EOF;                 // accept zero or more assignment items followed by EOF
assignment : Type ID '=' expr ';' ;       // match type followed by an identifier, then an '=' , an expression and ending with a ';'
expr : val expr2 ;                      // match expression as a value followed by an expr2
val : (ID | Int| Float);                       // match values
expr2 : ( | (opp (val | val expr2)));   // match second part of an expression [val (this part wtih the opperation and stuff)]
opp: '-' | '+' | '/' | '*';             // match opperations
Type: 'int' | 'float' | 'string' | 'double';    // match value types
Int : [0-9]+ ;                      // match integers
Float: [0-9]* '.' [0-9]+;
ID : [a-z]+ ;                       // match lower-case identifiers
WS : [ \t\r\n]+ -> skip ;           // skip spaces, tabs, newlines
