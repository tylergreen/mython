/* ______________________________________________________________________
   pgenmodule.c

   $Id: pgenmodule.c,v 1.2 2003/07/13 00:40:37 jriehl Exp $
   ______________________________________________________________________
   Interface design:

   PgenParserType:
       parseString (s : String) : PgenASTType
       parseFile (filename : String) : PgenASTType
       stringToSymbolMap () : Dict (String => Int)
       symbolToStringMap () : Dict (Int => String)
       getStart () : Int
       setStart (s : Int)

   buildParser (p : PgenASTType) : PgenParserType

   PgenASTType:
       getType () : Int
       getName () : String
       getGrammar () : PgenGrammarType
       toTuple () : Tuple(*)

   metaParser : PgenParserType

   * - Translates to a 2-tuple:
   node = (head, children)
   head = Int | (Int, String) | (Int, String, Int)
          { Non-terminal (type) vs. terminal (type, string, [lineno]) }
   children = [childTuple0, childTuple1, ... childTupleX]

   ______________________________________________________________________
   Portions and ideas:
   *  Copyright 1995-1996 by Fred L. Drake, Jr. and Virginia Polytechnic
   *  Institute and State University, Blacksburg, Virginia, USA.
   *  Portions copyright 1991-1995 by Stichting Mathematisch Centrum,
   *  Amsterdam, The Netherlands.  Copying is permitted under the terms
   *  associated with the main Python distribution, with the additional
   *  restriction that this additional notice be included and maintained
   *  on all distributed copies.
   ______________________________________________________________________ */

#include "Python.h"
#include "node.h"
#include "grammar.h"
#include "parsetok.h"
#include "token.h"
#include "pgenheaders.h"
#include "pgen.h"
#include "bitset.h"

/* ______________________________________________________________________
   Structure declarations.
   ______________________________________________________________________ */

typedef struct {
  PyObject_HEAD
  grammar * grammarPtr;
  int g_start;
  PyObject * symbolMap;
  PyObject * stringMap;
} PgenParserObject;

typedef struct {
  PyObject_HEAD
  node * nodePtr;
  PgenParserObject * parser;
} PgenASTObject;

/* ______________________________________________________________________
   Static data for the module.
   ______________________________________________________________________ */

static PgenParserObject * metaParser = NULL;
static PyObject * pgenError = NULL;

/* ______________________________________________________________________
   Forward function declarations.
   ______________________________________________________________________ */

static PyObject * pgenParser_parseString (PgenParserObject * self,
                                          PyObject * args, PyObject * kw);
static PyObject * pgenParser_parseFile (PgenParserObject * self,
                                        PyObject * args, PyObject * kw);
static PyObject * pgenParser_stringToSymbolMap (PgenParserObject * self,
                                                PyObject * args,
						PyObject * kw);
static PyObject * pgenParser_symbolToStringMap (PgenParserObject * self,
                                                PyObject * args,
						PyObject * kw);
static PyObject * pgenParser_getStart (PgenParserObject * self,
				       PyObject * args, PyObject * kw);
static PyObject * pgenParser_setStart (PgenParserObject * self,
				       PyObject * args, PyObject * kw);
static PyObject * pgenParser_toTuple (PgenParserObject * self,
                                      PyObject * args, PyObject * kw);

static PyObject * pgenAstNew (node * n, PgenParserObject * p);

static void       pgenAstFree (PgenASTObject * ast);

static PyObject * pgenAst_getType (PgenASTObject * self, PyObject * args,
                                   PyObject * kw);
static PyObject * pgenAst_getName (PgenASTObject * self, PyObject * args,
                                   PyObject * kw);
static PyObject * pgenAst_getGrammar (PgenASTObject * self, PyObject * args,
                                      PyObject * kw);
static PyObject * pgenAst_toTuple (PgenASTObject * self, PyObject * args,
                                   PyObject * kw);

/* ______________________________________________________________________
   Utility functions
   ______________________________________________________________________ */

/* Portions of the following function mimics code that is copyright CWI.
   See parsermodule.c, node2tuple(). */

