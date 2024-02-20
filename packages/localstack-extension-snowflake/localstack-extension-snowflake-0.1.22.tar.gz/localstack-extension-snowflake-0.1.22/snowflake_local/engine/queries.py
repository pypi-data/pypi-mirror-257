import base64,logging,re,uuid
from typing import Any
from localstack.utils.strings import to_bytes,to_str,truncate
from pg8000.dbapi import ProgrammingError
from sqlglot import parse_one
from snowflake_local import config
from snowflake_local.engine.db_engine import get_db_engine
from snowflake_local.engine.models import Query,QueryResult,QueryState,Session
from snowflake_local.engine.query_processors import QueryProcessor
from snowflake_local.engine.session import APP_STATE
from snowflake_local.engine.transform_utils import get_canonical_name
from snowflake_local.engine.transforms import remove_comments
from snowflake_local.server.models import QueryException,QueryResponse,QueryResponseData
LOG=logging.getLogger(__name__)
def cleanup_query(query):
	D='/\\*.*?\\*/';C='snowflake';B=query;A=B.strip(' ;')
	try:
		if re.match('.*DESC(RIBE)?.+FILE\\s+FORMAT',B,flags=re.I|re.M):raise Exception
		E=parse_one(A,read=C);F=E.transform(remove_comments);A=str(F.sql(dialect=C));A=re.sub(D,'',A,flags=re.I)
	except Exception:
		A=re.sub(D,'',A,flags=re.I);A=re.sub('^\\s*--.*','',A,flags=re.M)
		if re.match('\\s*DESC(RIBE)?\\s+TASK',A,flags=re.I|re.M):A=f"EXECUTE {A}"
	return A
def execute_query(query):A=query;B=get_db_engine();A=prepare_query(A);C=B.execute_query(A);return C
def prepare_query(query_obj):A=query_obj;A.original_query=A.query;A.query=_create_tmp_table_for_file_queries(A.query);B=get_db_engine();A=B.prepare_query(A);return A
def insert_rows_into_table(table,rows,schema=None,database=None):
	J=database;I=schema;H=', ';A=rows;E=f'"{table}"'
	if I:E=f"{get_canonical_name(I)}.{E}"
	if A and isinstance(A[0],dict):
		B=set()
		for C in A:B.update(C.keys())
		B=list(B);F=B
		if config.CONVERT_NAME_CASING:F=[f'"{A}"'for A in B]
		F=H.join(F);G=H.join(['?'for A in B]);K=f"INSERT INTO {E} ({F}) VALUES ({G})"
		for C in A:L=[C.get(A)for A in B];D=Query(query=K,params=list(L),database=J);execute_query(D)
	elif A and isinstance(A[0],(list,tuple)):
		for C in A:M=len(C);G=H.join(['?'for A in range(M)]);D=f"INSERT INTO {E} VALUES ({G})";D=Query(query=D,params=list(C),database=J);execute_query(D)
	elif A:raise Exception(f"Unexpected values when storing list of rows to table: {truncate(str(A))}")
def handle_query_request(query,params,session,request):
	N='type';M='002002';L=False;K='name';F=query;A=QueryResponse();A.data.parameters.append({K:'TIMEZONE','value':'UTC'});F=cleanup_query(F);G=A.data.queryId=str(uuid.uuid4());C=Query(query_id=G,query=F,params=params,session=session,request=request);APP_STATE.queries[G]=O=QueryState(query=C,query_state='RUNNING')
	try:D=execute_query(C)
	except Exception as B:
		P=LOG.exception if config.TRACE_LOG else LOG.warning;P('Error executing query: %s',B);A.success=L;A.message=str(B)
		if isinstance(B,ProgrammingError)and B.args:A.code=M;A.message=B.args[0].get('M')or str(B);A.data=QueryResponseData(**{'internalError':L,'errorCode':M,'age':0,'sqlState':'42710','queryId':G,'line':-1,'pos':-1,N:'COMPILATION'})
		for E in QueryProcessor.get_instances():
			if E.should_apply(C):E.postprocess_result(C,result=A)
		raise QueryException(message=A.message,query_data=A)from B
	O.result=D
	if D and D.columns:
		H=[];Q=D.columns
		for R in D.rows:H.append(list(R))
		J=[]
		for I in Q:J.append({K:I.name,N:I.type_name,'length':I.type_size,'precision':0,'scale':0,'nullable':True})
		A.data.rowset=H;A.data.rowtype=J;A.data.total=len(H)
	for E in QueryProcessor.get_instances():
		if E.should_apply(C):E.postprocess_result(C,result=A)
	return A
def _create_tmp_table_for_file_queries(query):
	A=query;B='(.*SELECT\\s+.+\\sFROM\\s+)(@[^\\(\\s]+)(\\s*\\([^\\)]+\\))?';C=re.match(B,A,flags=re.I)
	if not C:return A
	def D(match):A=match;B=to_str(base64.b64encode(to_bytes(A.group(3)or'')));return f"{A.group(1)} load_data('{A.group(2)}', '{B}') as _tmp"
	A=re.sub(B,D,A);return A