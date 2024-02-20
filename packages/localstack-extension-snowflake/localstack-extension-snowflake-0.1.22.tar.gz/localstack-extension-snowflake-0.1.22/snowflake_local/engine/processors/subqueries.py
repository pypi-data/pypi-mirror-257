from sqlglot import exp
from snowflake_local.engine.query_processors import QueryProcessor
class UnwrapMultiNestedSubqueries(QueryProcessor):
	def transform_query(C,expression,**D):
		B=expression
		if isinstance(B,exp.Subquery):
			A=B
			while isinstance(A.this,exp.Subquery)and not A.this.alias:A=A.this
			return A
		return B