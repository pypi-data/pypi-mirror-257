import dataclasses,logging,re
from rolo import Request
from snowflake_local.engine.models import Query,QueryState,Session
from snowflake_local.engine.transform_utils import NameType,get_canonical_name
from snowflake_local.tasks.models import Task
LOG=logging.getLogger(__name__)
@dataclasses.dataclass
class DBResources:file_formats:dict[str,dict]=dataclasses.field(default_factory=dict)
@dataclasses.dataclass
class ApplicationState:sessions:dict[str,Session]=dataclasses.field(default_factory=dict);queries:dict[str,QueryState]=dataclasses.field(default_factory=dict);db_resources:dict[str,DBResources]=dataclasses.field(default_factory=dict);tasks:dict[str,Task]=dataclasses.field(default_factory=dict)
APP_STATE=ApplicationState()
def handle_use_query(query_str,query,session):
	F=query;E=query_str;B=session;D=re.match('^\\s*USE\\s+(\\S+)\\s+(\\S+)',E,flags=re.I)
	if not D:return
	C=D.group(1).strip().lower();G=NameType.from_string(C);A=D.group(2)
	if'?'in A and F.params:A=F.params[0]
	A=get_canonical_name(A,quoted=False,type=G)
	if C=='database':B.database=A;B.schema=None
	elif C=='warehouse':B.warehouse=A
	elif C=='schema':
		B.schema=A
		if'.'in A:B.database,B.schema=A.split('.')
	else:LOG.info("Unexpected 'USE ...' query: %s",E)
def get_auth_token_from_request(request):A=request.headers.get('Authorization')or'';A=A.removeprefix('Snowflake ').strip();A=A.split('Token=')[-1].strip('\'"');return A
def lookup_request_session(request):
	B=get_auth_token_from_request(request)
	for A in APP_STATE.sessions.values():
		if A.auth_token==B:return A