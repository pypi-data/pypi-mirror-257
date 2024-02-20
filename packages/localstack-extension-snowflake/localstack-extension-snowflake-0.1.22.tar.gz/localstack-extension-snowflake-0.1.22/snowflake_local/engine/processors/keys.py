from sqlglot import exp,parse_one
from snowflake_local.engine.models import Query
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.query_processors import QueryProcessor
from snowflake_local.engine.transform_utils import get_canonical_name
from snowflake_local.utils.metadata import MetadataUtils
class HandleDropPrimaryKey(QueryProcessor):
	def transform_query(K,expression,query):
		B=query;A=expression
		if isinstance(A,exp.AlterTable):
			E=A.args.get('actions')or[];F=[A for A in E if isinstance(A,exp.Command)];G=[A for A in F if str(A.this).upper()=='DROP'];H=[A for A in G if'PRIMARY KEY'in str(A.expression).upper()]
			if H:
				I=get_canonical_name(str(A.this.this),quoted=False);C=B.get_database();D=MetadataUtils.get_primary_key_constraint(I,database=C);J=get_canonical_name(str(A.this.this))
				if D:B=f'ALTER TABLE {J} DROP CONSTRAINT "{D}"';State.server.run_query(B,database=C)
				return parse_one('SELECT NULL')
		return A