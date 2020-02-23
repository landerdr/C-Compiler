// Define a grammar called Hello
grammar Hello;                          // defines how the output code will be named
prog : assignment* EOF;                 // accept zero or more assignment items followed by EOF
//assignment : Type ID '=' expr ';' ;       // match type followed by an identifier, then an '=' , an expression and ending with a ';'
assignment : PLUS?  expr ';' ;
//expr : expr opp expr | '('expr')' | val;                      // match expression as a value followed by an expr2

expr:  add_expr ((AND | OR) add_expr)*;
add_expr: mult_expr ((PLUS | MINUS) mult_expr)*;
mult_expr:  atom ((STAR | SLASH ) atom)* ;

atom: val | LB PLUS?  expr RB ;

val : (MINUS)? (ID | Int| Float);           // match values

MINUS : '-';
PLUS : '+';

STAR : '*';
SLASH: '/';

AND : '&&' | '&';
OR : '||' | '|';

LB : '(';
RB : ')';

INCREMENT: PLUS PLUS;
DECREMENT: MINUS MINUS;

Type: 'int' | 'float' | 'string' | 'double';    // match value types
Int : [0-9]+ ;                      // match integers
Float: [0-9]* '.' [0-9]+;
ID : [a-z]+ ;                       // match lower-case identifiers
WS : [ \t\r\n]+ -> skip ;           // skip spaces, tabs, newlines