static PyObject * pgen_node2tuple (node * n, int lineno)
{
  PyObject * myNode = NULL;
  int i;
  int addOk;

  if (NULL == n)
    {
      Py_INCREF(Py_None);
      myNode = Py_None;
    }
  else
    {
      PyObject * head = NULL;
      PyObject * children;
      PyObject * child;

      /* Build head */
      if (ISTERMINAL(TYPE(n)))
        {
          PyObject * nodeType;
          PyObject * nodeString;

          nodeType = PyInt_FromLong(TYPE(n));
          nodeString = PyString_FromString(STR(n));
          if ((NULL != nodeType) && (NULL != nodeString))
            {
              if (lineno)
                {
                  head = PyTuple_New(3);
                }
              else
                {
                  head = PyTuple_New(2);
                }
              if (NULL != head)
                {
                  PyTuple_SetItem(head, 0, nodeType);
                  PyTuple_SetItem(head, 1, nodeString);
                  if (lineno)
                    PyTuple_SetItem(head, 2, PyInt_FromLong(n->n_lineno));
                }
            }
        }
      else
        {
          head = PyInt_FromLong(TYPE(n));
        }
      /* Build child list. */
      if (NULL != head)
        {
          /* Build children */
          children = PyList_New(NCH(n));
          if (NULL == children)
            {
              Py_DECREF(head);
            }
          else
            {
              for (i = 0; i < NCH(n); i++)
                {
                  child = pgen_node2tuple(CHILD(n, i), lineno);
                  if (NULL == child) break;
                  addOk = PyList_SetItem(children, i, child);
                  if (-1 == addOk)
                    {
                      Py_DECREF(child);
                      break;
                    }
                }
              if (i < NCH(n))
                {
                  Py_DECREF(head);
                  Py_DECREF(children);
                }
              else
                {
                  /* Construct node. */
                  myNode = PyTuple_New(2);
                  PyTuple_SetItem(myNode, 0, head);
                  PyTuple_SetItem(myNode, 1, children);
                }
            }
        }
    }
  return myNode;
}

/* ______________________________________________________________________ */

static void
freestate (state * s)
{
  if (NULL != s)
    {
      /* Free the state arcs. */
      if (NULL != s->s_arc)
        {
          PyMem_Free(s->s_arc);
          s->s_arc = NULL;
        }
      /* Free the state accelerator. */
      if (NULL != s->s_accel)
        {
          PyMem_Free(s->s_accel);
          s->s_accel = NULL;
        }
    }
}

/* ______________________________________________________________________ */

static void
freedfa (dfa * d)
{
  int i;
  state * s;

  if (NULL != d)
    {
      /* Free the DFA name. */
      if (NULL != d->d_name)
        {
          /* XXX - I'm trying to get PyMem routines to work, but that breaks
             pgen, which doesn't appear to link PyMem_Malloc. */
          free(d->d_name);
          d->d_name = NULL;
        }
      /* Free the DFA states. */
      if (NULL != d->d_state)
        {
          for (s = d->d_state, i = 0; i < d->d_nstates; s++, i++)
            {
              freestate(s);
            }
          PyMem_Free(d->d_state);
          d->d_state = NULL;
        }
    }
}

/* ______________________________________________________________________ */

static void
freegrammar (grammar * gg)
{
  int i;
  dfa * d;
  label * l;

  if (NULL != gg)
    {
      /* Free the DFA's. */
      if (NULL != gg->g_dfa)
	{
	  for (d = gg->g_dfa, i = 0; i < gg->g_ndfas; d++, i++)
	    {
              freedfa(d);
	    }
	  PyMem_Free(gg->g_dfa);
	  gg->g_dfa = NULL;
	}
      /* Free the label list. */
      for (l = gg->g_ll.ll_label, i = 0; i < gg->g_ll.ll_nlabels; l++, i++)
        {
          /* XXX - Same note as for the dfa name above - the label string is
             being allocated using strdup(), not by any of the PyMem
             routines. */
          if (Py_DebugFlag)
            {
              printf("Free label @ %08x, %d: %s\n", (unsigned)&gg->g_ll, i,
                     PyGrammar_LabelRepr(l));
            }
          free(l->lb_str);
        }
      PyMem_Free(gg->g_ll.ll_label);
      /* Free the grammar object itself. */
      PyMem_Free(gg);
    }
}

/* ______________________________________________________________________ */
/* buildSymbolToStringMap()
 */

