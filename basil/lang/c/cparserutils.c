/* ______________________________________________________________________
   cparserutils.c
   $Id: cparserutils.c,v 1.3 2003/07/13 00:40:37 jriehl Exp $
   ______________________________________________________________________ */

/* ______________________________________________________________________
   Include files
   ______________________________________________________________________ */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#include "cparserutils.h"
#include "namespace.h"

/* ______________________________________________________________________
   Static data
   ______________________________________________________________________ */

static CParserNode * root = NULL;

char * CParserNontermStrings [] = {"TOKEN_TYPE",
                                   "POSTFIX_EXPRESSION",
                                   "ARGUMENT_EXPRESSION_LIST",
                                   "UNARY_EXPRESSION",
                                   "CAST_EXPRESSION",
                                   "MULTIPLICATIVE_EXPRESSION",
                                   "ADDITIVE_EXPRESSION",
                                   "SHIFT_EXPRESSION",
                                   "RELATIONAL_EXPRESSION",
                                   "EQUALITY_EXPRESSION",
                                   "AND_EXPRESSION",
                                   "XOR_EXPRESSION",
                                   "OR_EXPRESSION",
                                   "LOGICAL_AND_EXPRESSION",
                                   "LOGICAL_OR_EXPRESSION",
                                   "CONDITIONAL_EXPRESSION",
                                   "ASSIGNMENT_EXPRESSION",
                                   "EXPRESSION",
                                   "DECLARATION",
                                   "DECLARATION_SPECIFIERS",
                                   "INIT_DECLARATOR_LIST",
                                   "INIT_DECLARATOR",
                                   "SU_SPECIFIER",
                                   "STRUCT_DECLARATION_LIST",
                                   "STRUCT_DECLARATION",
                                   "SPECIFIER_QUALIFIER_LIST",
                                   "STRUCT_DECLARATOR_LIST",
                                   "STRUCT_DECLARATOR",
                                   "ENUM_SPECIFIER",
                                   "ENUMERATOR_LIST",
                                   "ENUMERATOR",
                                   "DECLARATOR",
                                   "DIRECT_DECLARATOR",
                                   "POINTER",
                                   "TYPE_QUALIFIER_LIST",
                                   "PARAMETER_TYPE_LIST",
                                   "PARAMETER_LIST",
                                   "PARAMETER_DECLARATION",
                                   "IDENTIFIER_LIST",
                                   "TYPE_NAME_TYPE",
                                   "ABSTRACT_DECLARATOR",
                                   "DIRECT_ABSTRACT_DECLARATOR",
                                   "INITIALIZER",
                                   "INITIALIZER_LIST",
                                   "LABELED_STATEMENT",
                                   "COMPOUND_STATEMENT",
                                   "DECLARATION_LIST",
                                   "STATEMENT_LIST",
                                   "EXPRESSION_STATEMENT",
                                   "SELECTION_STATEMENT",
                                   "ITERATION_STATEMENT",
                                   "JUMP_STATEMENT",
                                   "TRANSLATION_UNIT",
                                   "FUNCTION_DEFINITION"};

char * CParserTokenStrings [] = {"IDENTIFIER",
                                 "CONSTANT",
                                 "STRING_LITERAL",
                                 "SIZEOF",
                                 "PTR_OP",
                                 "INC_OP",
                                 "DEC_OP",
                                 "LEFT_OP",
                                 "RIGHT_OP",
                                 "LE_OP",
                                 "GE_OP",
                                 "EQ_OP",
                                 "NE_OP",
                                 "AND_OP",
                                 "OR_OP",
                                 "MUL_ASSIGN",
                                 "DIV_ASSIGN",
                                 "MOD_ASSIGN",
                                 "ADD_ASSIGN",
                                 "SUB_ASSIGN",
                                 "LEFT_ASSIGN",
                                 "RIGHT_ASSIGN",
                                 "AND_ASSIGN",
                                 "XOR_ASSIGN",
                                 "OR_ASSIGN",
                                 "TYPE_NAME",
                                 "TYPEDEF",
                                 "EXTERN",
                                 "STATIC",
                                 "AUTO",
                                 "REGISTER",
                                 "CHAR",
                                 "SHORT",
                                 "INT",
                                 "LONG",
                                 "SIGNED",
                                 "UNSIGNED",
                                 "FLOAT",
                                 "DOUBLE",
                                 "CONST",
                                 "VOLATILE",
                                 "VOID",
                                 "STRUCT",
                                 "UNION",
                                 "ENUM",
                                 "ELLIPSIS",
                                 "CASE",
                                 "DEFAULT",
                                 "IF",
                                 "ELSE",
                                 "SWITCH",
                                 "WHILE",
                                 "DO",
                                 "FOR",
                                 "GOTO",
                                 "CONTINUE",
                                 "BREAK",
                                 "RETURN",
                                 "SEMICOLON",
                                 "LBRACE",
                                 "RBRACE",
                                 "COMMA",
                                 "COLON",
                                 "EQUAL",
                                 "LPAREN",
                                 "RPAREN",
                                 "LBRACK",
                                 "RBRACK",
                                 "PERIOD",
                                 "AMPERSAND",
                                 "EXCLAMATION",
                                 "TILDE",
                                 "MINUS",
                                 "PLUS",
                                 "ASTERISK",
                                 "SLASH",
                                 "PERCENT",
                                 "LT",
                                 "GT",
                                 "CIRCUMFLEX",
                                 "VBAR",
                                 "QUESTION",
                                 "NOT_A_TOKEN"};

