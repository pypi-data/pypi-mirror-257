import re
from sqlglot import exp,parse_one
from snowflake_local.engine.models import Query
from snowflake_local.engine.query_processors import QueryProcessor
class HandleCreateStorage(QueryProcessor):
	REGEX=re.compile('^\\s*CREATE\\s+STORAGE\\s.+',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,exp.Create):return parse_one("SELECT 'Storage successfully dropped.'")
		return A