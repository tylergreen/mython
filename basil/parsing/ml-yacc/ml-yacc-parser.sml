(* ______________________________________________________________________
   ml-yacc-parser.sml

   Jonathan Riehl

   $Id$
   ______________________________________________________________________ *)

structure MlyaccLrVals = MlyaccLrValsFun(structure Token = LrParser.Token)
structure MlyaccLex = MlyaccLexFun(structure Tokens = MlyaccLrVals.Tokens)
structure MlyaccParser = Join(structure LrParser = LrParser
                              structure ParserData = MlyaccLrVals.ParserData
                              structure Lex = MlyaccLex)

structure MLYaccParserDriver = struct

fun parseFile (fileName) =
    let val inFile = TextIO.openIn fileName
        fun inFn _ = (case (TextIO.inputLine inFile) of
                          SOME s => s
                        | NONE => (TextIO.closeIn inFile; ""))
        val lexer = MlyaccParser.makeLexer inFn
        fun printError (s, i : int, _) =
            TextIO.output(TextIO.stdOut, "Error, line " ^ (Int.toString i) ^
                                         ", " ^ s ^ "\n")
        val concreteParse = #1 (MlyaccParser.parse (0, lexer, printError, ()))
    in
        concreteParse
    end (* fun parseFile *)

end

(* ______________________________________________________________________
   End of ml-yacc-parser.sml
   ______________________________________________________________________ *)