/* ______________________________________________________________________
   Function definitions
   ______________________________________________________________________ */

void CParserSetRoot (CParserNode * newRoot)
{
  root = newRoot;
}

/* ______________________________________________________________________ */

CParserNode * CParserGetRoot (void)
{
  return root;
}

/* ______________________________________________________________________ */

CParserNode * CParserNewToken (int line, int col, int len, char * str,
                              TokenType ttyp)
{
  CParserNode * retVal = (CParserNode *)malloc(sizeof(CParserNode));
  char * tokenText = (char *)malloc(len + 1);

  strncpy(tokenText, str, len);
  tokenText[len] = '\0';

  retVal->line = line;
  retVal->col = col;
  retVal->str = tokenText;
  retVal->type = TOKEN_TYPE;
  retVal->tokType = ttyp;
  retVal->childCount = 0;
  retVal->children = NULL;
  return retVal;
}

/* ______________________________________________________________________ */

CParserNode * CParserNewNode (NodeType symbol, int childCount)
{
  CParserNode * retVal = (CParserNode *)malloc(sizeof(CParserNode));
  int i;

  retVal->line = 0;
  retVal->col = 0;
  retVal->str = NULL;
  retVal->type = symbol;
  retVal->tokType = TT_NOT_A_TOKEN;
  retVal->childCount = childCount;
  retVal->children = (CParserNode **)malloc(childCount * sizeof(CParserNode*));
  for (i = 0; i < childCount; i++)
    {
      retVal->children[i] = NULL;
    }
  return retVal;
}

/* ______________________________________________________________________ */

void CParserFreeNode (CParserNode * node)
{
  int i;
  if (NULL != node)
    {
      for (i = 0; i < node->childCount; i++)
        {
          CParserFreeNode(node->children[i]);
        }
      free(node->children);
      free(node->str);
      free(node);
    }
}

/* ______________________________________________________________________ */

void CParserSetChild (CParserNode * parent, int index, CParserNode * child)
{
  parent->children[index] = child;
}

/* ______________________________________________________________________ */

static int isATypedef (CParserNode * node)
{
  int i;
  int retVal = 0;
  switch (node->type)
    {
    case TOKEN_TYPE:
      if (node->tokType == TT_TYPEDEF)
        {
          retVal = 1;
        }
      break;

    default:
      for (i = 0; i < node->childCount; i++)
        {
          if (0 != isATypedef(node->children[i]))
            {
              retVal = 1;
              break;
            }
        }
    }
  return retVal;
}

/* ______________________________________________________________________ */

static int addIdentifiersToNamespace (CParserNode * node)
{
  int i;
  int retVal = 0;
  switch (node->type)
    {
    case TOKEN_TYPE:
      if (node->tokType == TT_IDENTIFIER)
        {
          addName(node->str, NULL);
          retVal = 1;
        }
      break;

    case INIT_DECLARATOR:
      /* Only process the first child node...the second is some sort of
         initialization string. */
      retVal = addIdentifiersToNamespace(node->children[0]);
      break;

    case INIT_DECLARATOR_LIST:
      /* We actually want to only stop on the first IDENTIFIER at the
         DECLARATOR level.  Here we ignore the exit code to fully process the
         declarator list. */
      for (i = 0; i < node->childCount; i++)
        {
          addIdentifiersToNamespace(node->children[i]);
        }
      break;

    default:
      for (i = 0; i < node->childCount; i++)
        {
          retVal = addIdentifiersToNamespace(node->children[i]);
          if (1 == retVal) break;
        }
    }
  return retVal;
}

/* ______________________________________________________________________ */

void CParserHandleDeclaration (CParserNode * declNode)
{
  assert(2 == declNode->childCount);
  if (0 != isATypedef(declNode->children[0]))
    {
      addIdentifiersToNamespace(declNode->children[1]);
    }
}

/* ______________________________________________________________________ */

static void printSpacing (int count) {
  int i;
  for (i = 0; i < count; i++) {
    printf(" ");
  }
}

/* ______________________________________________________________________ */

void CParserEmitTree (CParserNode * crnt, int level)
{
  if (NULL != crnt) {
    printSpacing(level);
    if (TOKEN_TYPE == crnt->type) {
      printf("((%s, \"%s\", %d, %d), [])\n",
             CParserTokenStrings[(int)crnt->tokType],
             crnt->str, crnt->line, crnt->col);
    } else {
      int i;

      printf("(%s, [\n", CParserNontermStrings[(int)crnt->type]);
      for (i = 0; i < crnt->childCount; i++) {
        CParserEmitTree(crnt->children[i], level + 1);
      }
      printSpacing(level);
      printf("])\n");
    }
  }
}

/* ______________________________________________________________________
   End of cparserutils.c
   ______________________________________________________________________ */
