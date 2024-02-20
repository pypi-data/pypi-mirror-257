from localstack.extensions.api import Extension
from rolo.gateway import CompositeExceptionHandler,CompositeResponseHandler
from rolo.router import Router,RuleAdapter,WithHost
class SnowflakeExtension(Extension):
	name='snowflake'
	def update_gateway_routes(C,router):from snowflake_local.server.routes import HOST_URL_PATTERN as A,RequestHandler as B;router.add(WithHost(A,[RuleAdapter(B())]))
	def update_response_handlers(D,handlers):A=handlers;from snowflake_local.analytics.handler import SnowflakeAnalyticsHandler as B,TraceLoggingHandler as C;A.append(B());A.append(C())
	def update_exception_handlers(B,handlers):from snowflake_local.analytics.handler import QueryFailureHandler as A;handlers.append(A())