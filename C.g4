grammar C;
Type: ('int' | 'char'| 'void') ('*' | Indexer)?;
Int: [0-9]+;
ID: [a-zA-Z][a-zA-Z0-9]*;
Indexer: '[' Int ']';
WS: [ \t\r\n]+ -> skip;

BinOp: '+'
    | '-'
    | '*'
    | '/'
    | '%'
    | '='
    | '+='
    | '-='
    | '*='
    | '/='
    | '%='
    | '|='
    | '&='
    | '^='
    | '=='
    | '!='
    | '<'
    | '>'
    | '<='
    | '>='
    | '&&'
    | '||'
    | '|'
    | '&'
    | '^';


library: function* EOF;
function: Type ID '(' params ')' compound_statement;

params: | param (',' param)*;
param: Type ID;

statement: compound_statement
    | conditional_statement
    | loop_statement
    | return_statement
    | break_statement
    | continue_statement
    | variable_definition
    | expression_statement;

compound_statement: '{' statement* '}';
conditional_statement: 'if' '(' expression ')' compound_statement;
loop_statement: ('while' '(' expression ')' compound_statement)
    | ('for' '(' variable_definition expression ';' expression ')' compound_statement);
return_statement: 'return' expression ';';
break_statement: 'break' ';';
continue_statement: 'continue' ';';
variable_definition: Type ID ('=' expression)? ';';
expression_statement: expression ';';

expression: ('(' expression ')')
    | literal_expression
    | indexing_expression
    | function_call_expression
    | binary_expression
    | unary_expression;
//    | ternary_expression;


literal_expression: ID | Int;
indexing_expression: ID '[' expression ']';
function_call_expression: ID '(' (() | (expression (',' expression)*)) ')';
binary_expression: literal_expression BinOp expression;
unary_expression: (('&' | '*' | '-' | '!' | '~' | '--' | '++') expression)
    | (ID ('++' | '--'));
ternary_expression: expression '?' expression ':' expression;
