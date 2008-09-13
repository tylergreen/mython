/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton implementation for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.3"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Using locations.  */
#define YYLSP_NEEDED 0

/* Substitute the variable and function names.  */
#define yyparse cparserparse
#define yylex   cparserlex
#define yyerror cparsererror
#define yylval  cparserlval
#define yychar  cparserchar
#define yydebug cparserdebug
#define yynerrs cparsernerrs


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     IDENTIFIER = 258,
     CONSTANT = 259,
     STRING_LITERAL = 260,
     SIZEOF = 261,
     PTR_OP = 262,
     INC_OP = 263,
     DEC_OP = 264,
     LEFT_OP = 265,
     RIGHT_OP = 266,
     LE_OP = 267,
     GE_OP = 268,
     EQ_OP = 269,
     NE_OP = 270,
     AND_OP = 271,
     OR_OP = 272,
     MUL_ASSIGN = 273,
     DIV_ASSIGN = 274,
     MOD_ASSIGN = 275,
     ADD_ASSIGN = 276,
     SUB_ASSIGN = 277,
     LEFT_ASSIGN = 278,
     RIGHT_ASSIGN = 279,
     AND_ASSIGN = 280,
     XOR_ASSIGN = 281,
     OR_ASSIGN = 282,
     TYPE_NAME = 283,
     TYPEDEF = 284,
     EXTERN = 285,
     STATIC = 286,
     AUTO = 287,
     REGISTER = 288,
     CHAR = 289,
     SHORT = 290,
     INT = 291,
     LONG = 292,
     SIGNED = 293,
     UNSIGNED = 294,
     FLOAT = 295,
     DOUBLE = 296,
     CONST = 297,
     VOLATILE = 298,
     VOID = 299,
     STRUCT = 300,
     UNION = 301,
     ENUM = 302,
     ELLIPSIS = 303,
     CASE = 304,
     DEFAULT = 305,
     IF = 306,
     ELSE = 307,
     SWITCH = 308,
     WHILE = 309,
     DO = 310,
     FOR = 311,
     GOTO = 312,
     CONTINUE = 313,
     BREAK = 314,
     RETURN = 315
   };
#endif
/* Tokens.  */
#define IDENTIFIER 258
#define CONSTANT 259
#define STRING_LITERAL 260
#define SIZEOF 261
#define PTR_OP 262
#define INC_OP 263
#define DEC_OP 264
#define LEFT_OP 265
#define RIGHT_OP 266
#define LE_OP 267
#define GE_OP 268
#define EQ_OP 269
#define NE_OP 270
#define AND_OP 271
#define OR_OP 272
#define MUL_ASSIGN 273
#define DIV_ASSIGN 274
#define MOD_ASSIGN 275
#define ADD_ASSIGN 276
#define SUB_ASSIGN 277
#define LEFT_ASSIGN 278
#define RIGHT_ASSIGN 279
#define AND_ASSIGN 280
#define XOR_ASSIGN 281
#define OR_ASSIGN 282
#define TYPE_NAME 283
#define TYPEDEF 284
#define EXTERN 285
#define STATIC 286
#define AUTO 287
#define REGISTER 288
#define CHAR 289
#define SHORT 290
#define INT 291
#define LONG 292
#define SIGNED 293
#define UNSIGNED 294
#define FLOAT 295
#define DOUBLE 296
#define CONST 297
#define VOLATILE 298
#define VOID 299
#define STRUCT 300
#define UNION 301
#define ENUM 302
#define ELLIPSIS 303
#define CASE 304
#define DEFAULT 305
#define IF 306
#define ELSE 307
#define SWITCH 308
#define WHILE 309
#define DO 310
#define FOR 311
#define GOTO 312
#define CONTINUE 313
#define BREAK 314
#define RETURN 315




/* Copy the first part of user declarations.  */
#line 1 "cparser.y"

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



/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif

#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif



/* Copy the second part of user declarations.  */


/* Line 216 of yacc.c.  */
#line 253 "cparser.tab.c"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int i)
#else
static int
YYID (i)
    int i;
