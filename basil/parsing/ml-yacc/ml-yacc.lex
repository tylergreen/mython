(* ML-Yacc Parser Generator (c) 1989 Andrew W. Appel, David R. Tarditi

   yacc.lex: Lexer specification
 *)

structure Tokens = Tokens
type svalue = Tokens.svalue
type pos = int
type ('a,'b) token = ('a,'b) Tokens.token
type lexresult = (svalue,pos) token

open Tokens

val errorOccurred = ref false
val pr = fn s : string => TextIO.output(TextIO.stdErr, s)

val error = (fn l : pos => fn msg : string =>
             (pr "Error, line "; pr (Int.toString l); pr ": ";
              pr msg; pr "\n"; errorOccurred := true))

val lineno = ref 0
val text = ref (nil: string list)

val pcount = ref 0
val commentLevel = ref 0
val actionstart = ref 0

val eof = fn i => (if (!pcount)>0 then
			error (!actionstart)
			      " eof encountered in action beginning here !"
		   else (); EOF(("EOF",!lineno),!lineno,!lineno))

val Add = fn s => (text := s::(!text))


local val dict = [("%prec",PREC_TAG),("%term",TERM),
	       ("%nonterm",NONTERM), ("%eop",PERCENT_EOP),("%start",START),
	       ("%prefer",PREFER),("%subst",SUBST),("%change",CHANGE),
	       ("%keyword",KEYWORD),("%name",NAME),
	       ("%verbose",VERBOSE), ("%nodefault",NODEFAULT),
	       ("%value",VALUE), ("%noshift",NOSHIFT),
	       ("%header",PERCENT_HEADER),("%pure",PERCENT_PURE),
	       ("%token_sig_info",PERCENT_TOKEN_SIG_INFO),
	       ("%arg",PERCENT_ARG),
	       ("%pos",PERCENT_POS)]
in val lookup =
     fn (s,left,right) =>
	 let fun f ((a,d)::b) =
                 if a=s then d((s, left), left,right) else f b
	       | f nil = UNKNOWN((s, left), left, right)
	 in f dict
	 end
end

fun inc (ri as ref i) = (ri := i+1)
fun dec (ri as ref i) = (ri := i-1)

%%
%header (
         functor MlyaccLexFun(structure Tokens : Mlyacc_TOKENS)
);
%s A CODE F COMMENT STRING EMPTYCOMMENT;
ws = [\t\ ]+;
idchars = [A-Za-z_'0-9];
id=[A-Za-z]{idchars}*;
tyvar="'"{idchars}*;
qualid ={id}".";
%%
<INITIAL>"(*"	=> (Add yytext; YYBEGIN COMMENT; commentLevel := 1;
		    continue() before YYBEGIN INITIAL);
<A>"(*"		=> (YYBEGIN EMPTYCOMMENT; commentLevel := 1; continue());
<CODE>"(*"	=> (Add yytext; YYBEGIN COMMENT; commentLevel := 1;
		    continue() before YYBEGIN CODE);
<INITIAL>[^%\n]+ => (Add yytext; continue());
<INITIAL>"%%"	 => (YYBEGIN A; HEADER ((concat (rev (!text)),!lineno),
                                        !lineno,!lineno));
<INITIAL,CODE,COMMENT,F,EMPTYCOMMENT>\n  => (Add yytext; inc lineno; continue());
<INITIAL>.	 => (Add yytext; continue());

<A>\n		=> (inc lineno; continue ());
<A>{ws}+	=> (continue());
<A>of		=> (OF((yytext,!lineno),!lineno,!lineno));
<A>for		=> (FOR((yytext,!lineno),!lineno,!lineno));
<A>"{"		=> (LBRACE((yytext,!lineno),!lineno,!lineno));
<A>"}"		=> (RBRACE((yytext,!lineno),!lineno,!lineno));
<A>","		=> (COMMA((yytext,!lineno),!lineno,!lineno));
<A>"*"		=> (ASTERISK((yytext,!lineno),!lineno,!lineno));
<A>"->"		=> (ARROW((yytext,!lineno), !lineno,!lineno));
<A>"%left"	=> (PREC(("LEFT",!lineno),!lineno,!lineno));
<A>"%right"	=> (PREC(("RIGHT",!lineno), !lineno,!lineno));
<A>"%nonassoc" 	=> (PREC(("NONASSOC",!lineno),!lineno,!lineno));
<A>"%"[a-z_]+	=> (lookup(yytext,!lineno,!lineno));
<A>{tyvar}	=> (TYVAR((yytext,!lineno),!lineno,!lineno));
<A>{qualid}	=> (IDDOT((yytext,!lineno),!lineno,!lineno));
<A>[0-9]+	=> (INT ((yytext,!lineno),!lineno,!lineno));
<A>"%%"		=> (DELIMITER((yytext,!lineno),!lineno,!lineno));
<A>":"		=> (COLON((yytext,!lineno),!lineno,!lineno));
<A>"|"		=> (BAR((yytext,!lineno),!lineno,!lineno));
<A>{id}		=> (ID ((yytext,!lineno),!lineno,!lineno));
<A>"("		=> (pcount := 1; actionstart := (!lineno);
		    text := nil; YYBEGIN CODE; continue() before YYBEGIN A);
<A>.		=> (UNKNOWN((yytext,!lineno),!lineno,!lineno));
<CODE>"("	=> (inc pcount; Add yytext; continue());
<CODE>")"	=> (dec pcount;
		    if !pcount = 0 then
			 PROG ((concat (rev (!text)),!lineno),!lineno,!lineno)
		    else (Add yytext; continue()));
<CODE>"\""	=> (Add yytext; YYBEGIN STRING; continue());
<CODE>[^()"\n]+	=> (Add yytext; continue());

<COMMENT>[(*)]	=> (Add yytext; continue());
<COMMENT>"*)"	=> (Add yytext; dec commentLevel;
		    if !commentLevel=0
			 then BOGUS_VALUE((yytext,!lineno),!lineno,
                                          !lineno)
			 else continue()
		   );
<COMMENT>"(*"	=> (Add yytext; inc commentLevel; continue());
<COMMENT>[^*()\n]+ => (Add yytext; continue());

<EMPTYCOMMENT>[(*)]  => (continue());
<EMPTYCOMMENT>"*)"   => (dec commentLevel;
		          if !commentLevel=0 then YYBEGIN A else ();
			  continue ());
<EMPTYCOMMENT>"(*"   => (inc commentLevel; continue());
<EMPTYCOMMENT>[^*()\n]+ => (continue());

<STRING>"\""	=> (Add yytext; YYBEGIN CODE; continue());
<STRING>\\	=> (Add yytext; continue());
<STRING>\n	=> (Add yytext; error (!lineno) "unclosed string";
 	            inc lineno; YYBEGIN CODE; continue());
<STRING>[^"\\\n]+ => (Add yytext; continue());
<STRING>\\\"	=> (Add yytext; continue());
<STRING>\\[\ \t\n]   => (Add yytext;
			if substring(yytext,1,1)="\n" then inc lineno else ();
		     	YYBEGIN F; continue());

<F>{ws}		=> (Add yytext; continue());
<F>\\		=> (Add yytext; YYBEGIN STRING; continue());
<F>.		=> (Add yytext; error (!lineno) "unclosed string";
		    YYBEGIN CODE; continue());

