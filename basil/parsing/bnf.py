#! /usr/bin/env python
#__________________________________________________________
"""Module bnf

Parser for a BNF-ish grammar description file.  Command line usage:
	% bnf.py <input file>

$Id: bnf.py,v 1.1 2001/09/24 04:13:21 jriehl Exp $
"""
#__________________________________________________________

__DEBUG__ = 0

#__________________________________________________________

import re
import string

#__________________________________________________________

token = "[A-Za-z0-9_]+"
restring = "\"[^\"]*[^\\\\]\""
ws = "[ \t\n\r]*"
ts = "(" + restring + "|" + token + ")"
rule = "(" + ws + ts + ")*"
rules = rule + "(" + ws + "\|" + rule + ")*" + ws
production = "(" + token + ")" + ws + ":(" + rules + ");" + ws

#__________________________________________________________

token_obj = re.compile (token)
ts_obj = re.compile (ts)
rule_obj = re.compile (rule)
rules_obj = re.compile (rules)
prod_obj = re.compile (production)

#__________________________________________________________

def get_prods (text):
  """get_prods (text):
  Extracts productions from a set of BNF productions in
  the passed string in text.  Returns a dictionary mapping
  a string to a list of lists of strings.
  ex. { 'nonterminal' : [['term1','term2'],['nonterm1']],
        'nonterm1' : [['term3','nonterminal','term4']] }
  """
  prod_dict = {}
  srch_res = prod_obj.search(text)
  first_key = ''
  #________________________________________________________
  while srch_res != None:
    next_srch = srch_res.end()
    if __DEBUG__:
      print
      print "_" * 60
      print srch_res.group(0)
      print srch_res.group(1)
      print srch_res.group(2)
      print "_" * 60
    #______________________________________________________
    prod_key = srch_res.group(1)
    prod_text = srch_res.group(2)
    if first_key == '':
      first_key = prod_key
    prod_set = []
    rules = string.split(prod_text, "|")
    for rule in rules:
      ruleSet = []
      index = 0
      tsResult = ts_obj.search(rule)
      while tsResult != None:
        ruleSet.append(tsResult.group())
	index = tsResult.end()
	tsResult = ts_obj.search(rule, index)
      prod_set.append(ruleSet)
    #______________________________________________________
    prod_dict [prod_key] = prod_set
    srch_res = prod_obj.search (text, next_srch)
  #________________________________________________________
  return first_key, prod_dict

#__________________________________________________________

def main ():
   import sys
   if len(sys.argv) > 1:
      text = open(sys.argv[1]).read()
      import pprint
      retVal = get_prods(text)
      pprint.pprint(retVal)
   else:
      print __doc__

#________________________________________________

if __name__ == "__main__":
   main()

#__________________________________________________________
# End of bnf.py