static PyObject * buildSymbolToStringMap (grammar * g)
{
  PyObject * retVal = NULL;
  dfa * d = g->g_dfa;
  int i;

  /* Iterate over the set of the grammar's DFA's, mapping from
     d->d_type to d->d_name. */
  retVal = PyDict_New();
  if (NULL != retVal)
    {
      for (i = 0; i < g->g_ndfas; i++, d++)
	{
	  if (NULL != d->d_name)
	    {
	      PyDict_SetItem(retVal, PyInt_FromLong(d->d_type),
			     PyString_FromString(d->d_name));
	    }
	}
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* getSymbolToStringMap()
 */

static PyObject * getSymbolToStringMap (PgenParserObject * parser)
{
  PyObject * retVal = NULL;
  if (NULL == parser->symbolMap)
    {
      retVal = buildSymbolToStringMap(parser->grammarPtr);
      if (NULL != retVal)
	{
	  Py_INCREF(retVal);
	  parser->symbolMap = retVal;
	}
    }
  else
    {
      retVal = parser->symbolMap;
      Py_INCREF(retVal);
    }
  return retVal;
}

/* ______________________________________________________________________ */

static int isValidSymbol (grammar * g, int symbolNo)
{
  int retVal = 0;
  int i;
  dfa * d = g->g_dfa;

  for (i = 0; i < g->g_ndfas; i++, d++)
    {
      if (NULL != d->d_name)
	{
	  if (symbolNo == d->d_type)
	    {
	      retVal = 1;
	      break;
	    }
	}
    }
  return retVal;
}

/* ______________________________________________________________________
   PgenParserType.
   ______________________________________________________________________ */

static void
pgenParserFree (PgenParserObject * p)
{
  if (p->grammarPtr != meta_grammar())
    {
      freegrammar(p->grammarPtr);
      if (p->symbolMap != NULL)
	{
	  Py_DECREF(p->symbolMap);
	}
      if (p->stringMap != NULL)
	{
	  Py_DECREF(p->stringMap);
	}
    }
  PyObject_Del(p);
}

/* ______________________________________________________________________ */

static PyMethodDef PgenParserMethods[] = {
  {"parseString", (PyCFunction)pgenParser_parseString, METH_VARARGS, ""},
  {"parseFile", (PyCFunction)pgenParser_parseFile, METH_VARARGS, ""},
  {"stringToSymbolMap", (PyCFunction)pgenParser_stringToSymbolMap,
   METH_VARARGS, ""},
  {"symbolToStringMap", (PyCFunction)pgenParser_symbolToStringMap,
   METH_VARARGS, ""},
  {"getStart", (PyCFunction)pgenParser_getStart, METH_VARARGS, ""},
  {"setStart", (PyCFunction)pgenParser_setStart, METH_VARARGS, ""},
  {"toTuple", (PyCFunction)pgenParser_toTuple, METH_VARARGS, ""},
  {NULL, NULL, 0, NULL}
};

static PyObject *
pgenParserGetAttr (PgenParserObject * obj, char * name)
{
  return Py_FindMethod(PgenParserMethods, (PyObject *)obj, name);
}

/* ______________________________________________________________________ */
/* XXX - Punt for now. */

static int
pgenParserCompare (PgenParserObject * left, PgenParserObject * right)
{
  int retVal;
  if (left == right)
    {
      retVal = 0;
    }
  else if (left < right)
    {
      retVal = -1;
    }
  else
    {
      retVal = 1;
    }
  return retVal;
}

/* ______________________________________________________________________ */

static PyTypeObject PgenParserType = {
  PyObject_HEAD_INIT(NULL)
  0,
  "pgenParser",                      /* tp_name              */
  (int) sizeof(PgenParserObject),    /* tp_basicsize         */
  0,                                 /* tp_itemsize          */
  (destructor)pgenParserFree,        /* tp_dealloc           */
  0,                                 /* tp_print             */
  (getattrfunc)pgenParserGetAttr,    /* tp_getattr           */
  0,                                 /* tp_setattr           */
  (cmpfunc)pgenParserCompare,        /* tp_compare           */
  0,                                 /* tp_repr              */
  0,                                 /* tp_as_number         */
  0,                                 /* tp_as_sequence       */
  0,                                 /* tp_as_mapping        */
  0,                                 /* tp_hash              */
  0,                                 /* tp_call              */
  0,                                 /* tp_str               */
  0,                                 /* tp_getattro          */
  0,                                 /* tp_setattro          */
  /* Functions to access object as input/output buffer */
  0,                                  /* tp_as_buffer         */
  Py_TPFLAGS_DEFAULT,                 /* tp_flags             */
  /* __doc__ */
  "Internal representation of a grammar and its DFA."
};  /* PgenParserType */

/* ______________________________________________________________________ */

static PyObject *
pgenParserNew (grammar * g)
{
  PgenParserObject * retVal = PyObject_New(PgenParserObject,
					    &PgenParserType);
  if (NULL != retVal)
    {
      retVal->grammarPtr = g;
      retVal->g_start = g->g_start;
      retVal->symbolMap = NULL;
      retVal->stringMap = NULL;
    }
  return (PyObject *)retVal;
}

/* ______________________________________________________________________ */

static PyObject *
pgenParser_parseString (PgenParserObject * self, PyObject * args,
			PyObject * kw)
{
  PyObject * retVal = NULL;
  node * n;
  perrdetail err;
  int ok = 0;
  char * text;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!s:parseString", &PgenParserType, &self,
                            &text);
    }
  else
    {
      ok = PyArg_ParseTuple(args, "s:parseString", &text);
    }
  if (0 != ok)
    {
      n = PyParser_ParseString(text, self->grammarPtr,
                               self->g_start, &err);
      if (NULL == n)
        {
	  /* XXX - See notes for PyParser_SetError() appearing below. */
	  PyParser_SetError(&err);
        }
      else
        {
          retVal = pgenAstNew(n, self);
        }
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* pgenParser_parseFile ()

   Front for the PyParser_ParseFile function, now in improved method format!
 */

static PyObject *
pgenParser_parseFile (PgenParserObject * self, PyObject * args, PyObject * kw)
{
  PyObject * retVal = NULL;
  FILE * fp;
  node * n;
  perrdetail err;
  int ok = 0;
  char * filename;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!s:parseFile", &PgenParserType, &self,
                            &filename);
    }
  else
    {
      ok = PyArg_ParseTuple(args, "s:parseFile", &filename);
    }
  if (0 != ok)
    {
      fp = fopen(filename, "r");
      if (NULL == fp)
        {
          perror(filename);
        }
      else
        {
          n = PyParser_ParseFile(fp, filename, self->grammarPtr,
                                 self->g_start, (char *)NULL, (char *)NULL,
                                 &err);
          if (NULL == n)
            {
	      /* XXX - Note that this is somewhat of a stopgap measure.
		 The error handler employed here is specific to the
		 statically built Python parser, and may generate nonsense
		 exceptions for other parsers/grammars. */
	      PyParser_SetError(&err);
            }
          else
            {
              retVal = pgenAstNew(n, self);
            }
          fclose(fp);
        }
    }
  return retVal;
}

