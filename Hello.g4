// Define a grammar called Hello
grammar Hello;                      // defines how the output code will be named
prog : assignment* EOF;             // accept zero or more hello items followed by EOF
assignment : tt ID '=' expr ';' ;  // match keyword hello followed by an identifier
expr : val expr2 ;
val : (ID | Int);
expr2 : ( | (opp (val | val expr2)));
opp: '-' | '+' | '/' | '*';
tt: 'int' | 'float' | 'string' | 'double';
Int : [0-9]+ ;
ID : [a-z]+ ;                       // match lower-case identifiers
WS : [ \t\r\n]+ -> skip ;           // skip spaces, tabs, newlines
