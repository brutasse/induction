import asyncio
import inspect

from aiohttp.server import DEFAULT_ERROR_MESSAGE, RESPONSES

__all__ = ['yields', 'error']


def yields(value):
    return (
        isinstance(value, asyncio.futures.Future) or
        inspect.isgenerator(value)
    )


def error(status_code):
    try:
        reason, msg = RESPONSES[status_code]
    except KeyError:
        status_code = 500
        reason, msg = '???', ''

    html = DEFAULT_ERROR_MESSAGE.format(
        status=status_code, reason=reason, message=msg).encode('utf-8')
    return html, {'Content-Type': 'text/html; charset=utf-8',
                  'Content-Length': str(len(html))}
