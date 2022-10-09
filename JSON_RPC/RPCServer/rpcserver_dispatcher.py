#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"


import os
import six
import traceback
import inspect


class RPCDispatcher(object):

    def __init__(self):
        self.method_map = {}
        self.subdispatchers = {}

    def add_subdispatch(self, dispatcher, prefix=''):
        self.subdispatchers.setdefault(prefix, []).append(dispatcher)

    def add_method(self, f, name=None):
        assert callable(f), "method argument must be callable"
        if not name:
            name = f.__name__

        if name in self.method_map:
            raise Exception('Name %s already registered' % name)

        self.method_map[name] = f

    def dispatch(self, request):
        if hasattr(request, 'create_batch_response'):
            results = [self._dispatch(req) for req in request]

            response = request.create_batch_response()
            if response:
                response.extend(results)

            return response
        else:
            return self._dispatch(request)

    def _dispatch(self, request):
        try:
            try:
                method = self.get_method(request.method)
            except Exception as e:
                return request.error_respond(e)

            # we found the method
            try:
                result = method(*request.args, **request.kwargs)
            except Exception as e:
                # an error occurred within the method, return it
                return request.error_respond(e)

            # respond with result
            return request.respond(result)
        except Exception as e:
            # unexpected error, do not let client know what happened
            return request.error_respond(Exception(e.message + os.linesep + traceback.format_exc()))

    def get_method(self, name):
        if name in self.method_map:
            return self.method_map[name]

        for prefix, subdispatchers in six.iteritems(self.subdispatchers):
            if name.startswith(prefix):
                for sd in subdispatchers:
                    try:
                        return sd.get_method(name[len(prefix):])
                    except KeyError:
                        pass

        raise Exception('Method not found: ' + name)

    def public(self, name=None):
        if callable(name):
            self.add_method(name)
            return name

        def _(f):
            self.add_method(f, name=name)
            return f

        return _

    def register_instance(self, obj, prefix=''):
        dispatch = self.__class__()
        for name, f in inspect.getmembers(
                obj, lambda f: callable(f) and hasattr(f, '_rpc_public_name')
        ):
            dispatch.add_method(f, f._rpc_public_name)

        # add to dispatchers
        self.add_subdispatch(dispatch, prefix)