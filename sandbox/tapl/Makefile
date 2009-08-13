# ______________________________________________________________________
# Makefile
#
# $Id: Makefile,v 1.12 2007/06/30 04:51:35 jriehl Exp $
# ______________________________________________________________________

LEXICAL_DEPS=Lexical.sdf Variables.sdf
SDF_TO_STR_TARGETS=BoolMain.str \
                   IntMain.str \
                   ComparisonMain.str \
                   UnitMain.str \
                   TypedLambdaMain.str \
                   SimpleLambdaPlus.str \
                   TuplesMain.str \
                   VariantsMain.str \
                   Lexical.str \
                   ToyFront.str

all:

%.def: %.sdf
	pack-sdf -i $< -o $@

%.tbl: %.def
	sdf2table -i $< -o $@ -m $*

%.rtg: %.def
	sdf2rtg -i $< -o $@ --main $*

%.sig: %.rtg
	rtg2sig -i $< -o $@

%.str: %.sig
	cp $< $@

%: %.str
	strc -i $< -la stratego-lib

# ____________________________________________________________
# Simple boolean language.

BOOL_MAIN_DEPS=BoolMain.sdf Bool.sdf $(LEXICAL_DEPS)

BoolMain.tbl: $(BOOL_MAIN_DEPS)

BoolMain.str: $(BOOL_MAIN_DEPS)

BoolTychMain: BoolTychMain.str BoolTych.str BoolMain.str

BoolEvalMain: BoolEvalMain.str EMachine.str BoolEval.str BoolMain.str

# ____________________________________________________________
# Simple integer expression language.

INT_MAIN_DEPS=IntMain.sdf Int.sdf $(LEXICAL_DEPS)

IntMain.tbl: $(INT_MAIN_DEPS)

IntMain.str: $(INT_MAIN_DEPS)

IntTychMain: IntTychMain.str IntTych.str IntMain.str

# ____________________________________________________________
# Comparison language.

COMP_MAIN_DEPS=ComparisonMain.sdf Comparison.sdf Int.sdf Bool.sdf \
               $(LEXICAL_DEPS)

ComparisonMain.tbl: $(COMP_MAIN_DEPS)

ComparisonMain.str: $(COMP_MAIN_DEPS)

COMPARISON_MAIN_EVAL_DEPS=ComparisonEval.str \
                          IntEval.str \
                          BoolEval.str \
                          EMachine.str \
                          Primop.str

ComparisonEvalMain: ComparisonEvalMain.str \
                    ComparisonMain.str \
                    $(COMPARISON_MAIN_EVAL_DEPS)

# ____________________________________________________________
# Unit expression language

UNIT_MAIN_DEPS=UnitMain.sdf Unit.sdf $(LEXICAL_DEPS)

UnitMain.tbl: $(UNIT_MAIN_DEPS)

UnitMain.str: $(UNIT_MAIN_DEPS)

# ____________________________________________________________
# Tuple language

TUPLES_MAIN_DEPS=TuplesMain.sdf Tuples.sdf Int.sdf $(LEXICAL_DEPS)

TuplesMain.tbl: $(TUPLES_MAIN_DEPS)

TuplesMain.str: $(TUPLES_MAIN_DEPS)

# ____________________________________________________________
# Variant language

VARIANTS_MAIN_DEPS=VariantsMain.sdf Variants.sdf $(LEXICAL_DEPS)

VariantsMain.tbl: $(VARIANTS_MAIN_DEPS)

VariantsMain.str: $(VARIANTS_MAIN_DEPS)

VARIANTS_TYCH_MAIN_DEPS=VariantsTychMain.str \
                        VariantsMain.str \
                        VariantsTych.str \
                        ComparisonTych.str \
                        IntTych.str \
                        BoolTych.str

VariantsTychMain: $(VARIANTS_TYCH_MAIN_DEPS)

# ____________________________________________________________
# Typed lambda calculus with no concrete types.