#endif
{
  return i;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef _STDLIB_H
#      define _STDLIB_H 1
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined _STDLIB_H \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef _STDLIB_H
#    define _STDLIB_H 1
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss;
  YYSTYPE yyvs;
  };

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack)					\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack, Stack, yysize);				\
	Stack = &yyptr->Stack;						\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  64
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   1302

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  85
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  66
/* YYNRULES -- Number of rules.  */
#define YYNRULES  215
/* YYNRULES -- Number of states.  */
#define YYNSTATES  353

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   315

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    72,     2,     2,     2,    74,    67,     2,
      61,    62,    68,    69,    66,    70,    65,    73,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    80,    82,
      75,    81,    76,    79,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    63,     2,    64,    77,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    83,    78,    84,    71,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     5,     7,     9,    13,    15,    20,    24,
      29,    33,    37,    40,    43,    45,    49,    51,    54,    57,
      60,    63,    68,    70,    72,    74,    76,    78,    80,    82,
      87,    89,    93,    97,   101,   103,   107,   111,   113,   117,
     121,   123,   127,   131,   135,   139,   141,   145,   149,   151,
     155,   157,   161,   163,   167,   169,   173,   175,   179,   181,
     187,   189,   193,   195,   197,   199,   201,   203,   205,   207,
     209,   211,   213,   215,   217,   221,   223,   226,   230,   232,
     235,   237,   240,   242,   245,   247,   251,   253,   257,   259,
     261,   263,   265,   267,   269,   271,   273,   275,   277,   279,
     281,   283,   285,   287,   289,   291,   297,   302,   305,   307,
     309,   311,   314,   318,   321,   323,   326,   328,   330,   334,
     336,   339,   343,   345,   347,   352,   358,   361,   363,   367,
     369,   373,   375,   377,   380,   382,   384,   388,   393,   397,
     402,   407,   411,   413,   416,   419,   423,   425,   428,   430,
     434,   436,   440,   443,   446,   448,   450,   454,   456,   459,
     461,   463,   466,   470,   473,   477,   481,   486,   489,   493,
     497,   502,   504,   508,   513,   515,   519,   521,   523,   525,
     527,   529,   531,   535,   540,   544,   546,   549,   553,   557,
     562,   564,   567,   569,   572,   574,   577,   583,   591,   597,
     603,   611,   618,   626,   630,   633,   636,   639,   643,   645,
     648,   650,   652,   657,   661,   665
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int16 yyrhs[] =
{
     148,     0,    -1,     3,    -1,     4,    -1,     5,    -1,    61,
     105,    62,    -1,    86,    -1,    87,    63,   105,    64,    -1,
      87,    61,    62,    -1,    87,    61,    88,    62,    -1,    87,
      65,     3,    -1,    87,     7,     3,    -1,    87,     8,    -1,
      87,     9,    -1,   103,    -1,    88,    66,   103,    -1,    87,
      -1,     8,    89,    -1,     9,    89,    -1,    90,    91,    -1,
       6,    89,    -1,     6,    61,   133,    62,    -1,    67,    -1,
      68,    -1,    69,    -1,    70,    -1,    71,    -1,    72,    -1,
      89,    -1,    61,   133,    62,    91,    -1,    91,    -1,    92,
      68,    91,    -1,    92,    73,    91,    -1,    92,    74,    91,
      -1,    92,    -1,    93,    69,    92,    -1,    93,    70,    92,
      -1,    93,    -1,    94,    10,    93,    -1,    94,    11,    93,
      -1,    94,    -1,    95,    75,    94,    -1,    95,    76,    94,
      -1,    95,    12,    94,    -1,    95,    13,    94,    -1,    95,
      -1,    96,    14,    95,    -1,    96,    15,    95,    -1,    96,
      -1,    97,    67,    96,    -1,    97,    -1,    98,    77,    97,
      -1,    98,    -1,    99,    78,    98,    -1,    99,    -1,   100,
      16,    99,    -1,   100,    -1,   101,    17,   100,    -1,   101,
      -1,   101,    79,   105,    80,   102,    -1,   102,    -1,    89,
     104,   103,    -1,    81,    -1,    18,    -1,    19,    -1,    20,
      -1,    21,    -1,    22,    -1,    23,    -1,    24,    -1,    25,
      -1,    26,    -1,    27,    -1,   103,    -1,   105,    66,   103,
      -1,   102,    -1,   108,    82,    -1,   108,   109,    82,    -1,
     111,    -1,   111,   108,    -1,   112,    -1,   112,   108,    -1,
     124,    -1,   124,   108,    -1,   110,    -1,   109,    66,   110,
      -1,   125,    -1,   125,    81,   136,    -1,    29,    -1,    30,
      -1,    31,    -1,    32,    -1,    33,    -1,    44,    -1,    34,
      -1,    35,    -1,    36,    -1,    37,    -1,    40,    -1,    41,
      -1,    38,    -1,    39,    -1,   113,    -1,   121,    -1,    28,
      -1,   114,   120,    83,   115,    84,    -1,   114,    83,   115,
      84,    -1,   114,   120,    -1,    45,    -1,    46,    -1,   116,
      -1,   115,   116,    -1,   117,   118,    82,    -1,   112,   117,
      -1,   112,    -1,   124,   117,    -1,   124,    -1,   119,    -1,
     118,    66,   119,    -1,   125,    -1,    80,   106,    -1,   125,
      80,   106,    -1,     3,    -1,    28,    -1,    47,    83,   122,
      84,    -1,    47,   120,    83,   122,    84,    -1,    47,   120,
      -1,   123,    -1,   122,    66,   123,    -1,     3,    -1,     3,
      81,   106,    -1,    42,    -1,    43,    -1,   127,   126,    -1,
     126,    -1,     3,    -1,    61,   125,    62,    -1,   126,    63,
     106,    64,    -1,   126,    63,    64,    -1,   126,    61,   129,
      62,    -1,   126,    61,   132,    62,    -1,   126,    61,    62,
      -1,    68,    -1,    68,   128,    -1,    68,   127,    -1,    68,
     128,   127,    -1,   124,    -1,   128,   124,    -1,   130,    -1,
     130,    66,    48,    -1,   131,    -1,   130,    66,   131,    -1,
     108,   125,    -1,   108,   134,    -1,   108,    -1,     3,    -1,
     132,    66,     3,    -1,   117,    -1,   117,   134,    -1,   127,
      -1,   135,    -1,   127,   135,    -1,    61,   134,    62,    -1,
      63,    64,    -1,    63,   106,    64,    -1,   135,    63,    64,
      -1,   135,    63,   106,    64,    -1,    61,    62,    -1,    61,
     129,    62,    -1,   135,    61,    62,    -1,   135,    61,   129,
      62,    -1,   103,    -1,    83,   137,    84,    -1,    83,   137,
      66,    84,    -1,   136,    -1,   137,    66,   136,    -1,   139,
      -1,   141,    -1,   144,    -1,   145,    -1,   146,    -1,   147,
      -1,     3,    80,   138,    -1,    49,   106,    80,   138,    -1,
      50,    80,   138,    -1,    83,    -1,   140,    84,    -1,   140,
     143,    84,    -1,   140,   142,    84,    -1,   140,   142,   143,
      84,    -1,   107,    -1,   142,   107,    -1,   138,    -1,   143,
     138,    -1,    82,    -1,   105,    82,    -1,    51,    61,   105,
      62,   138,    -1,    51,    61,   105,    62,   138,    52,   138,
      -1,    53,    61,   105,    62,   138,    -1,    54,    61,   105,
      62,   138,    -1,    55,   138,    54,    61,   105,    62,    82,
      -1,    56,    61,   144,   144,    62,   138,    -1,    56,    61,
     144,   144,   105,    62,   138,    -1,    57,     3,    82,    -1,
      58,    82,    -1,    59,    82,    -1,    60,    82,    -1,    60,
     105,    82,    -1,   149,    -1,   148,   149,    -1,   150,    -1,
     107,    -1,   108,   125,   142,   141,    -1,   108,   125,   141,
      -1,   125,   142,   141,    -1,   125,   141,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    39,    39,    40,    41,    42,    48,    49,    57,    64,
      72,    79,    86,    92,   103,   104,   116,   117,   123,   129,
     135,   141,   153,   154,   155,   156,   157,   158,   164,   165,
     178,   179,   186,   193,   205,   206,   213,   225,   226,   233,
     245,   246,   253,   260,   267,   279,   280,   287,   299,   300,
     312,   313,   325,   326,   338,   339,   351,   352,   364,   365,
     378,   379,   391,   392,   393,   394,   395,   396,   397,   398,
     399,   400,   401,   407,   408,   420,   426,   431,   443,   448,
     454,   459,   465,   470,   481,   482,   494,   495,   507,   508,
     509,   510,   511,   517,   518,   519,   520,   521,   522,   523,
     524,   525,   526,   527,   528,   534,   544,   552,   564,   565,
     571,   572,   583,   595,   601,   602,   608,   614,   615,   627,
     628,   634,   646,   647,   651,   659,   669,   681,   682,   694,
     695,   707,   708,   714,   720,   726,   727,   734,   742,   749,
     757,   765,   777,   778,   784,   790,   802,   803,   815,   816,
     828,   829,   841,   847,   853,   859,   860,   872,   873,   884,
     885,   886,   897,   904,   910,   917,   924,   932,   938,   945,
     952,   965,   966,   973,   986,   987,   999,  1000,  1001,  1002,
    1003,  1004,  1010,  1017,  1025,  1037,  1044,  1051,  1059,  1067,
    1081,  1088,  1099,  1100,  1111,  1112,  1123,  1132,  1143,  1157,
    1166,  1177,  1187,  1203,  1210,  1216,  1222,  1228,  1240,  1245,
    1257,  1258,  1264,  1272,  1279,  1286
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "IDENTIFIER", "CONSTANT",
  "STRING_LITERAL", "SIZEOF", "PTR_OP", "INC_OP", "DEC_OP", "LEFT_OP",
  "RIGHT_OP", "LE_OP", "GE_OP", "EQ_OP", "NE_OP", "AND_OP", "OR_OP",
  "MUL_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN",
  "LEFT_ASSIGN", "RIGHT_ASSIGN", "AND_ASSIGN", "XOR_ASSIGN", "OR_ASSIGN",
  "TYPE_NAME", "TYPEDEF", "EXTERN", "STATIC", "AUTO", "REGISTER", "CHAR",
  "SHORT", "INT", "LONG", "SIGNED", "UNSIGNED", "FLOAT", "DOUBLE", "CONST",
  "VOLATILE", "VOID", "STRUCT", "UNION", "ENUM", "ELLIPSIS", "CASE",
  "DEFAULT", "IF", "ELSE", "SWITCH", "WHILE", "DO", "FOR", "GOTO",
  "CONTINUE", "BREAK", "RETURN", "'('", "')'", "'['", "']'", "'.'", "','",
  "'&'", "'*'", "'+'", "'-'", "'~'", "'!'", "'/'", "'%'", "'<'", "'>'",
  "'^'", "'|'", "'?'", "':'", "'='", "';'", "'{'", "'}'", "$accept",
  "primary_expression", "postfix_expression", "argument_expression_list",
  "unary_expression", "unary_operator", "cast_expression",
  "multiplicative_expression", "additive_expression", "shift_expression",
  "relational_expression", "equality_expression", "and_expression",
  "exclusive_or_expression", "inclusive_or_expression",
  "logical_and_expression", "logical_or_expression",
  "conditional_expression", "assignment_expression", "assignment_operator",
  "expression", "constant_expression", "declaration",
  "declaration_specifiers", "init_declarator_list", "init_declarator",
  "storage_class_specifier", "type_specifier", "struct_or_union_specifier",
  "struct_or_union", "struct_declaration_list", "struct_declaration",
  "specifier_qualifier_list", "struct_declarator_list",
  "struct_declarator", "identifier_or_typename", "enum_specifier",
  "enumerator_list", "enumerator", "type_qualifier", "declarator",
  "direct_declarator", "pointer", "type_qualifier_list",
  "parameter_type_list", "parameter_list", "parameter_declaration",
  "identifier_list", "type_name", "abstract_declarator",
  "direct_abstract_declarator", "initializer", "initializer_list",
  "statement", "labeled_statement", "compound_statement_start",
  "compound_statement", "declaration_list", "statement_list",
  "expression_statement", "selection_statement", "iteration_statement",
  "jump_statement", "translation_unit", "external_declaration",
  "function_definition", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,    40,    41,    91,    93,    46,    44,    38,    42,    43,
      45,   126,    33,    47,    37,    60,    62,    94,   124,    63,
      58,    61,    59,   123,   125
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    85,    86,    86,    86,    86,    87,    87,    87,    87,
      87,    87,    87,    87,    88,    88,    89,    89,    89,    89,
      89,    89,    90,    90,    90,    90,    90,    90,    91,    91,
      92,    92,    92,    92,    93,    93,    93,    94,    94,    94,
      95,    95,    95,    95,    95,    96,    96,    96,    97,    97,
      98,    98,    99,    99,   100,   100,   101,   101,   102,   102,
     103,   103,   104,   104,   104,   104,   104,   104,   104,   104,
     104,   104,   104,   105,   105,   106,   107,   107,   108,   108,
     108,   108,   108,   108,   109,   109,   110,   110,   111,   111,
     111,   111,   111,   112,   112,   112,   112,   112,   112,   112,
     112,   112,   112,   112,   112,   113,   113,   113,   114,   114,
     115,   115,   116,   117,   117,   117,   117,   118,   118,   119,
     119,   119,   120,   120,   121,   121,   121,   122,   122,   123,
     123,   124,   124,   125,   125,   126,   126,   126,   126,   126,
     126,   126,   127,   127,   127,   127,   128,   128,   129,   129,
     130,   130,   131,   131,   131,   132,   132,   133,   133,   134,
     134,   134,   135,   135,   135,   135,   135,   135,   135,   135,
     135,   136,   136,   136,   137,   137,   138,   138,   138,   138,
     138,   138,   139,   139,   139,   140,   141,   141,   141,   141,
     142,   142,   143,   143,   144,   144,   145,   145,   145,   146,
     146,   146,   146,   147,   147,   147,   147,   147,   148,   148,
     149,   149,   150,   150,   150,   150
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     1,     1,     3,     1,     4,     3,     4,
       3,     3,     2,     2,     1,     3,     1,     2,     2,     2,
       2,     4,     1,     1,     1,     1,     1,     1,     1,     4,
       1,     3,     3,     3,     1,     3,     3,     1,     3,     3,
       1,     3,     3,     3,     3,     1,     3,     3,     1,     3,
       1,     3,     1,     3,     1,     3,     1,     3,     1,     5,
       1,     3,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     1,     2,     3,     1,     2,
       1,     2,     1,     2,     1,     3,     1,     3,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     5,     4,     2,     1,     1,
       1,     2,     3,     2,     1,     2,     1,     1,     3,     1,
       2,     3,     1,     1,     4,     5,     2,     1,     3,     1,
       3,     1,     1,     2,     1,     1,     3,     4,     3,     4,
       4,     3,     1,     2,     2,     3,     1,     2,     1,     3,
       1,     3,     2,     2,     1,     1,     3,     1,     2,     1,
       1,     2,     3,     2,     3,     3,     4,     2,     3,     3,
       4,     1,     3,     4,     1,     3,     1,     1,     1,     1,
       1,     1,     3,     4,     3,     1,     2,     3,     3,     4,
       1,     2,     1,     2,     1,     2,     5,     7,     5,     5,
       7,     6,     7,     3,     2,     2,     2,     3,     1,     2,
       1,     1,     4,     3,     3,     2
};

