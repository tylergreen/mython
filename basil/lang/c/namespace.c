/* ______________________________________________________________________
   namespace.c
   $Id: namespace.c,v 1.1 2003/06/29 00:22:47 jriehl Exp $
   ______________________________________________________________________ */

/* ______________________________________________________________________
   Include files
   ______________________________________________________________________ */

#include <stdlib.h>
#include <string.h>

#include "namespace.h"

typedef struct _nameEntry {
  struct _nameEntry * next;
  char * name;
  void * data;
} nameEntry;

typedef struct _nameList {
  struct _nameList * prev;
  nameEntry * head;
  nameEntry * tail;
} nameList;

static nameList * topNamespace = NULL;

/* ______________________________________________________________________ */

nameEntry * newNameEntry (char * name, void * data)
{
  nameEntry * retVal = (nameEntry *)malloc(sizeof(nameEntry));
  if (NULL != retVal)
    {
      retVal->name = strdup(name);
      retVal->data = data;
      retVal->next = NULL;
    }
  return retVal;
}

/* ______________________________________________________________________ */

void delNameEntry (nameEntry * entry)
{
  free(entry->name);
  free(entry);
}

/* ______________________________________________________________________ */

nameList * newNameList ()
{
  nameList * retVal = (nameList *)malloc(sizeof(nameList));
  if (NULL != retVal)
    {
      retVal->head = retVal->tail = NULL;
      retVal->prev = NULL;
    }
  return retVal;
}

/* ______________________________________________________________________ */

void delNameList (nameList * list)
{
  nameEntry * crntEntry = list->head;
  nameEntry * nextEntry;
  while (NULL != crntEntry)
    {
      nextEntry = crntEntry->next;
      delNameEntry(crntEntry);
      crntEntry = nextEntry;
    }
  free(list);
}

/* ______________________________________________________________________ */

void addEntryToList (nameList * list, nameEntry * entry)
{
  if (NULL != entry)
    {
      if (NULL == list->head)
        {
          list->head = list->tail = entry;
        }
      else
        {
          list->tail->next = entry;
          list->tail = entry;
        }
    }
}

/* ______________________________________________________________________ */

void initNamespace ()
{
  topNamespace = newNameList();
  if (NULL != topNamespace)
    {
      addEntryToList(topNamespace, newNameEntry("__builtin_va_list", NULL));
    }
}

/* ______________________________________________________________________
   Function definitions
   ______________________________________________________________________ */

void pushNamespace ()
{
  if (NULL == topNamespace)
    {
      initNamespace();
    }
  if (NULL != topNamespace)
    {
      nameList * newTop = newNameList();
      if (NULL != newTop)
        {
          newTop->prev = topNamespace;
          topNamespace = newTop;
        }
      else
        {
          /* XXX ERROR XXX */
        }
    }
}

/* ______________________________________________________________________ */

void popNamespace ()
{
  if (NULL != topNamespace)
    {
      nameList * oldNamespace = topNamespace;
      topNamespace = topNamespace->prev;
      if (NULL == topNamespace)
        {
          /* XXX ERROR XXX - Stack underflow. */
        }
      delNameList(oldNamespace);
    }
}

/* ______________________________________________________________________ */

void addName (char * name, void * data)
{
  if (NULL == topNamespace)
    {
      initNamespace();
    }
  if (NULL != topNamespace)
    {
      nameEntry * newEntry = newNameEntry(name, data);
      addEntryToList(topNamespace, newEntry);
    }
}

/* ______________________________________________________________________ */

int inNamespace (char * name)
{
  int retVal = 0;
  if (NULL == topNamespace)
    {
      initNamespace();
    }
  if (NULL != topNamespace)
    {
      nameList * crntList = topNamespace;
      nameEntry * crntEntry = NULL;
      while (NULL != crntList)
        {
          crntEntry = crntList->head;
          while (NULL != crntEntry)
            {
              if (0 == strcmp(name, crntEntry->name))
                {
                  retVal = 1;
                  break;
                }
              crntEntry = crntEntry->next;
            }
          if (1 == retVal) break;
          crntList = crntList->prev;
        }
    }
  return retVal;
}

/* ______________________________________________________________________ */
/* clearNamespace() - Delete the top level namespace. */

void clearNamespace (void)
{
  if (NULL != topNamespace)
    {
      delNameList(topNamespace);
      topNamespace = NULL;
    }
}

/* ______________________________________________________________________
   End of namespace.c
   ______________________________________________________________________ */