/* ______________________________________________________________________ */

static PyObject *
pgenParser_stringToSymbolMap (PgenParserObject * self, PyObject * args,
                              PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok = 0;
  int i;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:stringToSymbolMap", &PgenParserType,
                            &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":stringToSymbolMap");
    }
  if (0 != ok)
    {
      if (NULL == self->stringMap)
	{
	  grammar * g = self->grammarPtr;
	  dfa * d = g->g_dfa;

	  /* Iterate over the set of the grammar's DFA's, mapping from
	     d->d_name to d->d_type. */
	  retVal = PyDict_New();
	  for (i = 0; i < g->g_ndfas; i++, d++)
	    {
	      if (NULL != d->d_name)
		{
		  PyDict_SetItem(retVal, PyString_FromString(d->d_name),
				 PyInt_FromLong(d->d_type));
		}
	    }
	  /* Cache the map for later. */
	  Py_INCREF(retVal);
	  self->stringMap = retVal;
	}
      else
	{
	  retVal = self->stringMap;
	  Py_INCREF(retVal);
	}
    }
  return retVal;
}

/* ______________________________________________________________________ */

static PyObject *
pgenParser_symbolToStringMap (PgenParserObject * self, PyObject * args,
                              PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok = 0;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:symbolToStringMap", &PgenParserType,
                            &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":symbolToStringMap");
    }
  if (0 != ok)
    {
      retVal = getSymbolToStringMap(self);
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* pgenParser_getStart()

   Get the start symbol number that the parser will use when parsing input.
 */

static PyObject *
pgenParser_getStart (PgenParserObject * self, PyObject * args, PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok = 0;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:getStart", &PgenParserType,
                            &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":getStart");
    }
  if (0 != ok)
    {
      retVal = PyInt_FromLong(self->g_start);
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* pgenParser_setStart ()

   Set the start symbol that the parser will use.
 */

static PyObject *
pgenParser_setStart (PgenParserObject * self, PyObject * args, PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok = 0;
  int newStartSymbol;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!i:setStart", &PgenParserType,
                            &self, &newStartSymbol);
    }
  else
    {
      ok = PyArg_ParseTuple(args, "i:setStart", &newStartSymbol);
    }
  if (0 != ok)
    {
      if (1 == isValidSymbol(self->grammarPtr, newStartSymbol))
	{
	  self->g_start = newStartSymbol;
	  Py_INCREF(Py_None);
	  retVal = Py_None;
	}
      else
	{
	  PyErr_SetString(pgenError, "Invalid start symbol.");
	}
    }
  return retVal;
}

