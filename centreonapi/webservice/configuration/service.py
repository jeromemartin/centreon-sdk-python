# -*- coding: utf-8 -*-


import centreonapi.webservice.configuration.common as common

from centreonapi.webservice.configuration.macro import Macro
from centreonapi.webservice.configuration.common.centreonnotifyobject import CentreonNotifyObject


class ServiceTemplate(CentreonNotifyObject):

    def __init__(self, properties):
        super(ServiceTemplate, self).__init__()
        self._clapi_action = 'STPL'
        self.id = properties.get('id')
        self.alias = properties.get('alias')

        self.description = properties.get('description')
        self.check_command = properties.get('check command')
        self.check_command_args = properties.get('check command arg')
        self.max_check_attempts = properties.get('max check attempts')
        self.normal_check_interval = properties.get('normal check interval')
        self.passive_checks_enabled = properties.get('passive checks enabled')
        self.retry_check_interval = properties.get('retry check interval')
        self.active_check_enabled = properties.get('active checks enabled')

        self.name = self.description

        self.macros = dict()

    def getmacro(self):
        self.macros.clear()
        state, macro = self.webservice.call_clapi(
            'getmacro',
            self._clapi_action,
            self.reference)
        if state:
            if len(macro['result']) > 0:
                for m in macro['result']:
                    macro_obj = ServiceMacro(m)
                    self.macros[macro_obj.name] = macro_obj
                return state, self.macros
            else:
                return state, self.macros
        else:
            return state, macro

    def setmacro(self, name, value, is_password=None, description=None):
        if description is None:
            description = ''
        if is_password is None:
            is_password = 0
        values = self.reference + [name, value, is_password, description]
        return self.webservice.call_clapi(
            'setmacro',
            self._clapi_action,
            values)

    def deletemacro(self, macro):
        values = self.reference + ["|".join(common.build_param(macro, ServiceMacro))]
        return self.webservice.call_clapi(
            'delmacro',
            self._clapi_action,
            values)

    def enable(self):
        s, e = self.webservice.call_clapi(
            'enable',
            self._clapi_action,
            self.reference)
        if s:
            self.activate = "1"
        return s, e

    def disable(self):
        s, e = self.webservice.call_clapi(
            'disable',
            self._clapi_action,
            self.reference)
        if s:
            self.activate = "0"
        return s, e


class Service(ServiceTemplate):

    def __init__(self, properties):
        super(Service, self).__init__(properties)
        self._clapi_action = 'SERVICE'
        self.hostid = properties.get('host id')
        self.hostname = properties.get('host name')
        self.activate = properties.get('activate')
        self.name = self.hostname + '|' + self.description

    @property
    def reference(self):
        return [self.hostname, self.description]


class ServiceMacro(Macro):
    ENGINE_NAME = "SERVICE"


class Services(common.CentreonDecorator, common.CentreonClass):
    """
    Centreon Web Service Object
    """

    def __init__(self):
        super(Services, self).__init__()
        self.services = dict()
        self._clapi_action = 'SERVICE'

    def __contains__(self, item):
        return item in self.services.keys() or None

    def __getitem__(self, item):
        if not self.services:
            self.list()
        if item in self.services.keys():
            return True, self.services[item]
        else:
            return False, None

    @common.CentreonDecorator.pre_refresh
    def get(self, host, name):
        return self[(host, name)]

    @common.CentreonDecorator.pre_refresh
    def exists(self, host, name):
        return (host, name) in self

    def _refresh_list(self):
        self.services.clear()
        state, service = self.webservice.call_clapi(
            'show',
            self._clapi_action)
        if state and len(service['result']) > 0:
            for s in service['result']:
                service_obj = Service(s)
                self.services[(service_obj.hostname, service_obj.description)] = service_obj

    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.services

    @common.CentreonDecorator.post_refresh
    def add(self, hostname, servicename, template):
        values = [hostname, servicename, template]
        return self.webservice.call_clapi('add',
                                          self._clapi_action,
                                          values)

    @common.CentreonDecorator.post_refresh
    def delete(self, service):
        return self.webservice.call_clapi('del',
                                          self._clapi_action,
                                          [service.hostname,
                                           service.name])
    #
    # def setparam(self, service, name, value):
    #     values = [service.hostname, service.name, name, value]
    #     return self.webservice.call_clapi('setparam', self._clapi_action, values)

    #
    # def setseverity(self, hostname, servicename, name):
    #     values = [hostname, servicename, name]
    #     return self.webservice.call_clapi('setseverity', 'SERVICE', values)
    #
    # def unsetseverity(self, hostname, servicename):
    #     values = [hostname, servicename]
    #     return self.webservice.call_clapi('unsetseverity', 'SERVICE', values)
    #
    # def getcontact(self, hostname, servicename):
    #     values = [hostname, servicename]
    #     return self.webservice.call_clapi('getcontact', 'SERVICE', values)
    #
    # def addcontact(self, hostname, servicename, contact):
    #     values = [hostname, servicename, contact]
    #     return self.webservice.call_clapi('addcontact', 'SERVICE', values)
    #
    # def setcontact(self, hostname, servicename, contact):
    #     values = [hostname, servicename, '|'.join(contact)]
    #     return self.webservice.call_clapi('setcontact', 'SERVICE', values)
    #
    # def getcontactgrup(self, hostname, servicename):
    #     values = [hostname, servicename]
    #     return self.webservice.call_clapi('getcontactgroup', 'SERVICE', values)
    #
    # def setcontactgroup(self, hostname, servicename, contact):
    #     values = [hostname, servicename, '|'.join(contact)]
    #     return self.webservice.call_clapi('setcontactgroup', 'SERVICE', values)
    #
    # def delcontactgroup(self, hostname, servicename, contact):
    #     try:
    #         for i in contact:
    #             values = [hostname, servicename, i]
    #             self.webservice.call_clapi('delcontactgroup',
    #                                        'SERVICE',
    #                                        values)
    #         return True
    #     except Exception:
    #         return False
    #


class ServiceTemplates(Services):

    def __init__(self):
        super(ServiceTemplates, self).__init__()
        self._clapi_action = 'STPL'

    @common.CentreonDecorator.post_refresh
    def add(self, servicename, alias, template):
        values = [servicename, alias, template]
        return self.webservice.call_clapi('add',
                                          self._clapi_action,
                                          values)

    def _refresh_list(self):
        self.services.clear()
        state, service = self.webservice.call_clapi(
            'show',
            self._clapi_action)
        if state and len(service['result']) > 0:
            for s in service['result']:
                service_obj = ServiceTemplate(s)
                self.services[service_obj.description] = service_obj
