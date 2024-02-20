_D='SELECT NULL'
_C='<stream_name>'
_B='name'
_A=False
import logging,re
from sqlglot import exp,parse_one
from snowflake_local.engine.models import Query,TableColumn
from snowflake_local.engine.postgres.constants import DEFAULT_SCHEMA
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.query_processors import QueryProcessor
from snowflake_local.engine.transform_utils import NameType,get_canonical_name
from snowflake_local.server.models import QueryResponse
from snowflake_local.utils.metadata import MetadataUtils
LOG=logging.getLogger(__name__)
STREAM_FUNC_NAME_PATTERN='_stream_func_<stream_name>'
TRIGGER_NAME_PATTERN='_stream_trigger_<stream_name>'
COL_NAME_RECORD_ID='_ls_row_id'
STREAM_TABLES={}
class RemoveHiddenRowIdColsFromResults(QueryProcessor):
	def postprocess_result(E,query,result):
		A=result
		for(B,C)in enumerate(list(A.data.rowtype)):
			if C[_B].lower()==COL_NAME_RECORD_ID.lower():
				for D in A.data.rowset:del D[B]
				del A.data.rowtype[B];return
class HandleCreateStream(QueryProcessor):
	REGEX=re.compile('\\s*CREATE\\s+(OR\\s+REPLACE\\s+)?STREAM\\s+(IF\\s+NOT\\s+EXISTS\\s+)?(\\S+)\\s+(COPY\\s+GRANTS\\s+)?ON\\s+TABLE\\s+(\\S+)',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(X,expression,query):
		W='METADATA$ROW_ID';V='TEXT';U='METADATA$ACTION';J=query;I=expression;D=', '
		if isinstance(I,(exp.Create,exp.Command)):
			E=J.get_database();F=[];O=X.REGEX.match(str(I));Y=re.match('.+APPEND_ONLY\\s*=\\s*TRUE',J.original_query,flags=re.I)
			if Y:LOG.info('Please note that APPEND_ONLY=TRUE semantics for table streams are not fully supported yet')
			K=get_canonical_name(O.group(5));A=get_canonical_name(O.group(3));Z,P=_get_trigger_function_for_stream(A);a=J.session.schema or DEFAULT_SCHEMA;b=_get_stream_tables(E,a);b.add(A);B=get_canonical_name(COL_NAME_RECORD_ID);L=f"\n            ALTER TABLE {K} ADD {B} VARCHAR DEFAULT gen_random_uuid()\n            ";State.server.run_query(L,database=E);c=MetadataUtils.get_table_schema(K,database=E);Q=[A for A in c.columns if A.name.lower()!=COL_NAME_RECORD_ID];M=list(Q);C=list(Q);C.append(TableColumn(name=U,type_name=V));C.append(TableColumn(name='METADATA$ISUPDATE',type_name='BOOLEAN'));C.append(TableColumn(name=W,type_name=V));d=D.join([f"{get_canonical_name(A.name)} {A.type_name}"for A in C]);F.append(f"CREATE TABLE {A}({d})");G=D.join([get_canonical_name(A.name)for A in C]);H=D.join(['%L'for A in M]);R=D.join([f"NEW.{get_canonical_name(A.name)}"for A in M]);S=D.join([f"OLD.{get_canonical_name(A.name)}"for A in M]);N=get_canonical_name(W);T=get_canonical_name(U);F.append(f"""
            CREATE OR REPLACE FUNCTION {P}() RETURNS trigger AS $$
                DECLARE inserted BOOLEAN; deleted BOOLEAN; ref_row RECORD;
                BEGIN
                    ref_row := CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;

                    -- determine whether this row has been inserted/deleted within the current stream offset
                    inserted := (
                        SELECT count(*) FROM {A} WHERE {N} = ref_row.{B} and {T} = 'INSERT'
                    );
                    deleted := (
                        SELECT count(*) FROM {A} WHERE {N} = ref_row.{B} and {T} = 'DELETE'
                    );

                    -- delete existing row updates in this stream
                    EXECUTE format('DELETE FROM {A} WHERE {N} = %L', ref_row.{B});

                    -- handle logic for each row, depending on the operation in TG_OP (INSERT/UPDATE/DELETE)
                    if TG_OP = 'INSERT' then
                        EXECUTE format(
                            'INSERT INTO {A}({G}) VALUES ({H}, ''INSERT'', FALSE, %L)',
                            {R}, NEW.{B}
                        );
                    elsif TG_OP = 'UPDATE' then
                        -- UPDATE trigger - create a DELETE (for old row) as well as an INSERT (for new row)
                        if not inserted then
                            EXECUTE format(
                                'INSERT INTO {A}({G}) VALUES ({H}, ''DELETE'', TRUE, %L)',
                                {S}, NEW.{B}
                            );
                        end if;
                        EXECUTE format(
                            'INSERT INTO {A}({G}) VALUES ({H}, ''INSERT'', %L, %L)',
                            {R}, CASE WHEN inserted THEN FALSE ELSE TRUE END, NEW.{B}
                        );
                    elsif TG_OP = 'DELETE' then
                        if not inserted then
                            EXECUTE format(
                                'INSERT INTO {A}({G}) VALUES ({H}, ''DELETE'', TRUE, %L)',
                                {S}, NEW.{B}
                            );
                        end if;
                    end if;
                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql
            """);F.append(f"\n            CREATE TRIGGER {Z} BEFORE INSERT OR UPDATE OR DELETE ON {K}\n                FOR EACH ROW EXECUTE FUNCTION {P}()\n            ");L='; '.join(F);State.server.run_query(L,database=E);return parse_one(_D)
		return I
class HandleDropStream(QueryProcessor):
	REGEX=re.compile('\\s*DROP\\s+STREAM\\s+(IF\\s+EXISTS\\s+)?(\\S+)',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(C,expression,query):
		A=expression
		if isinstance(A,(exp.Drop,exp.Command)):D=query.get_database();E=C.REGEX.match(str(A));B=E.group(2);H,F=_get_trigger_function_for_stream(B);G=f"DROP FUNCTION IF EXISTS {F} CASCADE";State.server.run_query(G,database=D);return parse_one(f"SELECT '{get_canonical_name(B,quoted=_A)} successfully dropped.'")
		return A
class HandleShowStreams(QueryProcessor):
	REGEX=re.compile('\\s*SHOW\\s+(TERSE\\s+)?STREAMS\\s+',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def postprocess_result(T,query,result):
		N='type';J=query;I=None;H='timestamp_ltz';C=result;A='text';O=J.get_database();P='SELECT trigger_schema, event_object_table AS tab_name, trigger_name FROM information_schema.triggers';D=State.server.run_query(P,database=O);D=list(D);K=TRIGGER_NAME_PATTERN.replace(_C,'(.+)');E=[tuple(A)for A in D if re.match(K,A[2],flags=re.I)];E=list(set(E));C.data.rowset=[];Q={'created_on':H,_B:A,'database_name':A,'schema_name':A,'owner':A,'comment':A,'table_name':'','source_type':A,'base_tables':A,N:A,'stale':A,'mode':A,'stale_after':H,'invalid_reason':A,'owner_role_type':A};C.data.rowtype=[]
		for(R,L)in Q.items():C.data.rowtype.append({_B:R,'precision':I,'scale':3 if L==H else I,N:L,'nullable':True,'length':I})
		for F in E:B=get_canonical_name(F[0],quoted=_A,type=NameType.SCHEMA,external=True);B=B.upper()if B=='public'else B;M=get_canonical_name(F[1],quoted=_A);S=get_canonical_name(F[2],quoted=_A);G=re.match(K,S,flags=re.I).group(1);G=get_canonical_name(G,quoted=_A);C.data.rowset.append(['0',G,J.get_database(),B,B,'',M,'Table',M,'DELTA','false','APPEND_ONLY','0','N/A','ROLE'])
	def transform_query(A,expression,query):return parse_one(_D)
class FlushStreamTableOnDmlQuery(QueryProcessor):
	def postprocess_result(K,query,result):
		E=' "';C=query
		try:F=parse_one(C.original_query)
		except Exception:return
		if not isinstance(F,exp.Insert):return
		G=F.find(exp.Select)
		if not G:return
		H=G.find(exp.From)
		if not H:return
		A=str(H.this).split('.');I=get_canonical_name(A[-1]).strip(E);D=C.session.schema;B=C.get_database()
		if len(A)>1:D=get_canonical_name(A[-2]).strip(E)
		if len(A)>2:B=get_canonical_name(A[-3]).strip(E)
		K._initialize_stream_tables(B,D);L=_get_stream_tables(B,D)
		for J in(I,f'"{I}"'):
			if J in L:State.server.run_query(f"TRUNCATE TABLE {J}",database=B)
	def _initialize_stream_tables(A,database,schema):
		if database in STREAM_TABLES:return
def _get_stream_tables(database,schema):A=STREAM_TABLES.setdefault(database,{});return A.setdefault(schema,set())
def _get_trigger_function_for_stream(stream_name):B=get_canonical_name(stream_name);A=B.strip('"').lower();C=TRIGGER_NAME_PATTERN.replace(_C,A);D=STREAM_FUNC_NAME_PATTERN.replace(_C,A);return C,D