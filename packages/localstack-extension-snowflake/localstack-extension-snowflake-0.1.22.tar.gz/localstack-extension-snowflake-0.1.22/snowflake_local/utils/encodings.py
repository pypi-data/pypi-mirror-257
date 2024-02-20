import base64,datetime,decimal,io,json,logging,re,struct
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from localstack.utils.numbers import is_number
from localstack.utils.strings import to_bytes,to_str
from snowflake_local.engine.constants import FLOAT_TYPES,STRING_TYPES,TIMESTAMP_TYPES
from snowflake_local.engine.models import VARIANT_EXT_MARKER_PREFIX,VARIANT_MARKER_PREFIX
from snowflake_local.engine.transform_utils import is_variant_encoded_value,remove_variant_prefix,unwrap_variant_type
from snowflake_local.server.models import QueryResponse
LOG=logging.getLogger(__name__)
def decrypt_blob(blob,key,blob_path):B=struct.pack('q',0)+struct.pack('q',0);C=base64.b64decode(to_bytes(key));D=C+to_bytes(blob_path);E=sha256(D).digest();F=Cipher(algorithms.AES(E),modes.CTR(B));A=F.decryptor();G=A.update(blob)+A.finalize();return G
def get_parquet_from_blob(blob,key,blob_path):
	from pyarrow import parquet as B;A=decrypt_blob(blob,key=key,blob_path=blob_path)
	while A[-1]==0:A=A[:-1]
	try:C=io.BytesIO(A);D=B.read_table(C)
	except Exception as E:LOG.warning('Unable to parse parquet from decrypted data: %s... - %s',A[:300],E);raise
	return D.to_pylist()
def to_pyarrow_table_bytes_b64(result):
	V='BOOLEAN';U='ARRAY';T='OBJECT';S='INTEGER';R='type';P='TIME';O='DATE';N='FIXED';M='VARIANT';D=None;A=result;import pyarrow as B
	def K(row_type):
		X='TEXT';W=row_type;Q='38';L='16777216';K='T';J='finalType';I='physicalType';H='precision';G='scale';F='charLength';E='byteLength';C='0';B='logicalType';A=W[R]if W else M
		if A in(S,N):return{E:'4',F:C,B:N,G:C,H:Q,J:K}
		if A in(X,'VARCHAR'):return{I:'LOB',E:L,B:X,F:L}
		if A in(T,M,U):return{B:A,H:Q,G:C,F:L,E:L,J:K}
		if A in('DOUBLE',):return{B:'REAL',H:Q,G:C,F:C,E:'8',J:K}
		if A in TIMESTAMP_TYPES:
			D={B:A,H:C,G:'9'}
			if A=='TIMESTAMP_NTZ':D[I]='SB16'
			else:D[E]='16';D[F]=C;D[J]=K
			return D
		if A==O:return{I:'SB4',B:O}
		if A==P:return{I:'SB8',G:'9',B:P,H:C}
		if A==V:return{I:'SB1',B:A}
		return{B:A}
	def L(value,col_meta):
		A=value;C=str(col_meta[R]).upper()
		if A is D:
			if C in(S,N):return B.scalar(D,type=B.int32())
			if C in FLOAT_TYPES:return B.scalar(D,type=B.float32())
			if C in STRING_TYPES+(M,U,T):return B.scalar(D,type=B.string())
		if C in TIMESTAMP_TYPES:
			E={'epoch':B.scalar(int(A),type=B.int64()),'fraction':B.scalar(int(0),type=B.int32())}
			if C in('TIMESTAMP_LTZ','TIMESTAMP_TZ'):E['timezone']=1500
			return E
		if C==P and isinstance(A,datetime.time):F=9;E=A.hour*60*60+A.minute*60+A.second;E=E*10**F;return E
		if C==O and is_number(A):return B.scalar(int(A),type=B.date32())
		if C==V and isinstance(A,str):return A.lower()=='true'
		if C in FLOAT_TYPES and isinstance(A,decimal.Decimal):return float(A)
		if is_variant_encoded_value(A):
			if A.startswith(VARIANT_EXT_MARKER_PREFIX):return remove_variant_prefix(A)
			if A.startswith(VARIANT_MARKER_PREFIX):
				A=unwrap_variant_type(A)
				if A is D:A=B.scalar(D,type=B.string())
				elif isinstance(A,(list,dict)):A=json.dumps(A,indent=2)
		return A
	F=[];G=[re.sub('_col','$',A['name'],flags=re.I)for A in A.data.rowtype]
	for H in range(len(G)):Q=[L(B[H],A.data.rowtype[H])for B in A.data.rowset];F.append(B.array(Q))
	I=B.record_batch(F,names=G);J=B.BufferOutputStream();C=I.schema
	for E in range(len(C)):W=C.field(E);X=A.data.rowtype[E]if len(A.data.rowtype)>=E else D;Y=W.with_metadata(K(X));C=C.set(E,Y)
	with B.ipc.new_stream(J,C)as Z:Z.write_batch(I)
	A=base64.b64encode(J.getvalue());return to_str(A)