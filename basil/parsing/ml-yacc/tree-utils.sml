(* ______________________________________________________________________
   tree-utils.sml

   Jonathan Riehl

   $Id$
   ______________________________________________________________________ *)

structure TreeUtils = struct

datatype 'a tree = Node of string * 'a tree list
                 | Leaf of 'a

fun mkTreeToString f =
    let fun treeToString (Node(s, c)) =
            (s ^ "(" ^ concat (map treeToString c) ^ ")")
          | treeToString (Leaf(a)) = f a
    in
        treeToString
    end

end

(* ______________________________________________________________________
   End of tree-utils.sml
   ______________________________________________________________________ *)