/* ______________________________________________________________________
   PgenParser_toTuple()

   Convert the parser to a tuple of the following Python types:

   Grammar := ( [ DFA ], [ Label ], Start : Int , Accels : Int )
   DFA := (Type : Int, Name : String, Initial : Int, [ State ] )
   State := ( [ Arc ], Accel, Accept : Int )
   Arc := ( Label : Int, StateIndex )
   Accel := ( Upper : Int, Lower : Int, [ Int ] )
   Label := ( Type : Int, Name : String )

   The resulting parser should be usable with basil.lang.python.DFAParser.
   This method is only meant to assist with debugging a Python implementation
   of pgen and should be avoided for normal use.
*/

/* ____________________________________________________________
   Helper functions for PgenParser_toTuple():
*/

static PyObject * arcsToList (int narcs, arc * arcPtr)
{
  PyObject * retVal = NULL;
  PyObject * crntItem = NULL;
  int i, ok;

  retVal = PyList_New(narcs);
  if (NULL != retVal)
    {
      for (i = 0; i < narcs; i++, arcPtr++)
        {
          crntItem = Py_BuildValue("(h,h)", arcPtr->a_lbl, arcPtr->a_arrow);
          if (NULL == crntItem) break;
          ok = PyList_SetItem(retVal, i, crntItem);
          if (-1 == ok)
            {
              Py_DECREF(crntItem);
              break;
            }
        }
      if (i < narcs)
        {
          Py_DECREF(retVal);
          retVal = NULL;
        }
    }
  return retVal;
}

/* ____________________________________________________________ */

static PyObject * accelsToList (int naccels, int * accelPtr)
{
  PyObject * retVal = NULL;
  PyObject * crntItem = NULL;
  int i, ok;

  retVal = PyTuple_New(naccels);
  if (NULL != retVal)
    {
      for (i = 0; i < naccels; i++, accelPtr++)
        {
          crntItem = PyInt_FromLong((long)(*accelPtr));
          if (NULL == crntItem) break;
          ok = PyTuple_SetItem(retVal, i, crntItem);
          if (-1 == ok)
            {
              Py_DECREF(crntItem);
              break;
            }
        }
      if (i < naccels)
        {
          Py_DECREF(retVal);
          retVal = NULL;
        }
    }
  return retVal;
}

/* ____________________________________________________________ */

