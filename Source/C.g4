grammar C;
Type: ('int' | 'char') ('*' | Indexer)?;
Int: [0-9]+;
ID: [a-zA-Z][a-zA-Z0-9]*;
Indexer: '[' Int ']';
WS: [ \t\r\n]+ -> skip;


library: function* EOF;
function: (Type | 'void') ID '(' (params)? ')' compound_statement;

params: param (',' param)*;
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
conditional_statement: 'if' '(' expression ')' statement;
loop_statement: ('while' '(' expression ')' statement)
    | ('for' '(' variable_definition expression ';' expression ')' statement);
return_statement: 'return' expression ';';
break_statement: 'break' ';';
continue_statement: 'continue' ';';
variable_definition: Type ID ('=' expression)? ';';
expression_statement: expression ';';

expression: increment
    | decrement
    | indexing_expression
    | function_call_expression
    | equality_expression
    | ternary_expression;


negative: '-' expression;
inverse: '!' expression;
increment: ('++' ID) | (ID '++');
decrement: ('--' ID) | (ID '--');
indexing_expression: ID '[' expression ']';
function_call_expression: ID '(' ((expression (',' expression)*))? ')';
equality_expression: ID ('=' | '+=' | '-=' | '*=' | '/=' | '%=' | '|=' | '&=' | '^=') expression;


ternary_expression: conditional_expression ('?' conditional_expression ':' conditional_expression)?;
conditional_expression: additional_expression (('==' | '!=' | '<' | '<=' | '>' | '>=' | '&&' | '&' | '||' | '|') additional_expression)*;
additional_expression: multiplicational_expression (('+' | '-') multiplicational_expression)*;
multiplicational_expression: unary_expression (('*' | '/' | '%') unary_expression)*;
unary_expression: bracket_expression | inverse | negative;

bracket_expression: literal_expression | ('(' expression ')');
literal_expression: ID | Int;

