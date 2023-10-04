from starlette.middleware.base import BaseHTTPMiddleware


class MethodMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if "_method" in request.query_params:
            request.scope["method"] = request.query_params["_method"].upper()
        response = await call_next(request)
        return response
