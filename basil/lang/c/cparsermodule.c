/* ______________________________________________________________________
   cparsermodule.c
   $Id: cparsermodule.c,v 1.1 2003/07/02 21:59:38 jriehl Exp $
   ______________________________________________________________________ */

/* ______________________________________________________________________
   Include files
   ______________________________________________________________________ */

#include <Python.h>
#include "cparserutils.h"

/* ______________________________________________________________________
   Flex interface prototypes and definitions.
   ______________________________________________________________________ */

/* Note that the types here are fudged, but essentially correct - I just
   don't want to block copy a bunch of that Flex crap in here. */

#define CPARSER_BUF_SIZE 16384

extern void * cparser_create_buffer (FILE * buf, int size);
extern void cparser_delete_buffer (void * buf);
extern void cparser_switch_buffer (void * buf);
extern void * cparser_scan_string (char * str);

extern void cparserparse (void);

/* ______________________________________________________________________
   Static data for the module.
   ______________________________________________________________________ */

static PyObject * cparserError = NULL;

/* ______________________________________________________________________
   Function definitions
   ______________________________________________________________________ */

/* ______________________________________________________________________

   Note that this has a lot to do with the pgen_node2tuple function found
   in the pgen integration, which in turn mirrors node2tuple() in
   parsermodule.c.

   Perhaps some refactoring is in order?
*/

static PyObject * convertCParserNodeToTuple (CParserNode * node)
{
  PyObject * myNode = NULL;

  if (NULL == node)
    {
      Py_INCREF(Py_None);
      myNode = Py_None;
    }
  else
    {
      PyObject * payload;
      PyObject * children;
      PyObject * child;
      int i;
      if (TOKEN_TYPE == node->type)
        {
          payload = Py_BuildValue("(i,s,i,i)", (int)(node->tokType), node->str,
                                  node->col, node->line);
        }
      else
        {
          payload = Py_BuildValue("i", (int)node->type);
        }
      if (NULL != payload)
        {
          children = PyList_New(node->childCount);
          if (NULL == children)
            {
              Py_DECREF(payload);
            }
          else
            {
              for (i = 0; i < node->childCount; i++)
                {
                  child = convertCParserNodeToTuple(node->children[i]);
                  if (NULL == child) break;
                  if (-1 == PyList_SetItem(children, i, child))
                    {
                      Py_DECREF(child);
                      break;
                    }
                }
              if (i < node->childCount)
                {
                  Py_DECREF(payload);
                  Py_DECREF(children);
                }
              else
                {
                  myNode = Py_BuildValue("(N,N)", payload, children);
                }
            }
        }
    }
  return myNode;
}

/* ______________________________________________________________________ */

static PyObject * cparser_parseFile (PyObject * self, PyObject * args,
                                     PyObject * kw)
{
  PyObject * retVal = NULL;
  char * fileName;
  int ok;

  ok = PyArg_ParseTuple(args, "s:parseFile", &fileName);
  if (0 != ok)
    {
      FILE * iFile;

      iFile = fopen(fileName, "r");
      if (NULL == iFile)
        {
          PyErr_Format(cparserError, "Could not open '%s' for parsing.",
                       fileName);
        }
      else
        {
          void * bufferHandle;
          CParserNode * crntRoot;

          bufferHandle = cparser_create_buffer(iFile, CPARSER_BUF_SIZE);
          cparser_switch_to_buffer(bufferHandle);
          cparserparse();
          crntRoot = CParserGetRoot();
          retVal = convertCParserNodeToTuple(crntRoot);
          CParserSetRoot(NULL);
          CParserFreeNode(crntRoot);
          cparser_delete_buffer(bufferHandle);
          fclose(iFile);
        }
    }
  return retVal;
}

/* ______________________________________________________________________ */

static PyObject * cparser_parseString (PyObject * self, PyObject * args,
                                       PyObject * kw)
{
  PyObject * retVal = NULL;
  char * parseString;
  int ok;
  ok = PyArg_ParseTuple(args, "s:parseString", &parseString);
  if (0 != ok)
    {
      void * bufferHandle;
      CParserNode * crntRoot;

      bufferHandle = cparser_scan_string(parseString);
      cparser_switch_to_buffer(bufferHandle);
      cparserparse();
      cparser_delete_buffer(bufferHandle);
      crntRoot = CParserGetRoot();
      retVal = convertCParserNodeToTuple(crntRoot);
      CParserSetRoot(NULL);
      CParserFreeNode(crntRoot);
    }
  return retVal;
}

/* ______________________________________________________________________
   Module initialization
   ______________________________________________________________________ */

#define PUBLIC_METHOD_TYPE (METH_VARARGS|METH_KEYWORDS)

static PyMethodDef _cparserMethods [] = {
  {"parseFile", (PyCFunction)cparser_parseFile, PUBLIC_METHOD_TYPE, ""},
  {"parseString", (PyCFunction)cparser_parseString, PUBLIC_METHOD_TYPE, ""},
  {NULL, NULL, 0, NULL}
};

/* ______________________________________________________________________ */

DL_EXPORT(void) init_cparser (void);

DL_EXPORT(void) init_cparser (void)
{
  PyObject * module = NULL;
  PyObject * crntObj = NULL;
  Py_ssize_t crntSize = 0;
  Py_ssize_t index = 0;

  module = Py_InitModule("_cparser", _cparserMethods);

  cparserError = PyErr_NewException("_cparser.cparserError", NULL, NULL);
  PyModule_AddObject(module, "cparserError", cparserError);

  /* FIXME: Perform error checking on the following... */

  crntSize = (Py_ssize_t)MAX_NODE_TYPE_VAL;
  crntObj = PyTuple_New(crntSize);
  for (index = 0; index < crntSize; index++)
    {
      PyTuple_SetItem(crntObj, index,
                      PyString_FromString(CParserNontermStrings[index]));
    }
  PyModule_AddObject(module, "cNonterminals", crntObj);

  crntSize = (Py_ssize_t)TT_NOT_A_TOKEN + 1;
  crntObj = PyTuple_New(crntSize);
  for (index = 0; index < crntSize; index++)
    {
      PyTuple_SetItem(crntObj, index,
                      PyString_FromString(CParserTokenStrings[index]));
    }
  PyModule_AddObject(module, "cTokens", crntObj);
}

/* ______________________________________________________________________
   End of cparsermodule.c
   ______________________________________________________________________ */
