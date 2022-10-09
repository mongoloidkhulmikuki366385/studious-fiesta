#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"

import zmq
from Common.publisher import ZmqPublisher


def public(name=None):
    """Set RPC name on function.

    This function decorator will set the ``_rpc_public_name`` attribute on a
    function, causing it to be picked up if an instance of its parent class is
    registered using
    :py:func:`~tinyrpc.dispatch.RPCDispatcher.register_instance`.

    ``@public`` is a shortcut for ``@public()``.

    :param name: The name to register the function with.
    """
    # called directly with function
    if callable(name):
        f = name
        f._rpc_public_name = f.__name__
        return f

    def _(f):
        f._rpc_public_name = name or f.__name__
        return f

    return _


class FunctionMap(object):
    def __init__(self):
        ctx = zmq.Context().instance()
        endpoint = 9510
        # self.publisher = ZmqPublisher(ctx, endpoint, 'functionmap')

    def add(self):
        result = 5 + 10
        # self.publisher.publish(result)

        return result

    def sub(self):
        result = 5 - 10
        # self.publisher.publish(result)
        return result

    def mul(self):
        result = 5 * 10
        # self.publisher.publish(result)
        return result

    def chu(self):
        result = 5 / 10
        # self.publisher.publish(result)
        return result

    @public('hello')
    def hello(self):
        result = 'hello world!'
        # self.publisher.publish(result)
        return result

    def publish(self):
        pass

# print lambda f: callable(f) and hasattr(f, '_rpc_public_name')

# print inspect.getmembers(
#             FunctionMap, lambda f: callable(f) and hasattr(f, '_rpc_public_name') )

# print public.__name__


