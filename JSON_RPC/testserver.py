#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"


import threading
import zmq
from RPCServer.rpc_server import RPCServerWrapper
from RPCServer.rpcserver_dispatcher import RPCDispatcher
from function_map import FunctionMap


TEST_ENGINE_PUB = 6100
TEST_ENGINE_PORT = 6150


class TestEngine(RPCDispatcher):
        def __init__(self, site):
            super(TestEngine, self).__init__()
            self.site = site
            self.func_map = FunctionMap()

        def register_modules_public_methods(self):
            _function = {
                'add': self.func_map.add,
                'sub': self.func_map.sub,
                'mul': self.func_map.mul,
                'chu': self.func_map.chu,
                'hello': self.func_map.hello
            }
            for name, obj in _function.items():
                self.add_method(obj, name)


class TestServer(threading.Thread):
    def __init__(self):
        super(TestServer, self).__init__()

        self.site = 0
        ctx = zmq.Context()
        self.pub_endpoint = "tcp://127.0.0.1:" + str(TEST_ENGINE_PUB + self.site)

        self.test_engine = TestEngine(self.site)

        self.server_wrapper = RPCServerWrapper(
            TEST_ENGINE_PORT + self.site,
            ctx=ctx,
            dispatcher=self.test_engine
        ).rpc_server

        self.test_engine.register_modules_public_methods()

    def run(self):
        self.server_wrapper.serve_forever()


if __name__ == '__main__':
    ts = TestServer()
    ts.start()

