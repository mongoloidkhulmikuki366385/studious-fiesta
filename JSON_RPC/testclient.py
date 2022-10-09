#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"


import cmd
import zmq
from RPCClient.rpc_client import RPCClientWrapper
import threading

TEST_ENGINE_PORT = 6150
SEQUENCER_PORT = 6200


class EngineCLI(cmd.Cmd):
    prompt = 'test engine>'
    intro = 'Dummy Engine driver'

    def default(self, line):
        print self.proxy.__getattr__(line)().result


def start_client(site):
    # sub = submessage()
    cli = EngineCLI()
    cli.proxy = RPCClientWrapper(
        'tcp://127.0.0.1' + ':' + str(TEST_ENGINE_PORT + site),
        publisher=None
    ).remote_server()
    # sub.start()
    cli.cmdloop()


# class submessage(threading.Thread):
#     def __init__(self, site=0):
#         super(submessage, self).__init__()
#         ctx = zmq.Context().instance()
#         self.subscriber = ctx.socket(zmq.SUB)
#         # self.subscriber.connect('9150')
#         self.subscriber.setsockopt(zmq.SUBSCRIBE, '101')
#         self.lock = threading.Lock()
#
#     def run(self):
#         while True:
#             self.lock.acquire()
#             result = self.subscriber.recv_multipart()
#             print "sub>>>>>>", result
#             self.lock.release()


if __name__ == '__main__':
    # cli = testclient()
    # cli.add()
    # submessage(0)
    start_client(0)