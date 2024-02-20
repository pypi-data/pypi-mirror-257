from snowflake.connector.cursor import SnowflakeCursor
def cursor_to_records(cursor):
	A=cursor;C=[A.name for A in A.description];B=[]
	for D in list(A):B.append(dict(zip(C,D)))
	return B