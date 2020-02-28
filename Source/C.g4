grammar C;

Void: 'void';
If: 'if';
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

EQUALS: '=';
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

Type: ('int' | 'char') (STAR | Indexer)?;
Int: [0-9]+;
ID: [a-zA-Z][a-zA-Z0-9]*;
Indexer: '[' Int ']';
WS: [ \t\r\n]+ -> skip;


library: (function
    | expression_statement
    | variable_definition)* EOF;

function: (Type | Void) ID LB (params)? RB compound_statement;

params: param (COMMA param)*;
param: Type ID;

statement: compound_statement
    | conditional_statement
    | loop_statement
    | return_statement
    | break_statement
    | continue_statement
    | variable_definition
    | expression_statement;

compound_statement: LCB statement* RCB;
conditional_statement: If LB expression RB statement;
loop_statement: (While LB expression RB statement)
    | (For LB variable_definition expression TERMINUS expression RB statement);
return_statement: Return expression? TERMINUS;
break_statement: Break TERMINUS;
continue_statement: Continue TERMINUS;
variable_definition: Type ID (EQUALS expression)? TERMINUS;
expression_statement: expression TERMINUS;

expression: ternary_expression;


negative: MINUS expression;
positive: PLUS expression;
inverse: EXCLAMANTION expression;
increment: (INCREMENT ID) | (ID INCREMENT);
decrement: (DECREMENT ID) | (ID DECREMENT);
indexing_expression: ID LSB expression RSB;
function_call_expression: ID LB ((expression (COMMA expression)*))? RB;
equality_expression: ID (EQUALS | PLUSEQ | MINUSEQ | STAREQ | DIVEQ | MODULOEQ | BINOREQ | BINANDEQ | BINXOREQ) expression;


ternary_expression: conditional_expression (QUESTION conditional_expression COLON conditional_expression)?;
conditional_expression: additional_expression ((EQ | NEQ | LT | LTE | GT | GTE | AND | BINAND | OR | BINOR) additional_expression)*;
additional_expression: multiplicational_expression ((PLUS | MINUS) multiplicational_expression)*;
multiplicational_expression: unary_expression ((STAR | DIV | MODULO) unary_expression)*;
unary_expression: bracket_expression
    | inverse
    | negative
    | positive
    | increment
    | decrement
    | indexing_expression
    | function_call_expression
    | equality_expression;

bracket_expression: literal_expression | (LB expression RB);
literal_expression: ID | Int;

