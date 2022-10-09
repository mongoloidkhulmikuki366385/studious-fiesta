import datetime
import threading

import zmq

PUB_CHANNEL = '101'
DEBUG = 3
INFO = 2
CRITICAL = 1
REPORTER = 0


class Publisher(object):

    def __init__(self, identity):
        self.identity = identity

    def publish(self, msg, id_postfix=None, level=DEBUG):
        t = datetime.datetime.now()
        ts = datetime.datetime.strftime(t, '%m-%d_%H:%M:%S.%f')
        id_str = self.identity
        if id_postfix:
            id_str = id_str + '--' + id_postfix
        if hasattr(self, '_send'):
            self._send(ts, id_str, msg, level)


class ZmqPublisher(Publisher):

    def __init__(self, ctx, endpoint, identity):
        super(ZmqPublisher, self).__init__(identity)
        self.publisher = ctx.socket(zmq.PUB)
        self.publisher.setsockopt(zmq.IDENTITY, identity)
        self.publisher.bind(endpoint)
        self.lock = threading.Lock()

    def _send(self, ts, id_str, msg, level):
        # zmq socket is not thread safe
        self.lock.acquire()
        self.publisher.send_multipart([str(PUB_CHANNEL), str(ts),
                                       str(level), str(id_str), str(msg)])
        self.lock.release()

    def stop(self):
        if not self.publisher.closed:
            if zmq is None:
                # the zmq module may have been released by this time
                return
            self.publisher.setsockopt(zmq.LINGER, 0)
            self.publisher.close()

    def __del__(self):
        self.stop()
