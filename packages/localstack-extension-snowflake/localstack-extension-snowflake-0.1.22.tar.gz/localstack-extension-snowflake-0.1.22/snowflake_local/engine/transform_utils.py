_I='array_union_agg'
_H='array_sort'
_G='array_size'
_F='array_join'
_E='array_agg'
_D=False
_C='TABLE'
_B='array_cat'
_A='kind'
import json,logging
from enum import Enum
from typing import Any,Optional
from localstack.utils.collections import ensure_list
from localstack.utils.numbers import is_number
from sqlglot import exp,parse_one
from snowflake_local import config
from snowflake_local.engine.models import VARIANT,VARIANT_EXT_MARKER_PREFIX,VARIANT_MARKER_PREFIX
LOG=logging.getLogger(__name__)
INTERNAL_IDENTIFIERS={'attname','attnum','attrelid','atttypid','atttypmod','arg_max','arg_min',_E,_B,_F,_G,_H,_I,'current_database','current_schema','current_task_graphs','format_type','get_path','indisprimary','indkey','indrelid','is_array','lead','nspname','oid','parse_json','pg_attribute','pg_class','pg_database','pg_index','pg_namespace','plpython3u','plv8','relname','relnamespace','sum','to_char','to_date'}
SNOWFLAKE_FUNCTIONS={_E,'array_append',_B,'array_construct','array_construct_compact','array_contains',_F,'array_prepend','array_remove',_G,_H,_I}
class NameType(Enum):
	DATABASE=0;SCHEMA=1;RESOURCE=2
	@classmethod
	def from_string(B,type_name):
		A=[A for A in NameType if A.name.lower()==type_name.lower()]
		if A:return A[0]
def convert_function_args_to_variant(expression,function,**F):
	D='to_variant';A=expression
	if not isinstance(A,exp.Func):return A
	C=str(A.this).lower()
	if isinstance(A,exp.ArrayConcat):C=_B
	if C!=function:return A
	for(E,B)in enumerate(A.expressions):A.expressions[E]=exp.Anonymous(this=D,expressions=ensure_list(B))
	if isinstance(A,exp.ArrayConcat):B=A.this;A.args['this']=exp.Anonymous(this=D,expressions=ensure_list(B))
	return A
def is_create_table_expression(expression):A=expression;return isinstance(A,exp.Create)and(B:=A.args.get(_A))and isinstance(B,str)and B.upper()==_C
def get_canonical_identifier_multilevel(identifier):A=identifier.split('.');A=[get_canonical_name(A.strip())for A in A];B='.'.join(A);return B
def get_canonical_name(name,type=None,quoted=True,external=_D):
	G='public';D=external;C='"';B=quoted;A=name;A=A.strip();E=A.startswith(C)and A.endswith(C)
	if D and not B and not E:return A.strip(C).upper()
	if not config.CONVERT_NAME_CASING:
		if type==NameType.DATABASE and not B:return A.lower()
		return A
	if E:return A
	if'.'in A:LOG.info('Found dot in resource name, could hint at a potential name parsing issue: %s',A)
	if A.lower()in INTERNAL_IDENTIFIERS:return A
	if not D and type in[None,NameType.SCHEMA]and A.lower()==G:return G
	F=A.upper()
	if B:return f'"{F}"'
	return F
def get_table_from_creation_query(query):return get_name_from_creation_query(query,resource_type=_C)
def get_view_from_creation_query(query):return get_name_from_creation_query(query,resource_type='VIEW')
def get_name_from_creation_query(query,resource_type):
	B=parse_snowflake_query(query)
	if not isinstance(B,exp.Create):return
	if str(B.args.get(_A)).upper()!=resource_type.upper():return
	A=B.this
	while hasattr(A,'this'):A=A.this
	return str(A)
def get_table_from_drop_query(query):
	A=parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_A)!=_C:return
	B=A.this;C=B.this;D=C.this;return D
def get_database_from_drop_query(query):
	A=parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_A)!='DATABASE':return
	B=A.this;C=B.this;D=C.this;return D
def parse_snowflake_query(query):
	try:return parse_one(query,read='snowflake')
	except Exception:return
def unwrap_potential_variant_type(obj):
	A=obj
	if isinstance(A,str)and A.startswith(VARIANT_MARKER_PREFIX):return unwrap_variant_type(A)
	return A
def unwrap_variant_type(variant_obj_str,expected_type=None):
	C=expected_type;B=variant_obj_str;B=remove_variant_prefix(B);A=json.loads(B)
	if C:
		if not isinstance(A,C)and isinstance(A,str):
			try:
				D=json.loads(A)
				if isinstance(D,C):A=D
			except Exception:pass
	return A
def remove_variant_prefix(value):
	A=value
	if isinstance(A,str):A=A.removeprefix(VARIANT_EXT_MARKER_PREFIX);A=A.removeprefix(VARIANT_MARKER_PREFIX)
	return A
def to_variant(obj,external=_D):
	B=external;A=obj
	if is_variant_encoded_value(A,external=B):return A
	A=unwrap_potential_variant_type(A)
	if not isinstance(A,bool)and is_number(A)and int(A)==A:A=int(A)
	try:C=json.dumps(A);D=VARIANT_EXT_MARKER_PREFIX if B else VARIANT_MARKER_PREFIX;return f"{D}{C}"
	except Exception:return str(A)
def is_variant_encoded_value(value,external=_D):A=value;B=VARIANT_EXT_MARKER_PREFIX if external else VARIANT_MARKER_PREFIX;return isinstance(A,str)and A.startswith(B)