/* YYDEFACT[STATE-NAME] -- Default rule to reduce with in state
   STATE-NUM when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,   135,   104,    88,    89,    90,    91,    92,    94,    95,
      96,    97,   100,   101,    98,    99,   131,   132,    93,   108,
     109,     0,     0,   142,   211,     0,    78,    80,   102,     0,
     103,    82,     0,   134,     0,     0,   208,   210,   122,   123,
       0,   126,     0,   146,   144,   143,    76,     0,    84,    86,
      79,    81,     0,   107,    83,   185,   190,     0,     0,   215,
       0,     0,     0,   133,     1,   209,   129,     0,   127,     0,
     136,   147,   145,     0,    77,     0,   213,     0,   114,     0,
     110,     0,   116,     0,    86,     2,     3,     4,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    22,    23,    24,    25,    26,    27,   194,
     186,     6,    16,    28,     0,    30,    34,    37,    40,    45,
      48,    50,    52,    54,    56,    58,    60,    73,     0,   192,
     176,   177,     0,     0,   178,   179,   180,   181,   191,   214,
     155,   141,   154,     0,   148,   150,     0,     2,   138,    28,
      75,     0,     0,     0,   124,     0,    85,     0,   171,    87,
     212,   113,   106,   111,     0,     0,   117,   119,   115,     0,
       0,     0,    20,     0,    17,    18,     0,     0,     0,     0,
       0,     0,     0,     0,   204,   205,   206,     0,     0,   157,
       0,     0,    12,    13,     0,     0,     0,    63,    64,    65,
      66,    67,    68,    69,    70,    71,    72,    62,     0,    19,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     195,   188,     0,   187,   193,     0,     0,   152,   159,   153,
     160,   139,     0,   140,     0,   137,   130,   128,   125,   174,
       0,   120,     0,   112,     0,   105,   182,     0,     0,   184,
       0,     0,     0,     0,     0,   203,   207,     5,     0,   159,
     158,     0,    11,     8,     0,    14,     0,    10,    61,    31,
      32,    33,    35,    36,    38,    39,    43,    44,    41,    42,
      46,    47,    49,    51,    53,    55,    57,     0,    74,   189,
     167,     0,     0,   163,     0,   161,     0,     0,   149,   151,
     156,     0,   172,   118,   121,    21,   183,     0,     0,     0,
       0,     0,    29,     9,     0,     7,     0,   168,   162,   164,
     169,     0,   165,     0,   173,   175,   196,   198,   199,     0,
       0,     0,    15,    59,   170,   166,     0,     0,   201,     0,
     197,   200,   202
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,   111,   112,   274,   113,   114,   115,   116,   117,   118,
     119,   120,   121,   122,   123,   124,   125,   126,   127,   208,
     128,   151,    56,    57,    47,    48,    26,    27,    28,    29,
      79,    80,    81,   165,   166,    41,    30,    67,    68,    31,
      32,    33,    34,    45,   301,   144,   145,   146,   190,   302,
     240,   159,   250,   129,   130,    58,   131,    60,   133,   134,
     135,   136,   137,    35,    36,    37
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -224
static const yytype_int16 yypact[] =
{
     970,  -224,  -224,  -224,  -224,  -224,  -224,  -224,  -224,  -224,
    -224,  -224,  -224,  -224,  -224,  -224,  -224,  -224,  -224,  -224,
    -224,    26,    18,   144,  -224,     9,  1255,  1255,  -224,    41,
    -224,  1255,  1102,     3,    17,   880,  -224,  -224,  -224,  -224,
       4,   -43,   -15,  -224,  -224,   144,  -224,    21,  -224,  1082,
    -224,  -224,  1056,   -11,  -224,  -224,  -224,     9,   279,  -224,
    1102,   409,   667,     3,  -224,  -224,   -51,   -24,  -224,     4,
    -224,  -224,  -224,    18,  -224,   543,  -224,  1102,  1056,  1005,
    -224,    45,  1056,  1056,    30,   113,  -224,  -224,   786,   807,
     807,   831,   119,    23,   159,   169,   525,   172,   207,   135,
     161,   560,   646,  -224,  -224,  -224,  -224,  -224,  -224,  -224,
    -224,  -224,   140,   275,   831,  -224,   115,    63,   146,   116,
     226,   178,   170,   171,   243,     1,  -224,  -224,    48,  -224,
    -224,  -224,   349,   419,  -224,  -224,  -224,  -224,  -224,  -224,
    -224,  -224,    47,   201,   199,  -224,    77,  -224,  -224,  -224,
    -224,   206,   831,     4,  -224,   -21,  -224,   543,  -224,  -224,
    -224,  -224,  -224,  -224,   831,    69,  -224,   195,  -224,  1025,
     525,   646,  -224,   831,  -224,  -224,   196,   525,   831,   831,
     831,   223,   597,   197,  -224,  -224,  -224,    71,   128,   153,
     216,   277,  -224,  -224,   691,   831,   278,  -224,  -224,  -224,
    -224,  -224,  -224,  -224,  -224,  -224,  -224,  -224,   831,  -224,
     831,   831,   831,   831,   831,   831,   831,   831,   831,   831,
     831,   831,   831,   831,   831,   831,   831,   831,   831,   831,
    -224,  -224,   455,  -224,  -224,   925,   716,  -224,    55,  -224,
      31,  -224,  1234,  -224,   283,  -224,  -224,  -224,  -224,  -224,
      33,  -224,    45,  -224,   831,  -224,  -224,   227,   525,  -224,
     134,   142,   145,   229,   597,  -224,  -224,  -224,  1158,   173,
    -224,   831,  -224,  -224,   156,  -224,    -7,  -224,  -224,  -224,
    -224,  -224,   115,   115,    63,    63,   146,   146,   146,   146,
     116,   116,   226,   178,   170,   171,   243,    70,  -224,  -224,
    -224,   230,   241,  -224,   240,    31,  1199,   737,  -224,  -224,
    -224,   489,  -224,  -224,  -224,  -224,  -224,   525,   525,   525,
     831,   761,  -224,  -224,   831,  -224,   831,  -224,  -224,  -224,
    -224,   265,  -224,   267,  -224,  -224,   239,  -224,  -224,   163,
     525,   166,  -224,  -224,  -224,  -224,   525,   259,  -224,   525,
    -224,  -224,  -224
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -224,  -224,  -224,  -224,   -52,  -224,   -91,    43,    46,    34,
      51,    82,   118,   120,   117,   132,  -224,   -59,   -53,  -224,
     -97,   -57,     8,     0,  -224,   271,  -224,   -27,  -224,  -224,
     281,   -68,   -69,  -224,   108,   336,  -224,   297,   214,    44,
      -8,   -32,    -4,  -224,   -60,  -224,   126,  -224,   198,  -118,
    -223,  -129,  -224,   -80,  -224,  -224,   149,    96,   238,  -176,
    -224,  -224,  -224,  -224,   337,  -224
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If zero, do what YYDEFACT says.
   If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -1
static const yytype_uint16 yytable[] =
{
      25,   143,    63,   150,   187,   188,   264,    66,    24,   161,
     149,   163,     1,   168,    42,   305,   181,    49,   227,    44,
       1,     1,   158,   209,   239,    78,    50,    51,   249,    38,
     152,    54,   150,   189,   176,    25,   172,   174,   175,   149,
      69,    72,   153,    24,    38,   153,   305,    70,     1,    84,
       1,    78,    78,   234,    39,    78,    78,   325,     1,   229,
     154,   142,   149,   248,    61,    84,    62,    43,   138,    39,
      22,   270,    83,   167,   188,    78,   188,    23,    22,    22,
     228,   260,   261,   262,   178,   138,    23,    73,   321,    71,
     256,    46,   306,   150,   307,   246,    82,   259,   276,   311,
     149,   163,   189,    74,   158,   150,    22,   251,   235,    40,
     236,    75,   149,    23,   229,    23,   235,   312,   236,   279,
     280,   281,    82,    82,    52,   164,    82,    82,   217,   218,
     230,   297,   213,   214,   237,   252,   229,   229,   238,   243,
     138,   275,    78,   244,    78,    77,    82,   191,   192,   193,
     326,   253,   234,   266,   132,   278,   215,   216,   149,   149,
     149,   149,   149,   149,   149,   149,   149,   149,   149,   149,
     149,   149,   149,   149,   149,   149,   298,   150,   316,   304,
     322,    59,   335,   210,   149,   269,    16,    17,   211,   212,
     267,   219,   220,   170,   229,   150,   317,   314,    76,   177,
     229,   194,   149,   195,   318,   196,    63,   319,   229,   139,
     183,   229,    23,    82,   268,    82,   236,   184,   323,   149,
     179,    23,   324,   339,   341,   347,   160,    42,   349,   229,
     180,   238,   229,   182,   268,   142,   236,   336,   337,   338,
     221,   222,   142,   185,   167,   223,   331,   224,   150,   225,
     333,   286,   287,   288,   289,   149,   282,   283,   158,   226,
     348,   284,   285,   241,   269,   242,   350,   343,   142,   352,
     245,   342,   290,   291,   149,   254,   258,   263,   271,   265,
     272,   277,    85,    86,    87,    88,   310,    89,    90,   315,
     320,   346,   327,   197,   198,   199,   200,   201,   202,   203,
     204,   205,   206,   328,   329,   292,   142,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,   344,    91,    92,
      93,   345,    94,    95,    96,    97,    98,    99,   100,   101,
     102,   351,   293,   295,   156,   294,   103,   104,   105,   106,
     107,   108,    85,    86,    87,    88,   207,    89,    90,   296,
     313,   109,    55,   110,   169,    53,   155,   247,   309,   257,
     232,     0,    65,     0,     0,     0,     0,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,     0,    91,    92,
      93,     0,    94,    95,    96,    97,    98,    99,   100,   101,
     102,     0,   140,     0,     0,     0,   103,   104,   105,   106,
     107,   108,    85,    86,    87,    88,     0,    89,    90,     0,
       0,   109,    55,   231,     0,     0,     0,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,     0,    85,    86,
      87,    88,     0,    89,    90,     0,     0,     0,    91,    92,
      93,   141,    94,    95,    96,    97,    98,    99,   100,   101,
     102,     0,     0,     0,     0,     0,   103,   104,   105,   106,
     107,   108,   147,    86,    87,    88,     0,    89,    90,     0,
       0,   109,    55,   233,    91,    92,    93,     0,    94,    95,
      96,    97,    98,    99,   100,   101,   102,     0,     0,     0,
       0,     0,   103,   104,   105,   106,   107,   108,    85,    86,
      87,    88,     0,    89,    90,     0,     0,   109,    55,   299,
       0,     0,     0,     0,     0,     0,   147,    86,    87,    88,
     102,    89,    90,     0,     0,     0,   103,   104,   105,   106,
     107,   108,     0,   147,    86,    87,    88,     0,    89,    90,
       0,     0,   157,   334,    91,    92,    93,     0,    94,    95,
      96,    97,    98,    99,   100,   101,   102,     0,     0,     0,
       0,     0,   103,   104,   105,   106,   107,   108,     0,     0,
     147,    86,    87,    88,   102,    89,    90,   109,    55,     0,
     103,   104,   105,   106,   107,   108,     0,     0,     0,     0,
       0,   102,     0,     0,     0,     0,   157,   103,   104,   105,
     106,   107,   108,     0,     0,     0,     0,     0,     0,     0,
       0,     0,   186,     0,     0,     0,     0,     0,     0,   147,
      86,    87,    88,     0,    89,    90,     0,     0,   102,     0,
       0,     0,     0,     0,   103,   104,   105,   106,   107,   108,
     147,    86,    87,    88,     2,    89,    90,     0,     0,   109,
       8,     9,    10,    11,    12,    13,    14,    15,    16,    17,
      18,    19,    20,    21,   147,    86,    87,    88,     0,    89,
      90,     0,     0,     0,     0,     0,     0,   102,     0,     0,
       0,     0,     0,   103,   104,   105,   106,   107,   108,   147,
      86,    87,    88,     0,    89,    90,     0,     0,   102,     0,
       0,   148,     0,     0,   103,   104,   105,   106,   107,   108,
     147,    86,    87,    88,     0,    89,    90,     0,     0,     0,
       0,     0,   102,   273,     0,     0,     0,     0,   103,   104,
     105,   106,   107,   108,   147,    86,    87,    88,     0,    89,
      90,     0,     0,     0,     0,     0,     0,   102,     0,     0,
     303,     0,     0,   103,   104,   105,   106,   107,   108,   147,
      86,    87,    88,     0,    89,    90,     0,     0,   102,     0,
       0,   332,     0,     0,   103,   104,   105,   106,   107,   108,
     147,    86,    87,    88,     0,    89,    90,     0,     0,     0,
       0,     0,   102,   340,     0,     0,     0,     0,   103,   104,
     105,   106,   107,   108,   147,    86,    87,    88,     0,    89,
      90,     0,     0,     0,     0,     0,     0,   171,     0,     0,
       0,     0,     0,   103,   104,   105,   106,   107,   108,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   173,     0,
       0,     0,     0,     0,   103,   104,   105,   106,   107,   108,
      64,     0,     0,     1,     0,     0,     0,     0,     0,     0,
       0,     0,   102,     0,     0,     0,     0,     0,   103,   104,
     105,   106,   107,   108,     0,     0,     0,     0,     2,     3,
       4,     5,     6,     7,     8,     9,    10,    11,    12,    13,
      14,    15,    16,    17,    18,    19,    20,    21,     1,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,    22,     0,     0,     0,     0,     0,     0,    23,     0,
       0,     0,     0,     2,     3,     4,     5,     6,     7,     8,
       9,    10,    11,    12,    13,    14,    15,    16,    17,    18,
      19,    20,    21,     1,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,   235,   300,   236,     0,
       0,     0,     0,    23,     0,     0,     0,     0,     2,     3,
       4,     5,     6,     7,     8,     9,    10,    11,    12,    13,
      14,    15,    16,    17,    18,    19,    20,    21,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,    22,     0,     2,     0,     0,     0,     0,    23,     8,
       9,    10,    11,    12,    13,    14,    15,    16,    17,    18,
      19,    20,    21,     2,     0,     0,     0,     0,     0,     8,
       9,    10,    11,    12,    13,    14,    15,    16,    17,    18,
      19,    20,    21,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     2,     0,     0,     0,     0,   162,
       8,     9,    10,    11,    12,    13,    14,    15,    16,    17,
      18,    19,    20,    21,     0,     0,     0,     0,     0,   255,
       2,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    14,    15,    16,    17,    18,    19,    20,    21,
       2,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    14,    15,    16,    17,    18,    19,    20,    21,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    75,     0,    55,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,    55,     2,     3,     4,     5,
       6,     7,     8,     9,    10,    11,    12,    13,    14,    15,
      16,    17,    18,    19,    20,    21,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   268,
     300,   236,     0,     0,     0,     0,    23,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,   330,     2,     3,     4,     5,     6,     7,     8,     9,
      10,    11,    12,    13,    14,    15,    16,    17,    18,    19,
      20,    21,   308,     2,     3,     4,     5,     6,     7,     8,
       9,    10,    11,    12,    13,    14,    15,    16,    17,    18,
      19,    20,    21
};

static const yytype_int16 yycheck[] =
{
       0,    61,    34,    62,   101,   102,   182,     3,     0,    78,
      62,    79,     3,    82,    22,   238,    96,    25,    17,    23,
       3,     3,    75,   114,   142,    52,    26,    27,   157,     3,
      81,    31,    91,   102,    91,    35,    88,    89,    90,    91,
      83,    45,    66,    35,     3,    66,   269,    62,     3,    57,
       3,    78,    79,   133,    28,    82,    83,    64,     3,    66,
      84,    61,   114,    84,    61,    73,    63,    23,    60,    28,
      61,   189,    83,    81,   171,   102,   173,    68,    61,    61,
      79,   178,   179,   180,    61,    77,    68,    66,   264,    45,
     170,    82,    61,   152,    63,   152,    52,   177,   195,    66,
     152,   169,   171,    82,   157,   164,    61,   164,    61,    83,
      63,    81,   164,    68,    66,    68,    61,    84,    63,   210,
     211,   212,    78,    79,    83,    80,    82,    83,    12,    13,
      82,   228,    69,    70,   142,    66,    66,    66,   142,    62,
     132,   194,   169,    66,   171,    49,   102,     7,     8,     9,
      80,    82,   232,    82,    58,   208,    10,    11,   210,   211,
     212,   213,   214,   215,   216,   217,   218,   219,   220,   221,
     222,   223,   224,   225,   226,   227,   229,   236,   258,   236,
     271,    32,   311,    68,   236,   189,    42,    43,    73,    74,
      62,    75,    76,    80,    66,   254,    62,   254,    49,    80,
      66,    61,   254,    63,    62,    65,   238,    62,    66,    60,
       3,    66,    68,   169,    61,   171,    63,    82,    62,   271,
      61,    68,    66,   320,   321,    62,    77,   235,    62,    66,
      61,   235,    66,    61,    61,   235,    63,   317,   318,   319,
      14,    15,   242,    82,   252,    67,   306,    77,   307,    78,
     307,   217,   218,   219,   220,   307,   213,   214,   311,    16,
     340,   215,   216,    62,   268,    66,   346,   326,   268,   349,
      64,   324,   221,   222,   326,    80,    80,    54,    62,    82,
       3,     3,     3,     4,     5,     6,     3,     8,     9,    62,
      61,    52,    62,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    62,    64,   223,   306,    28,    29,    30,
      31,    32,    33,    34,    35,    36,    37,    38,    39,    40,
      41,    42,    43,    44,    45,    46,    47,    62,    49,    50,
      51,    64,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    82,   224,   226,    73,   225,    67,    68,    69,    70,
      71,    72,     3,     4,     5,     6,    81,     8,     9,   227,
     252,    82,    83,    84,    83,    29,    69,   153,   242,   171,
     132,    -1,    35,    -1,    -1,    -1,    -1,    28,    29,    30,
      31,    32,    33,    34,    35,    36,    37,    38,    39,    40,
      41,    42,    43,    44,    45,    46,    47,    -1,    49,    50,
      51,    -1,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    -1,     3,    -1,    -1,    -1,    67,    68,    69,    70,
      71,    72,     3,     4,     5,     6,    -1,     8,     9,    -1,
      -1,    82,    83,    84,    -1,    -1,    -1,    28,    29,    30,
      31,    32,    33,    34,    35,    36,    37,    38,    39,    40,
      41,    42,    43,    44,    45,    46,    47,    -1,     3,     4,
       5,     6,    -1,     8,     9,    -1,    -1,    -1,    49,    50,
      51,    62,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    -1,    -1,    -1,    -1,    -1,    67,    68,    69,    70,
      71,    72,     3,     4,     5,     6,    -1,     8,     9,    -1,
      -1,    82,    83,    84,    49,    50,    51,    -1,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    -1,    -1,    -1,
      -1,    -1,    67,    68,    69,    70,    71,    72,     3,     4,
       5,     6,    -1,     8,     9,    -1,    -1,    82,    83,    84,
      -1,    -1,    -1,    -1,    -1,    -1,     3,     4,     5,     6,
      61,     8,     9,    -1,    -1,    -1,    67,    68,    69,    70,
      71,    72,    -1,     3,     4,     5,     6,    -1,     8,     9,
      -1,    -1,    83,    84,    49,    50,    51,    -1,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    -1,    -1,    -1,
      -1,    -1,    67,    68,    69,    70,    71,    72,    -1,    -1,
       3,     4,     5,     6,    61,     8,     9,    82,    83,    -1,
      67,    68,    69,    70,    71,    72,    -1,    -1,    -1,    -1,
      -1,    61,    -1,    -1,    -1,    -1,    83,    67,    68,    69,
      70,    71,    72,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    82,    -1,    -1,    -1,    -1,    -1,    -1,     3,
       4,     5,     6,    -1,     8,     9,    -1,    -1,    61,    -1,
      -1,    -1,    -1,    -1,    67,    68,    69,    70,    71,    72,
       3,     4,     5,     6,    28,     8,     9,    -1,    -1,    82,
      34,    35,    36,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    46,    47,     3,     4,     5,     6,    -1,     8,
       9,    -1,    -1,    -1,    -1,    -1,    -1,    61,    -1,    -1,
      -1,    -1,    -1,    67,    68,    69,    70,    71,    72,     3,
       4,     5,     6,    -1,     8,     9,    -1,    -1,    61,    -1,
      -1,    64,    -1,    -1,    67,    68,    69,    70,    71,    72,
       3,     4,     5,     6,    -1,     8,     9,    -1,    -1,    -1,
      -1,    -1,    61,    62,    -1,    -1,    -1,    -1,    67,    68,
      69,    70,    71,    72,     3,     4,     5,     6,    -1,     8,
       9,    -1,    -1,    -1,    -1,    -1,    -1,    61,    -1,    -1,
      64,    -1,    -1,    67,    68,    69,    70,    71,    72,     3,
       4,     5,     6,    -1,     8,     9,    -1,    -1,    61,    -1,
      -1,    64,    -1,    -1,    67,    68,    69,    70,    71,    72,
       3,     4,     5,     6,    -1,     8,     9,    -1,    -1,    -1,
      -1,    -1,    61,    62,    -1,    -1,    -1,    -1,    67,    68,
      69,    70,    71,    72,     3,     4,     5,     6,    -1,     8,
       9,    -1,    -1,    -1,    -1,    -1,    -1,    61,    -1,    -1,
      -1,    -1,    -1,    67,    68,    69,    70,    71,    72,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    61,    -1,
      -1,    -1,    -1,    -1,    67,    68,    69,    70,    71,    72,
       0,    -1,    -1,     3,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    61,    -1,    -1,    -1,    -1,    -1,    67,    68,
      69,    70,    71,    72,    -1,    -1,    -1,    -1,    28,    29,
      30,    31,    32,    33,    34,    35,    36,    37,    38,    39,
      40,    41,    42,    43,    44,    45,    46,    47,     3,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    61,    -1,    -1,    -1,    -1,    -1,    -1,    68,    -1,
      -1,    -1,    -1,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,     3,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    61,    62,    63,    -1,
      -1,    -1,    -1,    68,    -1,    -1,    -1,    -1,    28,    29,
      30,    31,    32,    33,    34,    35,    36,    37,    38,    39,
      40,    41,    42,    43,    44,    45,    46,    47,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    61,    -1,    28,    -1,    -1,    -1,    -1,    68,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    28,    -1,    -1,    -1,    -1,    -1,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    28,    -1,    -1,    -1,    -1,    84,
      34,    35,    36,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    46,    47,    -1,    -1,    -1,    -1,    -1,    84,
      28,    29,    30,    31,    32,    33,    34,    35,    36,    37,
      38,    39,    40,    41,    42,    43,    44,    45,    46,    47,
      28,    29,    30,    31,    32,    33,    34,    35,    36,    37,
      38,    39,    40,    41,    42,    43,    44,    45,    46,    47,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    81,    -1,    83,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    83,    28,    29,    30,    31,
      32,    33,    34,    35,    36,    37,    38,    39,    40,    41,
      42,    43,    44,    45,    46,    47,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    61,
      62,    63,    -1,    -1,    -1,    -1,    68,    28,    29,    30,
      31,    32,    33,    34,    35,    36,    37,    38,    39,    40,
      41,    42,    43,    44,    45,    46,    47,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    62,    28,    29,    30,    31,    32,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    48,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     3,    28,    29,    30,    31,    32,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    61,    68,   107,   108,   111,   112,   113,   114,
     121,   124,   125,   126,   127,   148,   149,   150,     3,    28,
      83,   120,   125,   124,   127,   128,    82,   109,   110,   125,
     108,   108,    83,   120,   108,    83,   107,   108,   140,   141,
     142,    61,    63,   126,     0,   149,     3,   122,   123,    83,
      62,   124,   127,    66,    82,    81,   141,   142,   112,   115,
     116,   117,   124,    83,   125,     3,     4,     5,     6,     8,
       9,    49,    50,    51,    53,    54,    55,    56,    57,    58,
      59,    60,    61,    67,    68,    69,    70,    71,    72,    82,
      84,    86,    87,    89,    90,    91,    92,    93,    94,    95,
      96,    97,    98,    99,   100,   101,   102,   103,   105,   138,
     139,   141,   142,   143,   144,   145,   146,   147,   107,   141,
       3,    62,   108,   129,   130,   131,   132,     3,    64,    89,
     102,   106,    81,    66,    84,   122,   110,    83,   103,   136,
     141,   117,    84,   116,    80,   118,   119,   125,   117,   115,
      80,    61,    89,    61,    89,    89,   106,    80,    61,    61,
      61,   138,    61,     3,    82,    82,    82,   105,   105,   117,
     133,     7,     8,     9,    61,    63,    65,    18,    19,    20,
      21,    22,    23,    24,    25,    26,    27,    81,   104,    91,
      68,    73,    74,    69,    70,    10,    11,    12,    13,    75,
      76,    14,    15,    67,    77,    78,    16,    17,    79,    66,
      82,    84,   143,    84,   138,    61,    63,   125,   127,   134,
     135,    62,    66,    62,    66,    64,   106,   123,    84,   136,
     137,   106,    66,    82,    80,    84,   138,   133,    80,   138,
     105,   105,   105,    54,   144,    82,    82,    62,    61,   127,
     134,    62,     3,    62,    88,   103,   105,     3,   103,    91,
      91,    91,    92,    92,    93,    93,    94,    94,    94,    94,
      95,    95,    96,    97,    98,    99,   100,   105,   103,    84,
      62,   129,   134,    64,   106,   135,    61,    63,    48,   131,
       3,    66,    84,   119,   106,    62,   138,    62,    62,    62,
      61,   144,    91,    62,    66,    64,    80,    62,    62,    64,
      62,   129,    64,   106,    84,   136,   138,   138,   138,   105,
      62,   105,   103,   102,    62,    64,    52,    62,   138,    62,
     138,    82,   138
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  */

