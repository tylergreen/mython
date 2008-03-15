#ifndef __NAMESPACE_H__
#define __NAMESPACE_H__
/* ______________________________________________________________________
   namespace.h
   $Id: namespace.h,v 1.2 2003/07/02 21:59:38 jriehl Exp $
   ______________________________________________________________________ */

void pushNamespace (void);
void popNamespace (void);
void addName (char * name, void * data);
int inNamespace (char * name);
void clearNamespace (void);

/* ______________________________________________________________________
   End of namespace.h
   ______________________________________________________________________ */
#endif
