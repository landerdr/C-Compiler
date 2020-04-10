grammar C;

Void: 'void';
If: 'if';
Else: 'else';
While: 'while';
For: 'for';
Do: 'do';
Return: 'return';
Break: 'break';
Continue: 'continue';
Include: '#include';

PLUS: '+';
INCREMENT: '++';
MINUS: '-';
DECREMENT: '--';
STAR: '*';
DIV: '/';
MODULO: '%';

ASSIGNMENT: '=';
EQ: '==';
NEQ: '!=';
GT: '>';
LT: '<';
GTE: '>=';
LTE: '<=';
PLUSEQ: '+=';
MINUSEQ: '-=';
STAREQ: '*=';
MODULOEQ: '%=';
DIVEQ: '/=';
BINOREQ: '|=';
BINANDEQ: '&=';
BINXOREQ: '^=';

EXCLAMANTION: '!';
QUESTION: '?';
BINAND: '&';
BINOR: '|';
BINXOR: '^';
AND: '&&';
OR: '||';

LB: '(';
RB: ')';
LCB: '{';
RCB: '}';
LSB: '[';
RSB: ']';
COMMA: ',';
TERMINUS: ';';
COLON: ':';

Type: ('int' | 'char' | 'float');
CONST: 'const';
Int: [0-9]+;
String: '"' ~('\r' | '\n' | '"')* '"' ;
Float: [0-9]+'.'[0-9]+;
Char: '\''.'\'';
HeaderFile:  [_a-zA-Z][_a-zA-Z0-9]* '.h';
ID: [_a-zA-Z][_a-zA-Z0-9]*;
WS: [ \t\r\n]+ -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;

include: Include LT HeaderFile GT;

library: (include | function
    | expression_statement
    | variable_definition)* EOF;

value_type: CONST? Type STAR?;

// Functions
function: (value_type | Void) ID LB (params)? RB (compound_statement) | (TERMINUS);
params: param (COMMA param)*;
param: value_type ID (LSB Int RSB)?;

// Statements
statement: compound_statement
    | conditional_statement
    | loop_statement
    | return_statement
    | break_statement
    | continue_statement
    | variable_definition
    | expression_statement;

compound_statement: LCB statement* RCB;
conditional_statement: If LB expression RB statement (Else statement)?;
loop_statement: (While LB expression RB statement)
    | (For LB variable_definition expression TERMINUS expression RB statement)
    | (Do statement While LB expression RB TERMINUS);
return_statement: Return expression? TERMINUS;
break_statement: Break TERMINUS;
continue_statement: Continue TERMINUS;
variable_definition: value_type ID (LSB Int? RSB)* (ASSIGNMENT expression)? TERMINUS;
expression_statement: expression TERMINUS;

// Expressions
expression: ternary_expression;

// Ternary expression
ternary_expression: logical_or_expression (QUESTION logical_or_expression COLON logical_or_expression)?;

// Conditional expressions
logical_or_expression: logical_and_expression (log_or logical_and_expression)*;
log_or: OR;
logical_and_expression: bitwise_or_expression (log_and bitwise_or_expression)*;
log_and: AND;
bitwise_or_expression: bitwise_xor_expression (binor bitwise_xor_expression)*;
binor: BINOR;
bitwise_xor_expression: bitwise_and_expression (binxor bitwise_and_expression)*;
binxor: BINXOR;
bitwise_and_expression: relational_equality_expression (binand relational_equality_expression)*;
binand: BINAND;
relational_equality_expression: relational_comparison_expression (log_eq relational_comparison_expression)*;
log_eq: (EQ | NEQ);
relational_comparison_expression: additional_expression (rel_com additional_expression)*;
rel_com: (LT | GT | LTE | GTE);

// Addition
additional_expression: multiplication_expression (addopp multiplication_expression)*;
//additional_expression: multiplicational_expression addtemp;
//addtemp: (addopp multiplicational_expression addtemp) | ;
addopp: (PLUS | MINUS);

// Multiplication
multiplication_expression: unary_expression (multopp unary_expression)*;
//multiplicational_expression: unary_expression multtemp;
//multtemp: (multopp unary_expression multtemp) | ;
multopp: (STAR | DIV | MODULO);

// Unary
unary_expression: bracket_expression
    | inverse
    | negative
    | positive
    | pre_xcrement
    | post_xcrement
    | indexing_expression
    | function_call_expression
    | equality_expression
    | dereference
    | reference
    | list_expression;


// Unary expressions
// Signs
negative: MINUS expression;
positive: PLUS expression;
// Logical inverse
inverse: EXCLAMANTION expression;
// Increment/decrement
pre_xcrement: (INCREMENT left_value) | (DECREMENT left_value);
post_xcrement: (left_value INCREMENT) | (left_value DECREMENT);
// Indexing/fucntions
indexing_expression: (left_value | function_call_expression) (LSB expression RSB)+;
function_call_expression: ID LB ((expression (COMMA expression)*))? RB;
// Assignment
equality_expression: left_value equality_symbol expression;
equality_symbol: (ASSIGNMENT | PLUSEQ | MINUSEQ | STAREQ | DIVEQ | MODULOEQ | BINOREQ | BINANDEQ | BINXOREQ);
// Brackets
bracket_expression: literal_expression | (LB expression RB);
// Pointer operations
dereference: (STAR left_value) | (STAR LB expression RB);
reference: BINAND left_value;
// Left value
left_value: ID | dereference | l_indexing_expression;
l_indexing_expression: ID (LSB expression RSB)+;
// Initialiser Lists
list_expression: LCB literal_expression (COMMA expression)* RCB;

// Literal
literal_expression: ID | Int | Char | Float | String;

