import asyncio
import inspect

__all__ = ['yields']


def yields(value):
    return (
        isinstance(value, asyncio.futures.Future) or
        inspect.isgenerator(value)
    )
