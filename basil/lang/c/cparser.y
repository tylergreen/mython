%{
/* ______________________________________________________________________
   cparser.y
   $Id: cparser.y,v 1.2 2003/07/02 21:59:38 jriehl Exp $
   ______________________________________________________________________ */

/* This Yacc grammar is based on the grammar by Jutta Degener (1995),
 * http://www.lysator.liu.se/c/ANSI-C-grammar-y.html, which
 * was derived from a Yacc grammar of Jeff Lee.
*/

#include "cparserutils.h"
#include "namespace.h"

#define YYSTYPE CParserNode *
#define YYDEBUG 1

%}

%token IDENTIFIER CONSTANT STRING_LITERAL SIZEOF
%token PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token XOR_ASSIGN OR_ASSIGN TYPE_NAME

%token TYPEDEF EXTERN STATIC AUTO REGISTER
%token CHAR SHORT INT LONG SIGNED UNSIGNED FLOAT DOUBLE CONST VOLATILE VOID
%token STRUCT UNION ENUM ELLIPSIS

%token CASE DEFAULT IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN

%start translation_unit
%%


/* ______________________________________________________________________ */

primary_expression
        : IDENTIFIER
        | CONSTANT
        | STRING_LITERAL
        | '(' expression ')' { $$ = $2; }
        ;

/* ______________________________________________________________________ */

