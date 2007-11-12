/* ______________________________________________________________________
   cparser.l
   $Id: cparser.l,v 1.2 2003/07/02 21:59:38 jriehl Exp $
   ______________________________________________________________________ */

/* This Lex specification is based on the Lex specification by Jutta Degener
 * (1995), http://www.lysator.liu.se/c/ANSI-C-grammar-y.html, which
 * was derived from a Lex specification of Jeff Lee.
*/

D                       [0-9]
L                       [a-zA-Z_]
H                       [a-fA-F0-9]
E                       [Ee][+-]?{D}+
FS                      (f|F|l|L)
IS                      (u|U|l|L)*

%{
#include <stdio.h>
#include "cparserutils.h"
#include "namespace.h"

#define YYSTYPE CParserNode*

#include "cparser.tab.h"

static void CParserCount(TokenType tt);
static void CParserComment();
static void CParserHash();
static int CParserCheckType();

%}

%%
"/*"                    { CParserComment(); }
"#"                     { CParserHash(); }

"auto"                  { CParserCount(TT_AUTO); return(AUTO); }
"break"                 { CParserCount(TT_BREAK); return(BREAK); }
"case"                  { CParserCount(TT_CASE); return(CASE); }
"char"                  { CParserCount(TT_CHAR); return(CHAR); }
"const"                 { CParserCount(TT_CONST); return(CONST); }
"continue"              { CParserCount(TT_CONTINUE); return(CONTINUE); }
"default"               { CParserCount(TT_DEFAULT); return(DEFAULT); }
"do"                    { CParserCount(TT_DO); return(DO); }
"double"                { CParserCount(TT_DOUBLE); return(DOUBLE); }
"else"                  { CParserCount(TT_ELSE); return(ELSE); }
"enum"                  { CParserCount(TT_ENUM); return(ENUM); }
"extern"                { CParserCount(TT_EXTERN); return(EXTERN); }
"float"                 { CParserCount(TT_FLOAT); return(FLOAT); }
"for"                   { CParserCount(TT_FOR); return(FOR); }
"goto"                  { CParserCount(TT_GOTO); return(GOTO); }
"if"                    { CParserCount(TT_IF); return(IF); }
"int"                   { CParserCount(TT_INT); return(INT); }
"long"                  { CParserCount(TT_LONG); return(LONG); }
"register"              { CParserCount(TT_REGISTER); return(REGISTER); }
"return"                { CParserCount(TT_RETURN); return(RETURN); }
"short"                 { CParserCount(TT_SHORT); return(SHORT); }
"signed"                { CParserCount(TT_SIGNED); return(SIGNED); }
"sizeof"                { CParserCount(TT_SIZEOF); return(SIZEOF); }
"static"                { CParserCount(TT_STATIC); return(STATIC); }
"struct"                { CParserCount(TT_STRUCT); return(STRUCT); }
"switch"                { CParserCount(TT_SWITCH); return(SWITCH); }
"typedef"               { CParserCount(TT_TYPEDEF); return(TYPEDEF); }
"union"                 { CParserCount(TT_UNION); return(UNION); }
"unsigned"              { CParserCount(TT_UNSIGNED); return(UNSIGNED); }
"void"                  { CParserCount(TT_VOID); return(VOID); }
"volatile"              { CParserCount(TT_VOLATILE); return(VOLATILE); }
"while"                 { CParserCount(TT_WHILE); return(WHILE); }

{L}({L}|{D})*           { CParserCount(TT_IDENTIFIER);
                          return(CParserCheckType()); }

0[xX]{H}+{IS}?          { CParserCount(TT_CONSTANT); return(CONSTANT); }
0{D}+{IS}?              { CParserCount(TT_CONSTANT); return(CONSTANT); }
{D}+{IS}?               { CParserCount(TT_CONSTANT); return(CONSTANT); }
L?'(\\.|[^\\'])+'       { CParserCount(TT_CONSTANT); return(CONSTANT); }

{D}+{E}{FS}?            { CParserCount(TT_CONSTANT); return(CONSTANT); }
{D}*"."{D}+({E})?{FS}?  { CParserCount(TT_CONSTANT); return(CONSTANT); }
{D}+"."{D}*({E})?{FS}?  { CParserCount(TT_CONSTANT); return(CONSTANT); }

L?\"(\\.|[^\\"])*\"     { CParserCount(TT_STRING_LITERAL);
                          return(STRING_LITERAL); }

"..."                   { CParserCount(TT_ELLIPSIS); return(ELLIPSIS); }
">>="                   { CParserCount(TT_RIGHT_ASSIGN);
                          return(RIGHT_ASSIGN); }
