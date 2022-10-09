#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"

import zmq
from rpcclient_transport import ZmqClientTransport
from Common.jsonrpc import JSONRPCProtocol


class RPCClient(object):
    """Client for making RPC calls to connected servers.

    :param protocol: An :py:class:`~tinyrpc.RPCProtocol` instance.
    :param transport: A :py:class:`~tinyrpc.transports.ClientTransport`
                      instance.
    """

    def __init__(self, protocol, transport, publisher, retries=1):
        self.protocol = protocol
        self.transport = transport
        self.publisher = publisher
        self.retries = retries

    def _send_and_handle_reply(self, req):
        for i in range(self.retries):
            s_req = req.serialize()
            reply = self.transport.send_reply(s_req)
            self.log(s_req, 'sent')
            if reply:
                response = self.protocol.parse_reply(reply)
                if response.unique_id != req.unique_id:
                    self.log('Reply ID {0} is not matching Request ID {1}'.format(req.unique_id, response.unique_id))
                    return None
                self.log(response.serialize(), 'received')
                return response
            else:
                self.log(
                    'timed out waiting for response to req[' + req.unique_id + '], retries=' + str(
                        self.retries - i - 1))
        return None

    def log(self, *args):
        if self.publisher:
            self.publisher.publish(*args)

    def call(self, method, *args, **kwargs):
        """Calls the requested method and returns the result.

        If an error occured, an :py:class:`~tinyrpc.exc.RPCError` instance
        is raised.

        :param method: Name of the method to call.
        :param args: Arguments to pass to the method.
        :param kwargs: Keyword arguments to pass to the method.
        :param one_way: Whether or not a reply is desired.
        """
        if 'timeout' in kwargs:
            default_timeout = self.transport.timeout
            self.transport.timeout = kwargs['timeout']

        req = self.protocol.create_request(method, *args, **kwargs)

        result = self._send_and_handle_reply(req)

        if 'timeout' in kwargs:
            self.transport.timeout = default_timeout

        return result

    def get_proxy(self, prefix='', one_way=False):
        """Convenience method for creating a proxy.

        :param prefix: Passed on to :py:class:`~tinyrpc.client.RPCProxy`.
        :param one_way: Passed on to :py:class:`~tinyrpc.client.RPCProxy`.
        :return: :py:class:`~tinyrpc.client.RPCProxy` instance."""
        return RPCProxy(self, prefix, one_way)


class RPCProxy(object):
    """Create a new remote proxy object.

    Proxies allow calling of methods through a simpler interface. See the
    documentation for an example.

    :param client: An :py:class:`~tinyrpc.client.RPCClient` instance.
    :param prefix: Prefix to prepend to every method name.
    :param one_way: Passed to every call of
                    :py:func:`~tinyrpc.client.call`.
    """

    def __init__(self, client, prefix='', one_way=False):
        self.client = client
        self.prefix = prefix
        self.one_way = one_way

    def __getattr__(self, name):
        """Returns a proxy function that, when called, will call a function
        name ``name`` on the client associated with the proxy.
        """
        proxy_func = lambda *args, **kwargs: self.client.call(
            self.prefix + name,
            *args,
            **kwargs
        )
        return proxy_func


class RPCClientWrapper:
    def __init__(self, transport, publisher, ctx=None, protocol=None):
        self.ctx = ctx if ctx else zmq.Context().instance()
        if isinstance(transport, ZmqClientTransport):
            self.transport = transport
        else:
            if 'tcp' not in str(transport):
                transport = "tcp://*:" + str(transport)
            self.transport = ZmqClientTransport.create(self.ctx, transport)

        self.protocol = protocol if protocol else JSONRPCProtocol()
        self.publisher = publisher
        self.transport.publisher = publisher

        self.rpc_client = RPCClient(self.protocol, self.transport, self.publisher, retries=1)

    def remote_server(self):
        return self.rpc_client.get_proxy()

    def hijack(self, mock, func=None):
        self.rpc_client._send_and_handle_reply = mock