#define YYFAIL		goto yyerrlab

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      yytoken = YYTRANSLATE (yychar);				\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *bottom, yytype_int16 *top)
#else
static void
yy_stack_print (bottom, top)
    yytype_int16 *bottom;
    yytype_int16 *top;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; bottom <= top; ++bottom)
    YYFPRINTF (stderr, " %d", *bottom);
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      fprintf (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       		       );
      fprintf (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif



#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into YYRESULT an error message about the unexpected token
   YYCHAR while in state YYSTATE.  Return the number of bytes copied,
   including the terminating null byte.  If YYRESULT is null, do not
   copy anything; just return the number of bytes that would be
   copied.  As a special case, return 0 if an ordinary "syntax error"
   message will do.  Return YYSIZE_MAXIMUM if overflow occurs during
   size calculation.  */
static YYSIZE_T
yysyntax_error (char *yyresult, int yystate, int yychar)
{
  int yyn = yypact[yystate];

  if (! (YYPACT_NINF < yyn && yyn <= YYLAST))
    return 0;
  else
    {
      int yytype = YYTRANSLATE (yychar);
      YYSIZE_T yysize0 = yytnamerr (0, yytname[yytype]);
      YYSIZE_T yysize = yysize0;
      YYSIZE_T yysize1;
      int yysize_overflow = 0;
      enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
      char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
      int yyx;

# if 0
      /* This is so xgettext sees the translatable formats that are
	 constructed on the fly.  */
      YY_("syntax error, unexpected %s");
      YY_("syntax error, unexpected %s, expecting %s");
      YY_("syntax error, unexpected %s, expecting %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s");
# endif
      char *yyfmt;
      char const *yyf;
      static char const yyunexpected[] = "syntax error, unexpected %s";
      static char const yyexpecting[] = ", expecting %s";
      static char const yyor[] = " or %s";
      char yyformat[sizeof yyunexpected
		    + sizeof yyexpecting - 1
		    + ((YYERROR_VERBOSE_ARGS_MAXIMUM - 2)
		       * (sizeof yyor - 1))];
      char const *yyprefix = yyexpecting;

      /* Start YYX at -YYN if negative to avoid negative indexes in
	 YYCHECK.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;

      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yycount = 1;

      yyarg[0] = yytname[yytype];
      yyfmt = yystpcpy (yyformat, yyunexpected);

      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
	if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR)
	  {
	    if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
	      {
		yycount = 1;
		yysize = yysize0;
		yyformat[sizeof yyunexpected - 1] = '\0';
		break;
	      }
	    yyarg[yycount++] = yytname[yyx];
	    yysize1 = yysize + yytnamerr (0, yytname[yyx]);
	    yysize_overflow |= (yysize1 < yysize);
	    yysize = yysize1;
	    yyfmt = yystpcpy (yyfmt, yyprefix);
	    yyprefix = yyor;
	  }

      yyf = YY_(yyformat);
      yysize1 = yysize + yystrlen (yyf);
      yysize_overflow |= (yysize1 < yysize);
      yysize = yysize1;

      if (yysize_overflow)
	return YYSIZE_MAXIMUM;

      if (yyresult)
	{
	  /* Avoid sprintf, as that infringes on the user's name space.
	     Don't have undefined behavior even if the translation
	     produced a string with the wrong number of "%s"s.  */
	  char *yyp = yyresult;
	  int yyi = 0;
	  while ((*yyp = *yyf) != '\0')
	    {
	      if (*yyp == '%' && yyf[1] == 's' && yyi < yycount)
		{
		  yyp += yytnamerr (yyp, yyarg[yyi++]);
		  yyf += 2;
		}
	      else
		{
		  yyp++;
		  yyf++;
		}
	    }
	}
      return yysize;
    }
}
#endif /* YYERROR_VERBOSE */


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}


