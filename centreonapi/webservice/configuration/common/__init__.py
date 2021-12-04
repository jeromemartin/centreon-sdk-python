# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice


def build_param(param=None, objecttype=None, attr='name'):
    if param is None:
        return param
    #    raise ("Param must be defined")
    param_list = list()
    return_list = list()
    if not isinstance(param, list):
        param_list.append(param)
    else:
        param_list = list(param)
    for k in param_list:
        if isinstance(k, str):
            return_list.append(k)
        elif isinstance(k, objecttype):
            return_list.append(k.__dict__[attr])
    return return_list


class CentreonDecorator(object):

    @staticmethod
    def post_refresh(func):
        """
        Decorator that call __refresh_list() after func unless
        function's call contains 'post_refresh=False'
        eg:
            @post_refresh
            def hello(w, post_refresh=False):
                ...
        """

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # args[0] is always self
            # https://coderwall.com/p/jo39na/python-decorators-using-self
            if kwargs.get("post_refresh", True):
                args[0]._refresh_list()
            return result

        return wrapper

    @staticmethod
    def pre_refresh(func):
        def wrapper(*args, **kwargs):
            args[0]._refresh_list()
            return func(*args, **kwargs)

        return wrapper

    def _refresh_list(self):
        pass


class CentreonClass(object):

    def __init__(self):
        self.webservice = Webservice.getInstance()
        self._clapi_action = ""

    @CentreonDecorator.pre_refresh
    def get(self, name, pre_refresh=False):
        return self[name] or None

    @CentreonDecorator.pre_refresh
    def exists(self, name, pre_refresh=False):
        return name in self

    def list(self):
        pass


class CentreonObject(object):
    OBJECT_PARAMETERS = list()

    def __init__(self):
        self.webservice = Webservice.getInstance()
        self._clapi_action = ""
        self.name = ""
        self.params = dict()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def reference(self):
        return self.name

    def _prepare_values(self, *values):
        if isinstance(self.reference, list):
            return self.reference + list(values)
        else:
            return [self.reference] + list(values)

    def setparam(self, name, value):
        if self.OBJECT_PARAMETERS and name not in self.OBJECT_PARAMETERS:
            return False, f"No parameter {name}"

        values = self._prepare_values(name, value)
        self.params[name] = value
        return self.webservice.call_clapi(
            'setparam',
            self._clapi_action,
            values)

    def getparam(self, name):
        if self.OBJECT_PARAMETERS and name not in self.OBJECT_PARAMETERS:
            return False, f"No parameter {name}"

        values = self._prepare_values(name)
        state, res = self.webservice.call_clapi('getparam', self._clapi_action, values)
        if state:
            res = res['result']
            if len(res) == 1:
                self.params[name] = res[0]
                return state, res[0]
            elif len(res) > 1:
                self.params[name] = res
                return state, res
            else:
                return state, None
        else:
            return state, res

    def getparams(self):
        for p in self.OBJECT_PARAMETERS:
            st, res = self.getparam(p)
            if not st:
                return st, res
        return True, self.params
