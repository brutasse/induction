import asyncio

from aiohttp.server import ServerHttpProtocol

from .request import Request
from .response import Response

__all__ = ['AppServerHttpProtocol']


class AppServerHttpProtocol(ServerHttpProtocol):
    def __init__(self, app, **kwargs):
        self.app = app
        super().__init__(**kwargs)

    @asyncio.coroutine
    def handle_request(self, request, payload):
        response = self.prepare_response(request)
        request = Request(request)
        return (yield from self.app.handle_request(request, response, payload))

    def prepare_response(self, request):
        return Response(self.writer, 200, request=request)