static PyObject * statesToList (int nstates, state * statePtr)
{
  PyObject * retVal = NULL;
  PyObject * crntItem = NULL;
  PyObject * arcs = NULL;
  PyObject * accels = NULL;
  int i, ok;

  retVal = PyList_New(nstates);
  if (NULL != retVal)
    {
      for (i = 0; i < nstates; i++, statePtr++)
        {
          arcs = arcsToList(statePtr->s_narcs, statePtr->s_arc);
          if (NULL == arcs) break;
          accels = accelsToList(statePtr->s_upper - statePtr->s_lower,
                                statePtr->s_accel);
          if (NULL == accels)
            {
              Py_DECREF(arcs);
              break;
            }
          crntItem = Py_BuildValue("(N,(i,i,N),i)", arcs,
                                   statePtr->s_upper, statePtr->s_lower,
                                   accels, statePtr->s_accept);
          if (NULL == crntItem)
            {
              Py_DECREF(arcs); Py_DECREF(accels);
              break;
            }
          ok = PyList_SetItem(retVal, i, crntItem);
          if (-1 == ok)
            {
              Py_DECREF(crntItem);
              break;
            }
        }
      if (i < nstates)
        {
          Py_DECREF(retVal);
          retVal = NULL;
        }
    }
  return retVal;
}

/* ____________________________________________________________ */

static PyObject * dfasToList (int ndfas, dfa * dfaPtr, int bitsetSize)
{
  PyObject * retVal = NULL;
  PyObject * crntItem = NULL;
  PyObject * crntStates = NULL;
  int i, ok;

  retVal = PyList_New(ndfas);
  if (NULL != retVal)
    {
      for (i = 0; i < ndfas; i++, dfaPtr++)
        {
          crntStates = statesToList(dfaPtr->d_nstates, dfaPtr->d_state);
          if (NULL == crntStates) break;
          crntItem = Py_BuildValue("(i,s,i,N,s#)", dfaPtr->d_type,
                                   dfaPtr->d_name,
                                   dfaPtr->d_initial,
                                   crntStates, dfaPtr->d_first, bitsetSize);
          if (NULL == crntItem)
            {
              Py_DECREF(crntStates);
              break;
            }
          ok = PyList_SetItem(retVal, i, crntItem);
          if (-1 == ok)
            {
              Py_DECREF(crntItem);
              break;
            }
        }
      if (i < ndfas)
        {
          Py_DECREF(retVal);
          retVal = NULL;
        }
    }
  return retVal;
}

/* ____________________________________________________________ */

static PyObject * labelsToList (int nlabels, label * labelPtr)
{
  PyObject * retVal = NULL;
  PyObject * crntItem = NULL;
  int i, ok;

  retVal = PyList_New(nlabels);
  if (NULL != retVal)
    {
      for (i = 0; i < nlabels; i++, labelPtr++)
        {
          crntItem = Py_BuildValue("(i,s)", labelPtr->lb_type,
                                   labelPtr->lb_str);
          if (NULL == crntItem) break;
          ok = PyList_SetItem(retVal, i, crntItem);
          if (-1 == ok)
            {
              Py_DECREF(crntItem);
              break;
            }
        }
      if (i < nlabels)
        {
          Py_DECREF(retVal);
          retVal = NULL;
        }
    }
  return retVal;
}

/* ____________________________________________________________ */

static PyObject *
pgenParser_toTuple (PgenParserObject * self, PyObject * args, PyObject * kw)
{
  PyObject * retVal = NULL;
  PyObject * dfas = NULL;
  PyObject * labels = NULL;
  grammar * gramPtr = NULL;
  int ok = 0;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:toTuple", &PgenParserType, &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":toTuple");
    }
  if (0 != ok)
    {
      gramPtr = self->grammarPtr;
      dfas = dfasToList(gramPtr->g_ndfas, gramPtr->g_dfa,
                        NBYTES(gramPtr->g_ll.ll_nlabels));
      if (NULL != dfas)
        {
          labels = labelsToList(gramPtr->g_ll.ll_nlabels,
                                gramPtr->g_ll.ll_label);
          if (NULL == labels)
            {
              Py_DECREF(dfas);
            }
          else
            {
              retVal = Py_BuildValue("(N,N,i,i)", dfas, labels,
                                     gramPtr->g_start, gramPtr->g_accel);
            }
        }
    }
  return retVal;
}

/* ______________________________________________________________________
   PgenASTType
   ______________________________________________________________________ */

static PyMethodDef PgenASTMethods[] = {
  {"getType", (PyCFunction)pgenAst_getType, METH_VARARGS, ""},
  {"getName", (PyCFunction)pgenAst_getName, METH_VARARGS, ""},
  {"getGrammar", (PyCFunction)pgenAst_getGrammar, METH_VARARGS, ""},
  {"toTuple", (PyCFunction)pgenAst_toTuple, METH_VARARGS, ""},
  {NULL, NULL, 0, NULL}
};