/* Prevent warnings from -Wmissing-prototypes.  */

#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */



/* The look-ahead symbol.  */
int yychar;

/* The semantic value of the look-ahead symbol.  */
YYSTYPE yylval;

/* Number of syntax errors so far.  */
int yynerrs;



/*----------.
| yyparse.  |
`----------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{
  
  int yystate;
  int yyn;
  int yyresult;
  /* Number of tokens to shift before error messages enabled.  */
  int yyerrstatus;
  /* Look-ahead token as an internal (translated) token number.  */
  int yytoken = 0;
#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

  /* Three stacks and their tools:
     `yyss': related to states,
     `yyvs': related to semantic values,
     `yyls': related to locations.

     Refer to the stacks thru separate pointers, to allow yyoverflow
     to reallocate them elsewhere.  */

  /* The state stack.  */
  yytype_int16 yyssa[YYINITDEPTH];
  yytype_int16 *yyss = yyssa;
  yytype_int16 *yyssp;

  /* The semantic value stack.  */
  YYSTYPE yyvsa[YYINITDEPTH];
  YYSTYPE *yyvs = yyvsa;
  YYSTYPE *yyvsp;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  YYSIZE_T yystacksize = YYINITDEPTH;

  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;


  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY;		/* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */

  yyssp = yyss;
  yyvsp = yyvs;

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;


	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),

		    &yystacksize);

	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss);
	YYSTACK_RELOCATE (yyvs);

