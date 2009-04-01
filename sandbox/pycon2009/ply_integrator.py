#! /usr/bin/env python
#experiment for intergration between ply and basil grammars

import mycalcgrammar

myg = mycalcgrammar
tokens = mycalcgrammar.tokens

prodfns = [ getattr(myg,name) for name in myg.__dict__.keys()
            if name.startswith("p_") and name != "p_error" ]

prodstrs = [ f.__doc__ for f in prodfns ]

nts = set() 
print nts
print prodfns
print prodstrs

def parse_production_source (source):
    # Split the production string into individual strings.
    source_list = source.split()
    # Sanity checks.
    assert (len(source_list) > 2) and (source_list[1] == ":")
    nonterminal = source_list[0]
    assert nonterminal not in tokens
    # NOTE: We have to use tuples here, since we can't hash lists when
    # building the multimap.
    rhs = tuple(source_list[2:])
    nts.add(nonterminal)
    return nonterminal, rhs

prodtups = [ parse_production_source(source) for source in prodstrs ]

print nts
print prodtups

# Now build a multimap to rhs's.

prodmap = {}
for nt, rhs in prodtups:
    if nt not in prodmap:
        prodmap[nt] = set()
    prodmap[nt].add(rhs)

import pprint
pprint.pprint(prodmap)

# ______________________________________________________________________
# Another way to do this:

print "_" * 70

from ply.yacc import ParserReflect, parse_grammar

pinfo = ParserReflect(myg.__dict__)
pinfo.get_all()

prodparse = [ parse_grammar(doc_str, file_name, line_no)
              for line_no, file_name, func_name, doc_str in pinfo.pfuncs ]

pprint.pprint(prodparse)

prodmap2 = {}
for parse_result in prodparse:
    for file_name, line_no, nt, rhs in parse_result:
        if nt not in prodmap2:
            prodmap2[nt] = set()
        prodmap2[nt].add(tuple(rhs))

print "_" * 60
pprint.pprint(prodmap2)

assert prodmap == prodmap2

# ______________________________________________________________________
# Let's build a BasilGrammarModel...

from basil.models.grammar import BasilGrammarModel
from basil.models.grammar.InternalizeBNF import BNFInternalizer

model_factory = BasilGrammarModel.getModelFactory()()
internalizer = BNFInternalizer(model_factory)
model = internalizer((pinfo.start, prodmap2))

print model_factory.externalizeXML(model)
