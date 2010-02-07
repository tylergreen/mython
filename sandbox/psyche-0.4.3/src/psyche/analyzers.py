#
# This file is part of Psyche, the Python Scheme Interpreter
#
# Copyright (c) 2002
#       Yigal Duppen
#
# Psyche is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Psyche is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psyche; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
A collection of analyzers.

An analyzer is a visitor for ASTs. They can be used for annotations,
translations etc.
"""

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.6 $"[11:-2]

from spark import GenericASTTraversal


class _TailContextMarker(GenericASTTraversal):
    """The TailContextMarker marks all AST nodes that occur in a tail
    context according to R5RS 3.5.
    """

    def __init__(self, ast):
        GenericASTTraversal.__init__(self, ast)
        self.preorder()

    def typestring(self, node):
        try:
            return node.type
        except AttributeError:
            raise NotImplementedError(
                "Cannot obtain type for node %s of type %s"
                % (node, type(node)))

    def preorder(self, *args):
        GenericASTTraversal.preorder(self, *args)


    def n_Variable(self, node):
        self.prune()

    n_Number = n_Variable
    n_Boolean = n_Variable
    n_String = n_Variable
    n_Character = n_Variable
    n_Symbol = n_Variable
    n_List = n_Variable

    def n_Application(self, node):
        self.prune()

    def n_Definition(self, node):
        self.prune()

    def n_Lambda(self, node):
        node.body()[-1].inTailContext = 1

    def n_ProcDefinition(self, node):
        node.body()[-1].inTailContext = 1

    def n_If(self, node):
        if node.inTailContext:
            c = node.consequent()
            a = node.alternate()
            
            if c:
                c.inTailContext = 1
            if a:
                a.inTailContext = 1
            
    def n_Cond(self, node):
        if node.inTailContext:
            for clause in node.clauses():
                lastExpr = clause.sequence()[-1]
                lastExpr.inTailContext = 1

            seq = node.elseSequence()
            if seq:
                lastExpr = seq[-1]
                lastExpr.inTailContext = 1

    
    def n_And(self, node):
        if node.inTailContext:
            lastExpr = node.tests()[-1]
            if lastExpr:
                lastExpr.inTailContext = 1

    n_Or = n_And



def markTailContexts(ast):
    """Marks thos AST nodes that are in tail context"""
    _TailContextMarker(ast)
    return ast


