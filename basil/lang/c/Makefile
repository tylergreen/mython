# ______________________________________________________________________
# Makefile
# ______________________________________________________________________
# $Id: Makefile,v 1.3 2003/07/10 22:08:16 jriehl Exp $
# ______________________________________________________________________

CFLAGS=-g
CC=gcc ${CFLAGS}

cparser: cparser.tab.o lex.cparser.o cparserutils.o namespace.o cparsermain.o
	${CC} -o cparser cparserutils.o namespace.o cparser.tab.o \
	      lex.cparser.o cparsermain.o

test: cparser
	@ for testfile in tests/*.in; do\
	echo "____________________________________________________________";\
	echo $$testfile;\
	echo "____________________________________________________________";\
	./cparser < $$testfile;\
	done

# -d causes the .tab.h file to be generated
cparser.tab.c cparser.tab.h: cparser.y
	bison -pcparser -d cparser.y

lex.cparser.o: lex.cparser.c cparser.tab.h cparserutils.h namespace.h
	${CC} -c lex.cparser.c

lex.cparser.c: cparser.l
	flex -Pcparser cparser.l

cparser.tab.o: cparser.tab.c
	${CC} -o cparser.tab.o -c -DYYERROR_VERBOSE cparser.tab.c

clean:
	rm -f core cparser.tab.* *.o *~ lex.yy.c
