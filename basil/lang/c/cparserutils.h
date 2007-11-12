#ifndef __CPARSERUTILS_H__
#define __CPARSERUTILS_H__
/* ______________________________________________________________________
   cparserutils.h
   $Id: cparserutils.h,v 1.2 2003/07/02 21:59:38 jriehl Exp $
   ______________________________________________________________________ */

typedef enum {
  TOKEN_TYPE = 0,
  POSTFIX_EXPRESSION,
  ARGUMENT_EXPRESSION_LIST,
  UNARY_EXPRESSION,
  CAST_EXPRESSION,
  MULTIPLICATIVE_EXPRESSION,
  ADDITIVE_EXPRESSION,
  SHIFT_EXPRESSION,
  RELATIONAL_EXPRESSION,
  EQUALITY_EXPRESSION,
  AND_EXPRESSION,
  XOR_EXPRESSION,
  OR_EXPRESSION,
  LOGICAL_AND_EXPRESSION,
  LOGICAL_OR_EXPRESSION,
  CONDITIONAL_EXPRESSION,
  ASSIGNMENT_EXPRESSION,
  EXPRESSION,
  DECLARATION,
  DECLARATION_SPECIFIERS,
  INIT_DECLARATOR_LIST,
  INIT_DECLARATOR,
  SU_SPECIFIER,
  STRUCT_DECLARATION_LIST,
  STRUCT_DECLARATION,
  SPECIFIER_QUALIFIER_LIST,
  STRUCT_DECLARATOR_LIST,
  STRUCT_DECLARATOR,
  ENUM_SPECIFIER,
  ENUMERATOR_LIST,
  ENUMERATOR,
  DECLARATOR,
  DIRECT_DECLARATOR,
  POINTER,
  TYPE_QUALIFIER_LIST,
  PARAMETER_TYPE_LIST,
  PARAMETER_LIST,
  PARAMETER_DECLARATION,
  IDENTIFIER_LIST,
  TYPE_NAME_TYPE,
  ABSTRACT_DECLARATOR,
  DIRECT_ABSTRACT_DECLARATOR,
  INITIALIZER,
  INITIALIZER_LIST,
  LABELED_STATEMENT,
  COMPOUND_STATEMENT,
  DECLARATION_LIST,
  STATEMENT_LIST,
  EXPRESSION_STATEMENT,
  SELECTION_STATEMENT,
  ITERATION_STATEMENT,
  JUMP_STATEMENT,
  TRANSLATION_UNIT,
  FUNCTION_DEFINITION,
  MAX_NODE_TYPE_VAL
} NodeType;

typedef enum {
  TT_IDENTIFIER,
  TT_CONSTANT,
  TT_STRING_LITERAL,
  TT_SIZEOF,
  TT_PTR_OP,
  TT_INC_OP,
  TT_DEC_OP,
  TT_LEFT_OP,
  TT_RIGHT_OP,
  TT_LE_OP,
  TT_GE_OP,
  TT_EQ_OP,
  TT_NE_OP,
  TT_AND_OP,
  TT_OR_OP,
  TT_MUL_ASSIGN,
  TT_DIV_ASSIGN,
  TT_MOD_ASSIGN,
  TT_ADD_ASSIGN,
  TT_SUB_ASSIGN,
  TT_LEFT_ASSIGN,
  TT_RIGHT_ASSIGN,
  TT_AND_ASSIGN,
  TT_XOR_ASSIGN,
  TT_OR_ASSIGN,
  TT_TYPE_NAME,
  TT_TYPEDEF,
  TT_EXTERN,
  TT_STATIC,
  TT_AUTO,
  TT_REGISTER,
  TT_CHAR,
  TT_SHORT,
  TT_INT,
  TT_LONG,
  TT_SIGNED,
  TT_UNSIGNED,
  TT_FLOAT,
  TT_DOUBLE,
  TT_CONST,
  TT_VOLATILE,
  TT_VOID,
  TT_STRUCT,
  TT_UNION,
  TT_ENUM,
  TT_ELLIPSIS,
  TT_CASE,
  TT_DEFAULT,
  TT_IF,
  TT_ELSE,
  TT_SWITCH,
  TT_WHILE,
  TT_DO,
  TT_FOR,
  TT_GOTO,
  TT_CONTINUE,
  TT_BREAK,
  TT_RETURN,
  TT_SEMICOLON,
  TT_LBRACE,
  TT_RBRACE,
  TT_COMMA,
  TT_COLON,
  TT_EQUAL,
  TT_LPAREN,
  TT_RPAREN,
  TT_LBRACK,
  TT_RBRACK,
  TT_PERIOD,
  TT_AMPERSAND,
  TT_EXCLAMATION,
  TT_TILDE,
  TT_MINUS,
  TT_PLUS,
  TT_ASTERISK,
  TT_SLASH,
  TT_PERCENT,
  TT_LT,
  TT_GT,
  TT_CIRCUMFLEX,
  TT_VBAR,
  TT_QUESTION,
  TT_NOT_A_TOKEN
} TokenType;

typedef struct _pNode {
  int line, col;
  char * str;
  NodeType type;
  TokenType tokType;
  int childCount;
  struct _pNode ** children;
} CParserNode;

CParserNode * CParserNewToken (int line, int col, int len, char * str,
                              TokenType ttyp);
CParserNode * CParserNewNode (NodeType symbol, int childCount);
void CParserFreeNode (CParserNode * node);
void CParserSetChild (CParserNode * parent, int index, CParserNode * child);

void CParserHandleDeclaration (CParserNode * declNode);

void CParserSetRoot (CParserNode * newRoot);
CParserNode * CParserGetRoot (void);

void CParserEmitTree (CParserNode * crnt, int level);

extern char * CParserNontermStrings [];
extern char * CParserTokenStrings [];

/* ______________________________________________________________________
   End of cparserutils.h
   ______________________________________________________________________ */
#endif
