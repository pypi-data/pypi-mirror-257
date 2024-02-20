from localstack.utils.numbers import is_number,to_number
from pyparsing import Group,OneOrMore,ParseResults,Word,alphanums,alphas,delimitedList,nestedExpr,originalTextFor,printables,quotedString
def parse_comma_separated_variable_assignments(expr):B=quotedString|originalTextFor(OneOrMore(Word(printables,excludeChars='(),')|nestedExpr()));C=Word(alphas+'_',alphanums+'_');D=Group(C+Word('=')+B);E=delimitedList(D);A=E.parseString(expr);A=_construct_dict_from_matched_items(A);return A
def parse_whitespace_separated_variable_assignments(expr):B=Word(alphas+'_',alphanums+'_');C=Word(alphanums+'_');D=quotedString|C;E=Group(B+Word('=')+D);F=OneOrMore(E);A=F.parseString(expr);A=_construct_dict_from_matched_items(A);return A
def _construct_dict_from_matched_items(results):
	D=results.asList();C={}
	for E in D:
		B,F,A=E;B=B.strip();A=A.strip()
		if len(A)>=2 and A[0]==A[-1]=="'":A=A.strip("'")
		elif len(A)>=2 and A[0]==A[-1]=='"':A=A.strip('"')
		elif is_number(A):A=to_number(A)
		elif A.lower()in('true','false'):A=bool(A)
		elif A.lower()=='null':A=None
		C[B]=A
	return C