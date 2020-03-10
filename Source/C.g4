grammar C;

Void: 'void';
If: 'if';
Else: 'else';
While: 'while';
For: 'for';
Return: 'return';
Break: 'break';
Continue: 'continue';

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
Float: [0-9]+'.'[0-9]+;
Char: '\''.'\'';
ID: [_a-zA-Z][_a-zA-Z0-9]*;
WS: [ \t\r\n]+ -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;


library: (function
    | expression_statement
    | variable_definition)* EOF;

value_type: CONST? Type (STAR | LSB Int RSB)?;

// Functions
function: (value_type | Void) ID LB (params)? RB compound_statement;
params: param (COMMA param)*;
param: value_type ID;

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
conditional_statement: If LB expression RB statement (Else LB expression RB statement)?;
loop_statement: (While LB expression RB statement)
    | (For LB variable_definition expression TERMINUS expression RB statement);
return_statement: Return expression? TERMINUS;
break_statement: Break TERMINUS;
continue_statement: Continue TERMINUS;
variable_definition: value_type ID (ASSIGNMENT expression)? TERMINUS;
expression_statement: expression TERMINUS;

// Expressions
expression: ternary_expression;

// Ternary expression
ternary_expression: logical_or_expression (QUESTION logical_or_expression COLON logical_or_expression)?;

// Conditional expressions
logical_or_expression: logical_and_expression (OR logical_and_expression)*;
logical_and_expression: bitwise_or_expression (AND bitwise_or_expression)*;
bitwise_or_expression: bitwise_xor_expression (BINOR bitwise_xor_expression)*;
bitwise_xor_expression: bitwise_and_expression (BINXOR bitwise_and_expression)*;
bitwise_and_expression: relational_equality_expression (BINAND relational_equality_expression)*;
relational_equality_expression: relational_comparison_expression ((EQ | NEQ) relational_comparison_expression)*;
relational_comparison_expression: additional_expression ((LT | GT | LTE | GTE) additional_expression)*;

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
    | increment
    | decrement
    | indexing_expression
    | function_call_expression
    | equality_expression
    | dereference
    | reference;

// Unary expressions
// Signs
negative: MINUS expression;
positive: PLUS expression;
// Logical inverse
inverse: EXCLAMANTION expression;
// Increment/decrement
increment: (INCREMENT left_value) | (left_value INCREMENT);
decrement: (DECREMENT left_value) | (left_value DECREMENT);
// Indexing/fucntions
indexing_expression: (left_value | function_call_expression) (LSB expression RSB)+;
function_call_expression: ID LB ((expression (COMMA expression)*))? RB;
// Assignment
equality_expression: left_value equality_symbol expression;
equality_symbol: (ASSIGNMENT | PLUSEQ | MINUSEQ | STAREQ | DIVEQ | MODULOEQ | BINOREQ | BINANDEQ | BINXOREQ);
// Brackets
bracket_expression: literal_expression | (LB expression RB);
// Pointer operations
dereference: (STAR ID) | (STAR LB expression RB);
reference: BINAND ID;
// Left value
left_value: ID | dereference | l_indexing_expression;
l_indexing_expression: ID (LSB expression RSB)+;

// Literal
literal_expression: ID | Int | Char | Float;