TYPED_LAMBDA_MAIN_DEPS=TypedLambdaMain.sdf TypedLambda.sdf $(LEXICAL_DEPS)

TypedLambdaMain.tbl: $(TYPED_LAMBDA_MAIN_DEPS)

TypedLambdaMain.str: $(TYPED_LAMBDA_MAIN_DEPS)

# ____________________________________________________________
# Simply typed lambda calculus extended with the boolean and integer languages.

SIMPLE_LAMBDA_DEPS=TypedLambda.sdf \
                   Bool.sdf \
                   Int.sdf \
                   Comparison.sdf \
                   Unit.sdf \
                   $(LEXICAL_DEPS)

SIMPLE_LAMBDA_PLUS_DEPS=SimpleLambdaPlus.sdf $(SIMPLE_LAMBDA_DEPS)

SimpleLambdaPlus.tbl: $(SIMPLE_LAMBDA_PLUS_DEPS)

SimpleLambdaPlus.str: $(SIMPLE_LAMBDA_PLUS_DEPS)

SIMPLE_LAMBDA_PLUS_TYCH_DEPS=TypedLambdaTych.str \
                             IntTych.str \
                             BoolTych.str \
                             UnitTych.str \
                             ComparisonTych.str

SimpleLambdaPlusTych: SimpleLambdaPlusTych.str \
                      SimpleLambdaPlus.str \
                      $(SIMPLE_LAMBDA_PLUS_TYCH_DEPS)

SimpleLambdaPlusTychDebug: SimpleLambdaPlusTychDebug.str \
                           SimpleLambdaPlus.str \
                           $(SIMPLE_LAMBDA_PLUS_TYCH_DEPS)

SIMPLE_LAMBDA_PLUS_EVAL_DEPS=TypedLambdaEval.str \
                             UnitEval.str \
                             $(COMPARISON_MAIN_EVAL_DEPS)

SimpleLambdaPlusEval: SimpleLambdaPlusEval.str \
                      SimpleLambdaPlus.str \
                      $(SIMPLE_LAMBDA_PLUS_EVAL_DEPS)

# ____________________________________________________________
# Full toy language (pre-extension)

TOY_FRONT_DEPS=ToyFront.sdf \
               Fix.sdf \
               IsoRecursiveTypes.sdf \
               Tuples.sdf \
               Variants.sdf \
               String.sdf \
               TypeAlias.sdf \
               Let.sdf \
               $(SIMPLE_LAMBDA_DEPS)

ToyFront.tbl: $(TOY_FRONT_DEPS)

ToyFront.str: $(TOY_FRONT_DEPS)

TOY_TYCH_DEPS=FixTych.str \
              IsoRecursiveTypesTych.str \
              TuplesTych.str \
              VariantsTych.str \
              StringTych.str \
              TypeAliasTych.str \
              LetTych.str \
              $(SIMPLE_LAMBDA_PLUS_TYCH_DEPS)

ToyTych: ToyTych.str ToyFront.str $(TOY_TYCH_DEPS)

ToyTychDebug: ToyTychDebug.str ToyFront.str $(TOY_TYCH_DEPS)

TOY_EVAL_DEPS=FixEval.str \
              IsoRecursiveTypesEval.str \
              TuplesEval.str \
              VariantsEval.str \
              StringEval.str \
              LetEval.str \
              $(SIMPLE_LAMBDA_PLUS_EVAL_DEPS)

ToyEval: ToyEval.str ToyFront.str $(TOY_EVAL_DEPS)

ToyEvalStep: ToyEvalStep.str ToyFront.str $(TOY_EVAL_DEPS)

# ____________________________________________________________
# Miscellaneous rules.

clean:
	rm -rf *.o *~ *.def *.tbl *.rtg *.dep *.lo $(SDF_TO_STR_TARGETS)

.PHONY: clean test

# ______________________________________________________________________
# End of Makefile
