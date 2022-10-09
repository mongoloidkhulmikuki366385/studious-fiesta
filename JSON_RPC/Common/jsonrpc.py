#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import RPCResponse, RPCRequest, RPCProtocol

from uuid import uuid1

import json
import six


class JSONRPCSuccessResponse(RPCResponse):

    def _to_dict(self):
        return {
            'jsonrpc': JSONRPCProtocol.JSON_RPC_VERSION,
            'id': self.unique_id,
            'result': self.result,
        }

    def serialize(self):
        return json.dumps(self._to_dict())


class JSONRPCErrorResponse(RPCResponse):

    def _to_dict(self):
        return {
            'jsonrpc': JSONRPCProtocol.JSON_RPC_VERSION,
            'id': self.unique_id,
            'error': {
                'message': str(self.error),
                'code': self._jsonrpc_error_code,
            }
        }

    def serialize(self):
        return json.dumps(self._to_dict())


class JSONRPCRequest(RPCRequest):
    def error_respond(self, error):
        if not self.unique_id:
            return None

        response = JSONRPCErrorResponse()

        code = -32000
        if hasattr(error, 'jsonrpc_error_code'):
            code = error.jsonrpc_error_code

        response.error = error.message
        response.unique_id = self.unique_id
        response._jsonrpc_error_code = code
        return response

    def respond(self, result):
        response = JSONRPCSuccessResponse()

        if not self.unique_id:
            return None

        response.result = result
        response.unique_id = self.unique_id

        return response

    def __eq__(self, other):
        if self.method != other.method:
            return False
        if self.args != other.args:
            return False
        if self.kwargs != other.kwargs:
            return False
        return True

    def _to_dict(self):
        jdata = {
            'jsonrpc': JSONRPCProtocol.JSON_RPC_VERSION,
            'method': self.method,
        }
        if self.args:
            jdata['args'] = self.args
        if self.kwargs:
            jdata['kwargs'] = self.kwargs
        if self.unique_id:
            jdata['id'] = self.unique_id
        return jdata

    def serialize(self):
        return json.dumps(self._to_dict())


class JSONRPCProtocol(RPCProtocol):
    """JSONRPC protocol implementation.

    Currently, only version 2.0 is supported."""

    JSON_RPC_VERSION = "2.0"
    _ALLOWED_REPLY_KEYS = sorted(['id', 'jsonrpc', 'error', 'result'])
    _ALLOWED_REQUEST_KEYS = sorted(['id', 'jsonrpc', 'method', 'args', 'kwargs'])

    def __init__(self, *args, **kwargs):
        super(JSONRPCProtocol, self).__init__(*args, **kwargs)
        self._id_counter = 0

    def _get_unique_id(self):
        return uuid1().hex

    # def create_request(self, method, *args, **kwargs, one_way=False):
    def create_request(self, method, *args, **kwargs):
        request = JSONRPCRequest()

        if 'one_way' not in kwargs:
            request.unique_id = self._get_unique_id()

        request.method = method
        request.args = list(args)
        request.kwargs = kwargs
        return request

    def parse_reply(self, data):

        if six.PY3 and isinstance(data, bytes):
            data = data.decode()
        try:
            rep = json.loads(data)
        except Exception as e:
            pass

        if 'error' in rep:
            response = JSONRPCErrorResponse()
            error = rep['error']
            response.error = error['message']
            response._jsonrpc_error_code = error['code']
        else:
            response = JSONRPCSuccessResponse()
            response.result = rep.get('result')

        response.unique_id = rep['id']

        return response

    def parse_request(self, data):
        if six.PY3 and isinstance(data, bytes):
            data = data.decode()

        try:
            req = json.loads(data)
            return self._parse_subrequest(req)
        except Exception as e:
            # raise JSONRPCParseError()
            raise e, 'parse_request->json.loads error'

    def _parse_subrequest(self, req):
        for k in six.iterkeys(req):
            if not k in self._ALLOWED_REQUEST_KEYS:
                # raise JSONRPCInvalidRequestError()
                pass

        if req.get('jsonrpc', None) != self.JSON_RPC_VERSION:
            # raise JSONRPCInvalidRequestError()
            pass

        if not isinstance(req['method'], six.string_types):
            # raise JSONRPCInvalidRequestError()
            pass

        request = JSONRPCRequest()
        request.method = str(req['method'])
        request.unique_id = req.get('id')

        if 'args' in req:
            request.args = req['args']
        if 'kwargs' in req:
            request.kwargs = req['kwargs']
        return request

    def stop_respond(self):
        response = JSONRPCSuccessResponse()
        response.unique_id = '0'
        response.result = 'PASS'
        return response

    def error_respond(self, error, original_request):
        response = JSONRPCErrorResponse()

        code = error.jsonrpc_error_code

        response.error = error.message
        if original_request:
            response.unique_id = original_request.unique_id
        response._jsonrpc_error_code = code
        return response
