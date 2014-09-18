import aiohttp
import asyncio
import inspect
import io
import json

from jinja2 import Environment, FileSystemLoader
from routes import Mapper

from .encoding import JSONEncoder
from .protocol import AppServerHttpProtocol
from .utils import yields

__all__ = ['Induction', 'read_payload', 'jsonify']


def jsonify(data, cls=JSONEncoder, **kwargs):
    return json.dumps(data, cls=cls, **kwargs)


def read_payload(payload):
    _input = io.BytesIO()
    try:
        while True:
            _input.write((yield from payload.read()))
    except aiohttp.EofStream:
        pass
    _input.seek(0)
    return _input


class Induction:
    def __init__(self, name, template_folder='templates'):
        self._name = name
        self._routes = Mapper(register=False)
        self._before_request = []
        self._after_request = []
        self._error_handlers = {}
        self._jinja_env = Environment(loader=FileSystemLoader(template_folder))

    @asyncio.coroutine
    def handle_request(self, request, response, payload):
        # Apply request processors
        for func in self._before_request:
            before = func(request, response)
            if yields(before):
                before = yield from before
            if before is not None:
                data = before
                fn_name = func.__name__
                need_response = True
                break
        else:
            match = self._routes.match(request.path)
            _self = 0
            if match is None:
                handler = self.handle_404
                _self = 1
            else:
                handler = match.pop('_induction_handler')
            request.kwargs = match or {}

            # 2 arities supported in handlers:
            #
            # - handler(request, response)
            #   Handler can write stuff in response or return data that gets
            #   written to the response (str or bytes, or tuple of (response,
            #   status, headers) or (response, headers))
            #
            # - handler(request, response, payload)
            #   The payload is passed when the handler needs it.

            args = [request]
            need_response = False
            fn_name = handler.__name__

            spec = inspect.getargspec(handler)
            argc = len(spec.args) - _self
            if argc == 1:
                need_response = True
            elif argc >= 2:
                args.append(response)
            if argc == 3:
                args.append(payload)

            data = handler(*args)

        try:
            yield from self.handle_data(data, response, need_response, fn_name)
        except Exception as e:
            handler = self._error_handlers.get(type(e))
            if handler is None:
                raise
            data = handler(request, response, e)
            yield from self.handle_data(data, response, True, handler.__name__)

        for func in self._after_request:
            after = func(request, response)
            if yields(after):
                yield from after

    @asyncio.coroutine
    def handle_data(self, data, response, need_response, fn_name):
        if yields(data):
            yield from data
            if not response.finished:
                response.write_eof()
        else:
            if need_response and data is None:
                # when calling handler(request) we expect some data so that
                # we can write it to a response.
                raise TypeError("Expected response data, '{0}' returned "
                                "None".format(fn_name))
            if data is not None:
                rsp = data
                if isinstance(data, tuple):
                    # Flask-style way of returning (data, status, headers)
                    for value in data:
                        if isinstance(value, int):
                            # Status
                            response.set_status(value)
                        elif isinstance(value, (dict, tuple)):
                            # Headers
                            if isinstance(value, dict):
                                value = value.items()
                            for name, val in value:
                                response.add_header(name, val)
                        elif isinstance(value, (str, bytes, bytearray)):
                            # body
                            rsp = value

                for name, _ in response.headers.items():
                    if name == 'CONTENT-TYPE':
                        break
                else:
                    response.add_header('Content-Type',
                                        'text/html; charset=utf-8')

                if isinstance(rsp, (str, bytes, bytearray)):
                    response.write(rsp, unchunked=True)
                else:
                    response.write_eof()

    def route(self, path, **conditions):
        def wrap(func):
            self._routes.connect(path, _induction_handler=func,
                                 conditions=conditions)
            return func
        return wrap

    def before_request(self, func):
        self._before_request.append(func)
        return func

    def after_request(self, func):
        self._after_request.append(func)
        return func

    def error_handler(self, typ):
        def wrap(func):
            self._error_handlers[typ] = func
            return func
        return wrap

    def run(self, *, host='0.0.0.0', port=8000, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        asyncio.async(
            loop.create_server(lambda: AppServerHttpProtocol(self),
                               host, port)
        )
        print("Listening on http://{0}:{1}".format(host, port))
        loop.run_forever()

    def render_template(self, template_name_or_list, **context):
        template = self._jinja_env.get_or_select_template(
            template_name_or_list)
        return template.render(context)

    def handle_404(self, request):
        return (jsonify({'error': 404}), 404,
                {'Content-Type': 'application/json'})