static PyObject *
pgenAstGetAttr (PgenASTObject * obj, char * name)
{
  return Py_FindMethod(PgenASTMethods, (PyObject *)obj, name);
}

/* ______________________________________________________________________ */
/* XXX - Punt for now. */

static int
pgenAstCompare (PgenASTObject * left, PgenASTObject * right)
{
  int retVal;
  if (left == right)
    {
      retVal = 0;
    }
  else if (left < right)
    {
      retVal = -1;
    }
  else
    {
      retVal = 1;
    }
  return retVal;
}

/* ______________________________________________________________________ */

static PyTypeObject PgenASTType = {
  PyObject_HEAD_INIT(NULL)
  0,
  "pgenAST",                          /* tp_name              */
  (int) sizeof(PgenASTObject),        /* tp_basicsize         */
  0,                                  /* tp_itemsize          */
  (destructor)pgenAstFree,            /* tp_dealloc           */
  0,                                  /* tp_print             */
  (getattrfunc)pgenAstGetAttr,        /* tp_getattr           */
  0,                                  /* tp_setattr           */
  (cmpfunc)pgenAstCompare,            /* tp_compare           */
  0,                                  /* tp_repr              */
  0,                                  /* tp_as_number         */
  0,                                  /* tp_as_sequence       */
  0,                                  /* tp_as_mapping        */
  0,                                  /* tp_hash              */
  0,                                  /* tp_call              */
  0,                                  /* tp_str               */
  0,                                  /* tp_getattro          */
  0,                                  /* tp_setattro          */
  /* Functions to access object as input/output buffer */
  0,                                  /* tp_as_buffer         */
  Py_TPFLAGS_DEFAULT,                 /* tp_flags             */
  /* __doc__ */
  "Internal representation of a pgen parser generated parse tree."
};  /* PgenASTType */

/* ______________________________________________________________________ */
/* pgenAstNew(node * n, PgenParserObject *p)

   Create a new PyObject given a parse tree node and Python parser object.
 */

static PyObject *
pgenAstNew (node * n, PgenParserObject * p)
{
  PgenASTObject * retVal = PyObject_New(PgenASTObject, &PgenASTType);

  if (NULL != retVal)
    {
      retVal->nodePtr = n;
      Py_INCREF(p);
      retVal->parser = p;
    }
  else
    {
      PyNode_Free(n);
    }
  return (PyObject *)retVal;
}

/* ______________________________________________________________________ */
/* pgenAstFree (PgenASTObject * ast)

   Release the memory for a PgenASTObject.
*/

static void
pgenAstFree (PgenASTObject * ast)
{
  if (NULL != ast)
    {
      Py_DECREF(ast->parser);
      PyObject_Del(ast);
    }
}

/* ______________________________________________________________________ */
/* pgenAst_getType(PgenASTObject * self, PyObject * args, PyObject * kw)

   Returns the node type code of the start token used to create the AST.
 */