postfix_expression
        : primary_expression
        | postfix_expression '[' expression ']'
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | postfix_expression '(' ')'
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | postfix_expression '(' argument_expression_list ')'
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | postfix_expression '.' IDENTIFIER
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | postfix_expression PTR_OP IDENTIFIER
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | postfix_expression INC_OP
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | postfix_expression DEC_OP
{
  $$ = CParserNewNode(POSTFIX_EXPRESSION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

argument_expression_list
        : assignment_expression
        | argument_expression_list ',' assignment_expression
{
  $$ = CParserNewNode(ARGUMENT_EXPRESSION_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

unary_expression
        : postfix_expression
        | INC_OP unary_expression
{
  $$ = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | DEC_OP unary_expression
{
  $$ = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | unary_operator cast_expression
{
  $$ = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | SIZEOF unary_expression
{
  $$ = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | SIZEOF '(' type_name ')'
{
  $$ = CParserNewNode(UNARY_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

unary_operator
        : '&'
        | '*'
        | '+'
        | '-'
        | '~'
        | '!'
        ;

/* ______________________________________________________________________ */

cast_expression
        : unary_expression
        | '(' type_name ')' cast_expression
{
  $$ = CParserNewNode(CAST_EXPRESSION, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);  
}
        ;

/* ______________________________________________________________________ */

multiplicative_expression
        : cast_expression
        | multiplicative_expression '*' cast_expression
{
  $$ = CParserNewNode(MULTIPLICATIVE_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | multiplicative_expression '/' cast_expression
{
  $$ = CParserNewNode(MULTIPLICATIVE_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | multiplicative_expression '%' cast_expression
{
  $$ = CParserNewNode(MULTIPLICATIVE_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

additive_expression
        : multiplicative_expression
        | additive_expression '+' multiplicative_expression
{
  $$ = CParserNewNode(ADDITIVE_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | additive_expression '-' multiplicative_expression
{
  $$ = CParserNewNode(ADDITIVE_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

shift_expression
        : additive_expression
        | shift_expression LEFT_OP additive_expression
{
  $$ = CParserNewNode(SHIFT_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | shift_expression RIGHT_OP additive_expression
{
  $$ = CParserNewNode(SHIFT_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

relational_expression
        : shift_expression
        | relational_expression '<' shift_expression
{
  $$ = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | relational_expression '>' shift_expression
{
  $$ = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | relational_expression LE_OP shift_expression
{
  $$ = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | relational_expression GE_OP shift_expression
{
  $$ = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

equality_expression
        : relational_expression
        | equality_expression EQ_OP relational_expression
{
  $$ = CParserNewNode(EQUALITY_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | equality_expression NE_OP relational_expression
{
  $$ = CParserNewNode(EQUALITY_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

and_expression
        : equality_expression
        | and_expression '&' equality_expression
{
  $$ = CParserNewNode(AND_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

exclusive_or_expression
        : and_expression
        | exclusive_or_expression '^' and_expression
{
  $$ = CParserNewNode(XOR_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

inclusive_or_expression
        : exclusive_or_expression
        | inclusive_or_expression '|' exclusive_or_expression
{
  $$ = CParserNewNode(OR_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

logical_and_expression
        : inclusive_or_expression
        | logical_and_expression AND_OP inclusive_or_expression
{
  $$ = CParserNewNode(LOGICAL_AND_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

logical_or_expression
        : logical_and_expression
        | logical_or_expression OR_OP logical_and_expression
{
  $$ = CParserNewNode(LOGICAL_OR_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

conditional_expression
        : logical_or_expression
        | logical_or_expression '?' expression ':' conditional_expression
{
  $$ = CParserNewNode(CONDITIONAL_EXPRESSION, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        ;

/* ______________________________________________________________________ */

assignment_expression
        : conditional_expression
        | unary_expression assignment_operator assignment_expression
{
  $$ = CParserNewNode(ASSIGNMENT_EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

assignment_operator
        : '='
        | MUL_ASSIGN
        | DIV_ASSIGN
        | MOD_ASSIGN
        | ADD_ASSIGN
        | SUB_ASSIGN
        | LEFT_ASSIGN
        | RIGHT_ASSIGN
        | AND_ASSIGN
        | XOR_ASSIGN
        | OR_ASSIGN
        ;

/* ______________________________________________________________________ */

expression
        : assignment_expression
        | expression ',' assignment_expression
{
  $$ = CParserNewNode(EXPRESSION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

constant_expression
        : conditional_expression
        ;

/* ______________________________________________________________________ */

declaration
        : declaration_specifiers ';'
{
  $$ = CParserNewNode(DECLARATION, 1);
  CParserSetChild($$, 0, $1);
}
        | declaration_specifiers init_declarator_list ';'
{
  $$ = CParserNewNode(DECLARATION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserHandleDeclaration($$);
}
        ;

/* ______________________________________________________________________ */

declaration_specifiers
        : storage_class_specifier
{
  $$ = CParserNewNode(DECLARATION_SPECIFIERS, 1);
  CParserSetChild($$, 0, $1);
}
        | storage_class_specifier declaration_specifiers
{
  $$ = CParserNewNode(DECLARATION_SPECIFIERS, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | type_specifier
{
  $$ = CParserNewNode(DECLARATION_SPECIFIERS, 1);
  CParserSetChild($$, 0, $1);
}
        | type_specifier declaration_specifiers
{
  $$ = CParserNewNode(DECLARATION_SPECIFIERS, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | type_qualifier
{
  $$ = CParserNewNode(DECLARATION_SPECIFIERS, 1);
  CParserSetChild($$, 0, $1);
}
        | type_qualifier declaration_specifiers
{
  $$ = CParserNewNode(DECLARATION_SPECIFIERS, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

init_declarator_list
        : init_declarator
        | init_declarator_list ',' init_declarator
{
  $$ = CParserNewNode(INIT_DECLARATOR_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

init_declarator
        : declarator
        | declarator '=' initializer
{
  $$ = CParserNewNode(INIT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

storage_class_specifier
        : TYPEDEF
        | EXTERN
        | STATIC
        | AUTO
        | REGISTER
        ;

/* ______________________________________________________________________ */

type_specifier
        : VOID
        | CHAR
        | SHORT
        | INT
        | LONG
        | FLOAT
        | DOUBLE
        | SIGNED
        | UNSIGNED
        | struct_or_union_specifier
        | enum_specifier
        | TYPE_NAME
        ;

/* ______________________________________________________________________ */

struct_or_union_specifier
        : struct_or_union identifier_or_typename '{' struct_declaration_list '}'
{
  $$ = CParserNewNode(SU_SPECIFIER, 5);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
  $2->tokType = TT_IDENTIFIER;
}
        | struct_or_union '{' struct_declaration_list '}'
{
  $$ = CParserNewNode(SU_SPECIFIER, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | struct_or_union identifier_or_typename
{
  $$ = CParserNewNode(SU_SPECIFIER, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  $2->tokType = TT_IDENTIFIER;
}
        ;

/* ______________________________________________________________________ */

struct_or_union
        : STRUCT
        | UNION
        ;

/* ______________________________________________________________________ */

struct_declaration_list
        : struct_declaration
        | struct_declaration_list struct_declaration
{
  $$ = CParserNewNode(STRUCT_DECLARATION_LIST, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

struct_declaration
        : specifier_qualifier_list struct_declarator_list ';'
{
  $$ = CParserNewNode(STRUCT_DECLARATION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

specifier_qualifier_list
        : type_specifier specifier_qualifier_list
{
  $$ = CParserNewNode(SPECIFIER_QUALIFIER_LIST, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | type_specifier
        | type_qualifier specifier_qualifier_list
{
  $$ = CParserNewNode(SPECIFIER_QUALIFIER_LIST, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | type_qualifier
        ;

/* ______________________________________________________________________ */

struct_declarator_list
        : struct_declarator
        | struct_declarator_list ',' struct_declarator
{
  $$ = CParserNewNode(STRUCT_DECLARATOR_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

struct_declarator
        : declarator
        | ':' constant_expression
{
  $$ = CParserNewNode(STRUCT_DECLARATOR, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | declarator ':' constant_expression
{
  $$ = CParserNewNode(STRUCT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

identifier_or_typename
        : IDENTIFIER
        | TYPE_NAME
        ;

enum_specifier
        : ENUM '{' enumerator_list '}'
{
  $$ = CParserNewNode(ENUM_SPECIFIER, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | ENUM identifier_or_typename '{' enumerator_list '}'
{
  $$ = CParserNewNode(ENUM_SPECIFIER, 5);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
  $2->tokType = TT_IDENTIFIER;
}
        | ENUM identifier_or_typename
{
  $$ = CParserNewNode(ENUM_SPECIFIER, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  $2->tokType = TT_IDENTIFIER;
}
        ;

/* ______________________________________________________________________ */

enumerator_list
        : enumerator
        | enumerator_list ',' enumerator
{
  $$ = CParserNewNode(ENUMERATOR_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

enumerator
        : IDENTIFIER
        | IDENTIFIER '=' constant_expression
{
  $$ = CParserNewNode(ENUMERATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

type_qualifier
        : CONST
        | VOLATILE
        ;

/* ______________________________________________________________________ */

declarator
        : pointer direct_declarator
{
  $$ = CParserNewNode(DECLARATOR, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | direct_declarator
        ;

/* ______________________________________________________________________ */

direct_declarator
        : IDENTIFIER
        | '(' declarator ')'
{
  $$ = CParserNewNode(DIRECT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | direct_declarator '[' constant_expression ']'
{
  $$ = CParserNewNode(DIRECT_DECLARATOR, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | direct_declarator '[' ']'
{
  $$ = CParserNewNode(DIRECT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | direct_declarator '(' parameter_type_list ')'
{
  $$ = CParserNewNode(DIRECT_DECLARATOR, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | direct_declarator '(' identifier_list ')'
{
  $$ = CParserNewNode(DIRECT_DECLARATOR, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | direct_declarator '(' ')'
{
  $$ = CParserNewNode(DIRECT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

pointer
        : '*'
        | '*' type_qualifier_list
{
  $$ = CParserNewNode(POINTER, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | '*' pointer
{
  $$ = CParserNewNode(POINTER, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | '*' type_qualifier_list pointer
{
  $$ = CParserNewNode(POINTER, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

type_qualifier_list
        : type_qualifier
        | type_qualifier_list type_qualifier
{
  $$ = CParserNewNode(TYPE_QUALIFIER_LIST, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;


/* ______________________________________________________________________ */

parameter_type_list
        : parameter_list
        | parameter_list ',' ELLIPSIS
{
  $$ = CParserNewNode(PARAMETER_TYPE_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

parameter_list
        : parameter_declaration
        | parameter_list ',' parameter_declaration
{
  $$ = CParserNewNode(PARAMETER_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

parameter_declaration
        : declaration_specifiers declarator
{
  $$ = CParserNewNode(PARAMETER_DECLARATION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | declaration_specifiers abstract_declarator
{
  $$ = CParserNewNode(PARAMETER_DECLARATION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | declaration_specifiers
        ;

/* ______________________________________________________________________ */

identifier_list
        : IDENTIFIER
        | identifier_list ',' IDENTIFIER
{
  $$ = CParserNewNode(IDENTIFIER_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

type_name
        : specifier_qualifier_list
        | specifier_qualifier_list abstract_declarator
{
  $$ = CParserNewNode(TYPE_NAME_TYPE, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

abstract_declarator
        : pointer
        | direct_abstract_declarator
        | pointer direct_abstract_declarator
{
  $$ = CParserNewNode(ABSTRACT_DECLARATOR, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

direct_abstract_declarator
        : '(' abstract_declarator ')'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | '[' ']'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | '[' constant_expression ']'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | direct_abstract_declarator '[' ']'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | direct_abstract_declarator '[' constant_expression ']'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | '(' ')'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | '(' parameter_type_list ')'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | direct_abstract_declarator '(' ')'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | direct_abstract_declarator '(' parameter_type_list ')'
{
  $$ = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        ;

/* ______________________________________________________________________ */

initializer
        : assignment_expression
        | '{' initializer_list '}'
{
  $$ = CParserNewNode(INITIALIZER, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | '{' initializer_list ',' '}'
{
  $$ = CParserNewNode(INITIALIZER, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        ;

/* ______________________________________________________________________ */

initializer_list
        : initializer
        | initializer_list ',' initializer
{
  $$ = CParserNewNode(INITIALIZER_LIST, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

statement
        : labeled_statement
        | compound_statement
        | expression_statement
        | selection_statement
        | iteration_statement
        | jump_statement
        ;

/* ______________________________________________________________________ */

labeled_statement
        : IDENTIFIER ':' statement
{
  $$ = CParserNewNode(LABELED_STATEMENT, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | CASE constant_expression ':' statement
{
  $$ = CParserNewNode(LABELED_STATEMENT, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | DEFAULT ':' statement
{
  $$ = CParserNewNode(LABELED_STATEMENT, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

compound_statement_start
        : '{'
{
  pushNamespace();
}
        ;

compound_statement
        : compound_statement_start '}'
{
  $$ = CParserNewNode(COMPOUND_STATEMENT, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  popNamespace();
}
        | compound_statement_start statement_list '}'
{
  $$ = CParserNewNode(COMPOUND_STATEMENT, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  popNamespace();
}
        | compound_statement_start declaration_list '}'
{
  $$ = CParserNewNode(COMPOUND_STATEMENT, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  popNamespace();
}
        | compound_statement_start declaration_list statement_list '}'
{
  $$ = CParserNewNode(COMPOUND_STATEMENT, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  popNamespace();
}
        ;

/* ______________________________________________________________________ */

declaration_list
        : declaration
{
  /* I don't usually do this, but this helps handlers disambiguate K&R
     style fucntion definitions alot. */
  $$ = CParserNewNode(DECLARATION_LIST, 1);
  CParserSetChild($$, 0, $1);
}
        | declaration_list declaration
{
  $$ = CParserNewNode(DECLARATION_LIST, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

statement_list
        : statement
        | statement_list statement
{
  $$ = CParserNewNode(STATEMENT_LIST, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

expression_statement
        : ';'
        | expression ';'
{
  $$ = CParserNewNode(EXPRESSION_STATEMENT, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

/* ______________________________________________________________________ */

selection_statement
        : IF '(' expression ')' statement
{
  $$ = CParserNewNode(SELECTION_STATEMENT, 5);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
}
        | IF '(' expression ')' statement ELSE statement
{
  $$ = CParserNewNode(SELECTION_STATEMENT, 7);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
  CParserSetChild($$, 5, $6);
  CParserSetChild($$, 6, $7);
}
        | SWITCH '(' expression ')' statement
{
  $$ = CParserNewNode(SELECTION_STATEMENT, 5);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
}
        ;

/* ______________________________________________________________________ */

iteration_statement
        : WHILE '(' expression ')' statement
{
  $$ = CParserNewNode(ITERATION_STATEMENT, 5);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
}
        | DO statement WHILE '(' expression ')' ';'
{
  $$ = CParserNewNode(ITERATION_STATEMENT, 7);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
  CParserSetChild($$, 5, $6);
  CParserSetChild($$, 6, $7);
}
        | FOR '(' expression_statement expression_statement ')' statement
{
  $$ = CParserNewNode(ITERATION_STATEMENT, 6);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
  CParserSetChild($$, 5, $6);
}
        | FOR '(' expression_statement expression_statement expression ')' statement
{
  $$ = CParserNewNode(ITERATION_STATEMENT, 7);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
  CParserSetChild($$, 4, $5);
  CParserSetChild($$, 5, $6);
  CParserSetChild($$, 6, $7);
}
        ;

/* ______________________________________________________________________ */

jump_statement
        : GOTO IDENTIFIER ';'
{
  $$ = CParserNewNode(JUMP_STATEMENT, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | CONTINUE ';'
{
  $$ = CParserNewNode(JUMP_STATEMENT, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | BREAK ';'
{
  $$ = CParserNewNode(JUMP_STATEMENT, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | RETURN ';'
{
  $$ = CParserNewNode(JUMP_STATEMENT, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        | RETURN expression ';'
{
  $$ = CParserNewNode(JUMP_STATEMENT, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        ;

/* ______________________________________________________________________ */

translation_unit
        : external_declaration
{
  $$ = $1;
  CParserSetRoot($1);
}
        | translation_unit external_declaration
{
  $$ = CParserNewNode(TRANSLATION_UNIT, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetRoot($$);
}
        ;

/* ______________________________________________________________________ */

external_declaration
        : function_definition
        | declaration
        ;

/* ______________________________________________________________________ */

function_definition
        : declaration_specifiers declarator declaration_list compound_statement
{
  $$ = CParserNewNode(FUNCTION_DEFINITION, 4);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
  CParserSetChild($$, 3, $4);
}
        | declaration_specifiers declarator compound_statement
{
  $$ = CParserNewNode(FUNCTION_DEFINITION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | declarator declaration_list compound_statement
{
  $$ = CParserNewNode(FUNCTION_DEFINITION, 3);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
  CParserSetChild($$, 2, $3);
}
        | declarator compound_statement
{
  $$ = CParserNewNode(FUNCTION_DEFINITION, 2);
  CParserSetChild($$, 0, $1);
  CParserSetChild($$, 1, $2);
}
        ;

%%
#include <stdio.h>

extern char cparsertext[];
extern int cparser_column;

int cparsererror (char * s)
{
        fflush(stdout);
        printf("\n%*s\n%*s\n", cparser_column, "^", cparser_column, s);
        return 0;
}
