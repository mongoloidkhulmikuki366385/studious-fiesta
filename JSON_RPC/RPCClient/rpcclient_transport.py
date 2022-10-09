#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"

import zmq
import time
import six
from . import *


class ClientTransport(object):

    def send_message(self, message, expect_reply=True):
        raise NotImplementedError


class ZmqClientTransport(ClientTransport):
    """Client transport based on a :py:const:`zmq.REQ` socket.

    :param socket: A :py:const:`zmq.REQ` socket instance, connected to the
                   server socket.
        :param zmq_context: A 0mq context.
        :param endpoint: The endpoint the server is bound to.
    """

    def __init__(self, socket, context, endpoint, timeout=DEFAULT_RPC_TIMEOUT):
        self.publisher = None
        self.socket = socket
        self.context = context
        self.endpoint = endpoint
        self.timeout = timeout

    def reconnect(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        time.sleep(0.1)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.endpoint)

    def send_reply(self, message):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)

        if six.PY3 and isinstance(message, six.string_types):
            message = message.encode()

        self.socket.send(message)

        z_timeout = self.timeout + 50 if self.timeout > 0 else None  # give it a little time for overhead
        socks = dict(poll.poll(z_timeout))
        if socks.get(self.socket) == zmq.POLLIN:
            reply = self.socket.recv()
        else:
            reply = None
            poll.unregister(self.socket)
            self.reconnect()  # reconnect socket otherwise ZMQ socket stuck in unusable state
            poll.register(self.socket, zmq.POLLIN)

        return reply

    def shutdown(self):
        if not self.socket.closed:
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()

    @classmethod
    def create(cls, zmq_context, endpoint):
        """Create new client transport.

        Instead of creating the socket yourself, you can call this function and
        merely pass the :py:class:`zmq.core.context.Context` instance.

        By passing a context imported from :py:mod:`zmq.green`, you can use
        green (gevent) 0mq sockets as well.

        :param zmq_context: A 0mq context.
        :param endpoint: The endpoint the server is bound to.
        """
        socket = zmq_context.socket(zmq.REQ)
        socket.connect(endpoint)
        return cls(socket, zmq_context, endpoint)