PyObject * pgenAst_getType (PgenASTObject * self, PyObject * args,
                            PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:getType", &PgenASTType, &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":getType");
    }
  if (0 != ok)
    {
      retVal = PyInt_FromLong(TYPE(self->nodePtr));
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* pgenAst_getName()

   Returns the name of the start token used in generation of the AST object.
 */

PyObject * pgenAst_getName (PgenASTObject * self, PyObject * args,
			    PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:getName", &PgenASTType, &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":getName");
    }
  if (0 != ok)
    {
      PyObject * typeCode = PyInt_FromLong(TYPE(self->nodePtr));
      PyObject * nDict = getSymbolToStringMap(self->parser);
      retVal = PyDict_GetItem(nDict, typeCode);
      if (NULL != retVal)
	{
	  Py_INCREF(retVal);
	}
      else
	{
	  PyErr_SetString(pgenError, "Internal error.");
	}
      Py_DECREF(nDict);
      Py_DECREF(typeCode);
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* pgenAst_getGrammar ()

   Return the parser/grammar object used to generate the given AST object.
 */

PyObject * pgenAst_getGrammar (PgenASTObject * self, PyObject * args,
                               PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:getGrammar", &PgenASTType, &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":getGrammar");
    }
  if (0 != ok)
    {
      retVal = (PyObject *)self->parser;
      Py_INCREF(retVal);
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* pgenAst_toTuple ()

   Returns a representation of the  AST object as a set of nested tuples and
   lists.
 */

PyObject * pgenAst_toTuple (PgenASTObject * self, PyObject * args,
                            PyObject * kw)
{
  PyObject * retVal = NULL;
  int ok;

  if (NULL == self)
    {
      ok = PyArg_ParseTuple(args, "O!:astToTuple", &PgenASTType, &self);
    }
  else
    {
      ok = PyArg_ParseTuple(args, ":toTuple");
    }
  if (0 != ok)
    {
      if (NULL != self->nodePtr)
        {
          retVal = pgen_node2tuple(self->nodePtr, 1);
        }
    }
  return retVal;
}

/* ______________________________________________________________________
   Module level functions.
   ______________________________________________________________________ */

/* ______________________________________________________________________ */
/* pgen_buildParser()

   Create a parser object using an input AST generated by the pgen meta-
   grammar.
 */

static PyObject *
pgen_buildParser (PgenASTObject * self, PyObject * args, PyObject * kw)
{
  PyObject * retVal = NULL;
  grammar * g;
  int ok;

  ok = PyArg_ParseTuple(args, "O!:buildParser", &PgenASTType, &self);
  if (0 != ok)
    {
      if (metaParser != self->parser)
	{
	  PyErr_SetString(pgenError,
			  "AST was not built using pgen metaparser");
	}
      else
	{
	  g = pgen(self->nodePtr);
	  if (NULL == g)
	    {
	      /* XXX - Need to do some real error handling here. */
	      PyErr_SetString(pgenError,
			      "Error in parser generator and/or input.");
	    }
	  else
	    {
	      retVal = pgenParserNew(g);
	    }
	}
    }
  return retVal;
}

/* ______________________________________________________________________
   Method table and initialization method for the pgen extension module.
   ______________________________________________________________________ */

#define PUBLIC_METHOD_TYPE (METH_VARARGS|METH_KEYWORDS)

static PyMethodDef pgenMethods [] = {
  {"buildParser", (PyCFunction)pgen_buildParser, PUBLIC_METHOD_TYPE, ""},
  {"parseFile", (PyCFunction)pgenParser_parseFile, PUBLIC_METHOD_TYPE, ""},
  {"parseString", (PyCFunction)pgenParser_parseString, PUBLIC_METHOD_TYPE,
   ""},
  {"symbolToStringMap", (PyCFunction)pgenParser_symbolToStringMap,
   PUBLIC_METHOD_TYPE, ""},
  {"stringToSymbolMap", (PyCFunction)pgenParser_stringToSymbolMap,
   PUBLIC_METHOD_TYPE, ""},
  {"astToTuple", (PyCFunction)pgenAst_toTuple, PUBLIC_METHOD_TYPE, ""},
  {NULL, NULL, 0, NULL}
};

/* ______________________________________________________________________ */

DL_EXPORT(void) initpgen (void); /* Shut GCC up about no prototype... */

DL_EXPORT(void) initpgen (void)
{
  PyObject * module;

  PgenASTType.ob_type = &PyType_Type;
  PgenParserType.ob_type = &PyType_Type;

  module = Py_InitModule("pgen", pgenMethods);

  Py_INCREF(&PgenASTType);
  PyModule_AddObject(module, "pgenASTType", (PyObject *)&PgenASTType);

  Py_INCREF(&PgenParserType);
  PyModule_AddObject(module, "pgenParserType", (PyObject *)&PgenParserType);

  if (NULL == metaParser)
    {
      metaParser = (PgenParserObject *)pgenParserNew(meta_grammar());
      Py_INCREF(metaParser);
    }

  PyModule_AddObject(module, "metaParser", (PyObject *)metaParser);

  if (NULL == pgenError)
    {
      pgenError = PyErr_NewException("pgen.pgenError", NULL, NULL);
    }

  PyModule_AddObject(module, "pgenError", pgenError);
}

/* ______________________________________________________________________
   End of pgenmodule.c
   ______________________________________________________________________ */