#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;


      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     look-ahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to look-ahead token.  */
  yyn = yypact[yystate];
  if (yyn == YYPACT_NINF)
    goto yydefault;

  /* Not known => get a look-ahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid look-ahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yyn == 0 || yyn == YYTABLE_NINF)
	goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the look-ahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token unless it is eof.  */
  if (yychar != YYEOF)
    yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 5:
#line 42 "cparser.y"
    { (yyval) = (yyvsp[(2) - (3)]); ;}
    break;

  case 7:
#line 50 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 8:
#line 58 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 9:
#line 65 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 10:
#line 73 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 11:
#line 80 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 12:
#line 87 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 13:
#line 93 "cparser.y"
    {
  (yyval) = CParserNewNode(POSTFIX_EXPRESSION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 15:
#line 105 "cparser.y"
    {
  (yyval) = CParserNewNode(ARGUMENT_EXPRESSION_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 17:
#line 118 "cparser.y"
    {
  (yyval) = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 18:
#line 124 "cparser.y"
    {
  (yyval) = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 19:
#line 130 "cparser.y"
    {
  (yyval) = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 20:
#line 136 "cparser.y"
    {
  (yyval) = CParserNewNode(UNARY_EXPRESSION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 21:
#line 142 "cparser.y"
    {
  (yyval) = CParserNewNode(UNARY_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
;}
    break;

  case 29:
#line 166 "cparser.y"
    {
  (yyval) = CParserNewNode(CAST_EXPRESSION, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));  
;}
    break;

  case 31:
#line 180 "cparser.y"
    {
  (yyval) = CParserNewNode(MULTIPLICATIVE_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 32:
#line 187 "cparser.y"
    {
  (yyval) = CParserNewNode(MULTIPLICATIVE_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 33:
#line 194 "cparser.y"
    {
  (yyval) = CParserNewNode(MULTIPLICATIVE_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 35:
#line 207 "cparser.y"
    {
  (yyval) = CParserNewNode(ADDITIVE_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 36:
#line 214 "cparser.y"
    {
  (yyval) = CParserNewNode(ADDITIVE_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 38:
#line 227 "cparser.y"
    {
  (yyval) = CParserNewNode(SHIFT_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 39:
#line 234 "cparser.y"
    {
  (yyval) = CParserNewNode(SHIFT_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 41:
#line 247 "cparser.y"
    {
  (yyval) = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 42:
#line 254 "cparser.y"
    {
  (yyval) = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 43:
#line 261 "cparser.y"
    {
  (yyval) = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 44:
#line 268 "cparser.y"
    {
  (yyval) = CParserNewNode(RELATIONAL_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 46:
#line 281 "cparser.y"
    {
  (yyval) = CParserNewNode(EQUALITY_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 47:
#line 288 "cparser.y"
    {
  (yyval) = CParserNewNode(EQUALITY_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 49:
#line 301 "cparser.y"
    {
  (yyval) = CParserNewNode(AND_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 51:
#line 314 "cparser.y"
    {
  (yyval) = CParserNewNode(XOR_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 53:
#line 327 "cparser.y"
    {
  (yyval) = CParserNewNode(OR_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 55:
#line 340 "cparser.y"
    {
  (yyval) = CParserNewNode(LOGICAL_AND_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 57:
#line 353 "cparser.y"
    {
  (yyval) = CParserNewNode(LOGICAL_OR_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 59:
#line 366 "cparser.y"
    {
  (yyval) = CParserNewNode(CONDITIONAL_EXPRESSION, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (5)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (5)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (5)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (5)]));
;}
    break;

  case 61:
#line 380 "cparser.y"
    {
  (yyval) = CParserNewNode(ASSIGNMENT_EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 74:
#line 409 "cparser.y"
    {
  (yyval) = CParserNewNode(EXPRESSION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 76:
#line 427 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION, 1);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
;}
    break;

  case 77:
#line 432 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserHandleDeclaration((yyval));
;}
    break;

  case 78:
#line 444 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_SPECIFIERS, 1);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (1)]));
;}
    break;

  case 79:
#line 449 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_SPECIFIERS, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 80:
#line 455 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_SPECIFIERS, 1);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (1)]));
;}
    break;

  case 81:
#line 460 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_SPECIFIERS, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 82:
#line 466 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_SPECIFIERS, 1);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (1)]));
;}
    break;

  case 83:
#line 471 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_SPECIFIERS, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 85:
#line 483 "cparser.y"
    {
  (yyval) = CParserNewNode(INIT_DECLARATOR_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 87:
#line 496 "cparser.y"
    {
  (yyval) = CParserNewNode(INIT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 105:
#line 535 "cparser.y"
    {
  (yyval) = CParserNewNode(SU_SPECIFIER, 5);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (5)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (5)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (5)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (5)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (5)]));
  (yyvsp[(2) - (5)])->tokType = TT_IDENTIFIER;
;}
    break;

  case 106:
#line 545 "cparser.y"
    {
  (yyval) = CParserNewNode(SU_SPECIFIER, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 107:
#line 553 "cparser.y"
    {
  (yyval) = CParserNewNode(SU_SPECIFIER, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
  (yyvsp[(2) - (2)])->tokType = TT_IDENTIFIER;
;}
    break;

  case 111:
#line 573 "cparser.y"
    {
  (yyval) = CParserNewNode(STRUCT_DECLARATION_LIST, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 112:
#line 584 "cparser.y"
    {
  (yyval) = CParserNewNode(STRUCT_DECLARATION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 113:
#line 596 "cparser.y"
    {
  (yyval) = CParserNewNode(SPECIFIER_QUALIFIER_LIST, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 115:
#line 603 "cparser.y"
    {
  (yyval) = CParserNewNode(SPECIFIER_QUALIFIER_LIST, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 118:
#line 616 "cparser.y"
    {
  (yyval) = CParserNewNode(STRUCT_DECLARATOR_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 120:
#line 629 "cparser.y"
    {
  (yyval) = CParserNewNode(STRUCT_DECLARATOR, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 121:
#line 635 "cparser.y"
    {
  (yyval) = CParserNewNode(STRUCT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 124:
#line 652 "cparser.y"
    {
  (yyval) = CParserNewNode(ENUM_SPECIFIER, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 125:
#line 660 "cparser.y"
    {
  (yyval) = CParserNewNode(ENUM_SPECIFIER, 5);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (5)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (5)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (5)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (5)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (5)]));
  (yyvsp[(2) - (5)])->tokType = TT_IDENTIFIER;
;}
    break;

  case 126:
#line 670 "cparser.y"
    {
  (yyval) = CParserNewNode(ENUM_SPECIFIER, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
  (yyvsp[(2) - (2)])->tokType = TT_IDENTIFIER;
;}
    break;

  case 128:
#line 683 "cparser.y"
    {
  (yyval) = CParserNewNode(ENUMERATOR_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 130:
#line 696 "cparser.y"
    {
  (yyval) = CParserNewNode(ENUMERATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 133:
#line 715 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATOR, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 136:
#line 728 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 137:
#line 735 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_DECLARATOR, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 138:
#line 743 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 139:
#line 750 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_DECLARATOR, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 140:
#line 758 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_DECLARATOR, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 141:
#line 766 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 143:
#line 779 "cparser.y"
    {
  (yyval) = CParserNewNode(POINTER, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 144:
#line 785 "cparser.y"
    {
  (yyval) = CParserNewNode(POINTER, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 145:
#line 791 "cparser.y"
    {
  (yyval) = CParserNewNode(POINTER, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 147:
#line 804 "cparser.y"
    {
  (yyval) = CParserNewNode(TYPE_QUALIFIER_LIST, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 149:
#line 817 "cparser.y"
    {
  (yyval) = CParserNewNode(PARAMETER_TYPE_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 151:
#line 830 "cparser.y"
    {
  (yyval) = CParserNewNode(PARAMETER_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 152:
#line 842 "cparser.y"
    {
  (yyval) = CParserNewNode(PARAMETER_DECLARATION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 153:
#line 848 "cparser.y"
    {
  (yyval) = CParserNewNode(PARAMETER_DECLARATION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 156:
#line 861 "cparser.y"
    {
  (yyval) = CParserNewNode(IDENTIFIER_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 158:
#line 874 "cparser.y"
    {
  (yyval) = CParserNewNode(TYPE_NAME_TYPE, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 161:
#line 887 "cparser.y"
    {
  (yyval) = CParserNewNode(ABSTRACT_DECLARATOR, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 162:
#line 898 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 163:
#line 905 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 164:
#line 911 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 165:
#line 918 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 166:
#line 925 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 167:
#line 933 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 168:
#line 939 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 169:
#line 946 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 170:
#line 953 "cparser.y"
    {
  (yyval) = CParserNewNode(DIRECT_ABSTRACT_DECLARATOR, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 172:
#line 967 "cparser.y"
    {
  (yyval) = CParserNewNode(INITIALIZER, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 173:
#line 974 "cparser.y"
    {
  (yyval) = CParserNewNode(INITIALIZER, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 175:
#line 988 "cparser.y"
    {
  (yyval) = CParserNewNode(INITIALIZER_LIST, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 182:
#line 1011 "cparser.y"
    {
  (yyval) = CParserNewNode(LABELED_STATEMENT, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 183:
#line 1018 "cparser.y"
    {
  (yyval) = CParserNewNode(LABELED_STATEMENT, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 184:
#line 1026 "cparser.y"
    {
  (yyval) = CParserNewNode(LABELED_STATEMENT, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 185:
#line 1038 "cparser.y"
    {
  pushNamespace();
;}
    break;

  case 186:
#line 1045 "cparser.y"
    {
  (yyval) = CParserNewNode(COMPOUND_STATEMENT, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
  popNamespace();
;}
    break;

  case 187:
#line 1052 "cparser.y"
    {
  (yyval) = CParserNewNode(COMPOUND_STATEMENT, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
  popNamespace();
;}
    break;

  case 188:
#line 1060 "cparser.y"
    {
  (yyval) = CParserNewNode(COMPOUND_STATEMENT, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
  popNamespace();
;}
    break;

  case 189:
#line 1068 "cparser.y"
    {
  (yyval) = CParserNewNode(COMPOUND_STATEMENT, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
  popNamespace();
;}
    break;

  case 190:
#line 1082 "cparser.y"
    {
  /* I don't usually do this, but this helps handlers disambiguate K&R
     style fucntion definitions alot. */
  (yyval) = CParserNewNode(DECLARATION_LIST, 1);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (1)]));
;}
    break;

  case 191:
#line 1089 "cparser.y"
    {
  (yyval) = CParserNewNode(DECLARATION_LIST, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 193:
#line 1101 "cparser.y"
    {
  (yyval) = CParserNewNode(STATEMENT_LIST, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 195:
#line 1113 "cparser.y"
    {
  (yyval) = CParserNewNode(EXPRESSION_STATEMENT, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 196:
#line 1124 "cparser.y"
    {
  (yyval) = CParserNewNode(SELECTION_STATEMENT, 5);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (5)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (5)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (5)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (5)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (5)]));
;}
    break;

  case 197:
#line 1133 "cparser.y"
    {
  (yyval) = CParserNewNode(SELECTION_STATEMENT, 7);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (7)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (7)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (7)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (7)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (7)]));
  CParserSetChild((yyval), 5, (yyvsp[(6) - (7)]));
  CParserSetChild((yyval), 6, (yyvsp[(7) - (7)]));
;}
    break;

  case 198:
#line 1144 "cparser.y"
    {
  (yyval) = CParserNewNode(SELECTION_STATEMENT, 5);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (5)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (5)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (5)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (5)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (5)]));
;}
    break;

  case 199:
#line 1158 "cparser.y"
    {
  (yyval) = CParserNewNode(ITERATION_STATEMENT, 5);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (5)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (5)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (5)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (5)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (5)]));
;}
    break;

  case 200:
#line 1167 "cparser.y"
    {
  (yyval) = CParserNewNode(ITERATION_STATEMENT, 7);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (7)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (7)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (7)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (7)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (7)]));
  CParserSetChild((yyval), 5, (yyvsp[(6) - (7)]));
  CParserSetChild((yyval), 6, (yyvsp[(7) - (7)]));
;}
    break;

  case 201:
#line 1178 "cparser.y"
    {
  (yyval) = CParserNewNode(ITERATION_STATEMENT, 6);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (6)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (6)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (6)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (6)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (6)]));
  CParserSetChild((yyval), 5, (yyvsp[(6) - (6)]));
;}
    break;

  case 202:
#line 1188 "cparser.y"
    {
  (yyval) = CParserNewNode(ITERATION_STATEMENT, 7);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (7)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (7)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (7)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (7)]));
  CParserSetChild((yyval), 4, (yyvsp[(5) - (7)]));
  CParserSetChild((yyval), 5, (yyvsp[(6) - (7)]));
  CParserSetChild((yyval), 6, (yyvsp[(7) - (7)]));
;}
    break;

  case 203:
#line 1204 "cparser.y"
    {
  (yyval) = CParserNewNode(JUMP_STATEMENT, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 204:
#line 1211 "cparser.y"
    {
  (yyval) = CParserNewNode(JUMP_STATEMENT, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 205:
#line 1217 "cparser.y"
    {
  (yyval) = CParserNewNode(JUMP_STATEMENT, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 206:
#line 1223 "cparser.y"
    {
  (yyval) = CParserNewNode(JUMP_STATEMENT, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;

  case 207:
#line 1229 "cparser.y"
    {
  (yyval) = CParserNewNode(JUMP_STATEMENT, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 208:
#line 1241 "cparser.y"
    {
  (yyval) = (yyvsp[(1) - (1)]);
  CParserSetRoot((yyvsp[(1) - (1)]));
;}
    break;

  case 209:
#line 1246 "cparser.y"
    {
  (yyval) = CParserNewNode(TRANSLATION_UNIT, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
  CParserSetRoot((yyval));
;}
    break;

  case 212:
#line 1265 "cparser.y"
    {
  (yyval) = CParserNewNode(FUNCTION_DEFINITION, 4);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (4)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (4)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (4)]));
  CParserSetChild((yyval), 3, (yyvsp[(4) - (4)]));
;}
    break;

  case 213:
#line 1273 "cparser.y"
    {
  (yyval) = CParserNewNode(FUNCTION_DEFINITION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 214:
#line 1280 "cparser.y"
    {
  (yyval) = CParserNewNode(FUNCTION_DEFINITION, 3);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (3)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (3)]));
  CParserSetChild((yyval), 2, (yyvsp[(3) - (3)]));
;}
    break;

  case 215:
#line 1287 "cparser.y"
    {
  (yyval) = CParserNewNode(FUNCTION_DEFINITION, 2);
  CParserSetChild((yyval), 0, (yyvsp[(1) - (2)]));
  CParserSetChild((yyval), 1, (yyvsp[(2) - (2)]));
;}
    break;


/* Line 1267 of yacc.c.  */
#line 3213 "cparser.tab.c"
      default: break;
    }
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;


  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
      {
	YYSIZE_T yysize = yysyntax_error (0, yystate, yychar);
	if (yymsg_alloc < yysize && yymsg_alloc < YYSTACK_ALLOC_MAXIMUM)
	  {
	    YYSIZE_T yyalloc = 2 * yysize;
	    if (! (yysize <= yyalloc && yyalloc <= YYSTACK_ALLOC_MAXIMUM))
	      yyalloc = YYSTACK_ALLOC_MAXIMUM;
	    if (yymsg != yymsgbuf)
	      YYSTACK_FREE (yymsg);
	    yymsg = (char *) YYSTACK_ALLOC (yyalloc);
	    if (yymsg)
	      yymsg_alloc = yyalloc;
	    else
	      {
		yymsg = yymsgbuf;
		yymsg_alloc = sizeof yymsgbuf;
	      }
	  }

	if (0 < yysize && yysize <= yymsg_alloc)
	  {
	    (void) yysyntax_error (yymsg, yystate, yychar);
	    yyerror (yymsg);
	  }
	else
	  {
	    yyerror (YY_("syntax error"));
	    if (yysize != 0)
	      goto yyexhaustedlab;
	  }
      }
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse look-ahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse look-ahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (yyn != YYPACT_NINF)
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  *++yyvsp = yylval;


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#ifndef yyoverflow
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEOF && yychar != YYEMPTY)
     yydestruct ("Cleanup: discarding lookahead",
		 yytoken, &yylval);
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}


#line 1294 "cparser.y"

#include <stdio.h>

extern char cparsertext[];
extern int cparser_column;

int cparsererror (char * s)
{
        fflush(stdout);
        printf("\n%*s\n%*s\n", cparser_column, "^", cparser_column, s);
        return 0;
}

