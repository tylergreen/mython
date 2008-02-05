CFLAGS     = -DFENICS_HEADER=\<lap2.cxx\> -I.
EXTRA_ARGS =

mass: mass.o chkopts
	-${CLINKER} -o $@ $<  ${PETSC_SNES_LIB}
	${RM} -f $<

mass2: mass2.o chkopts
	-${CLINKER} -o $@ $<  ${PETSC_SNES_LIB}
	${RM} -f $<

lap2: lap2.o chkopts
	-${CLINKER} -o $@ $<  ${PETSC_SNES_LIB}
	${RM} -f $<

bratu: bratu.o chkopts
	-${CLINKER} -o $@ $<  ${PETSC_SNES_LIB}
	${RM} -f $<

include ${PETSC_DIR}/conf/base