"<<="                   { CParserCount(TT_LEFT_ASSIGN); return(LEFT_ASSIGN); }
"+="                    { CParserCount(TT_ADD_ASSIGN); return(ADD_ASSIGN); }
"-="                    { CParserCount(TT_SUB_ASSIGN); return(SUB_ASSIGN); }
"*="                    { CParserCount(TT_MUL_ASSIGN); return(MUL_ASSIGN); }
"/="                    { CParserCount(TT_DIV_ASSIGN); return(DIV_ASSIGN); }
"%="                    { CParserCount(TT_MOD_ASSIGN); return(MOD_ASSIGN); }
"&="                    { CParserCount(TT_AND_ASSIGN); return(AND_ASSIGN); }
"^="                    { CParserCount(TT_XOR_ASSIGN); return(XOR_ASSIGN); }
"|="                    { CParserCount(TT_OR_ASSIGN); return(OR_ASSIGN); }
">>"                    { CParserCount(TT_RIGHT_OP); return(RIGHT_OP); }
"<<"                    { CParserCount(TT_LEFT_OP); return(LEFT_OP); }
"++"                    { CParserCount(TT_INC_OP); return(INC_OP); }
"--"                    { CParserCount(TT_DEC_OP); return(DEC_OP); }
"->"                    { CParserCount(TT_PTR_OP); return(PTR_OP); }
"&&"                    { CParserCount(TT_AND_OP); return(AND_OP); }
"||"                    { CParserCount(TT_OR_OP); return(OR_OP); }
"<="                    { CParserCount(TT_LE_OP); return(LE_OP); }
">="                    { CParserCount(TT_GE_OP); return(GE_OP); }
"=="                    { CParserCount(TT_EQ_OP); return(EQ_OP); }
"!="                    { CParserCount(TT_NE_OP); return(NE_OP); }
";"                     { CParserCount(TT_SEMICOLON); return(';'); }
("{"|"<%")              { CParserCount(TT_LBRACE); return('{'); }
("}"|"%>")              { CParserCount(TT_RBRACE); return('}'); }
","                     { CParserCount(TT_COMMA); return(','); }
":"                     { CParserCount(TT_COLON); return(':'); }
"="                     { CParserCount(TT_EQUAL); return('='); }
"("                     { CParserCount(TT_LPAREN); return('('); }
")"                     { CParserCount(TT_RPAREN); return(')'); }
("["|"<:")              { CParserCount(TT_LBRACK); return('['); }
("]"|":>")              { CParserCount(TT_RBRACK); return(']'); }
"."                     { CParserCount(TT_PERIOD); return('.'); }
"&"                     { CParserCount(TT_AMPERSAND); return('&'); }
"!"                     { CParserCount(TT_EXCLAMATION); return('!'); }
"~"                     { CParserCount(TT_TILDE); return('~'); }
"-"                     { CParserCount(TT_MINUS); return('-'); }
"+"                     { CParserCount(TT_PLUS); return('+'); }
"*"                     { CParserCount(TT_ASTERISK); return('*'); }
"/"                     { CParserCount(TT_SLASH); return('/'); }
"%"                     { CParserCount(TT_PERCENT); return('%'); }
"<"                     { CParserCount(TT_LT); return('<'); }
">"                     { CParserCount(TT_GT); return('>'); }
"^"                     { CParserCount(TT_CIRCUMFLEX); return('^'); }
"|"                     { CParserCount(TT_VBAR); return('|'); }
"?"                     { CParserCount(TT_QUESTION); return('?'); }

[ \t\v\n\f]             { CParserCount(TT_NOT_A_TOKEN); }
.                       { /* ignore bad characters */ }

%%

int cparserwrap()
{
        return(1);
}


static void CParserHash()
{
        while ('\n' != input());
}

static void CParserComment()
{
        char c, c1;

        putchar('/'); putchar('*'); /* gdc: added */
loop:
        while ((c = input()) != '*' && c != 0)
                putchar(c);

        if ((c1 = input()) != '/' && c != 0)
        {
                unput(c1);
                goto loop;
        }

        if (c != 0)
                putchar(c); /* gdc: added */
                putchar(c1);
}

int cparser_line = 0;
int cparser_column = 0;

static void CParserCount(TokenType tt)
{
        int i;

        /* This was added to define the semantic value of the current yytext */
        if (TT_NOT_A_TOKEN != tt) /* Used to indicate whitespace... */
           {          
                cparserlval = CParserNewToken(cparser_line, cparser_column,
                                              cparserleng, cparsertext, tt);
           }

        for (i = 0; cparsertext[i] != '\0'; i++)
                if (cparsertext[i] == '\n') {
                        cparser_column = 0;
                        cparser_line++;
                }
                else if (cparsertext[i] == '\t')
                        cparser_column += 8 - (cparser_column % 8);
                else
                        cparser_column++;

        ECHO;
}

/*
* pseudo code --- this is what it should check
*
*       if (cparsertext == type_name)
*               return(TYPE_NAME);
*
*       return(IDENTIFIER);
*/

static int CParserCheckType()
{
    char * name = (char *)malloc(cparserleng + 1);
    strncpy(name, cparsertext, cparserleng);
    name[cparserleng] = '\0';

    if (inNamespace(name))
     {
        cparserlval->tokType = TT_TYPE_NAME;
        return(TYPE_NAME);
     }
    else
     {
        return(IDENTIFIER);
     }
}
