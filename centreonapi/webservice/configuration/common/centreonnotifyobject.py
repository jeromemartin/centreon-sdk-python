import centreonapi.webservice.configuration.common as common
from centreonapi.webservice.configuration.common import CentreonObject
from centreonapi.webservice.configuration.contact import Contact, ContactGroup


class CentreonNotifyObject(CentreonObject):
    def __init__(self):
        super(CentreonNotifyObject, self).__init__()
        self.contacts = dict()
        self.contactgroups = dict()

    def getcontact(self):
        """
        :return: state (True/False), contacts or error message
        """
        state, cs = self.webservice.call_clapi(
            'getcontact',
            self._clapi_action,
            self.reference)
        if state:
            if len(cs['result']) > 0:
                for c in cs['result']:
                    c_obj = Contact(c)
                    self.contacts[c_obj.name] = c_obj
                return state, self.contacts
            else:
                return state, None
        else:
            return state, cs

    def addcontact(self, contacts):
        c = "|".join(common.build_param(contacts, Contact))
        return self.webservice.call_clapi(
            'addcontact',
            self._clapi_action,
            self._prepare_values(c))

    def setcontact(self, contacts):
        c = "|".join(common.build_param(contacts, Contact))
        return self.webservice.call_clapi(
            'setcontact',
            self._clapi_action,
            self._prepare_values(c))

    def deletecontact(self, contacts):
        c = "|".join(common.build_param(contacts, Contact))
        return self.webservice.call_clapi(
            'delcontact',
            self._clapi_action,
            self._prepare_values(c))

    def getcontactgroup(self):
        state, cgs = self.webservice.call_clapi(
            'getcontactgroup',
            self._clapi_action,
            self.reference)
        if state:
            if len(cgs['result']) > 0:
                for c in cgs['result']:
                    cg_obj = ContactGroup(c)
                    self.contactgroups[cg_obj.name] = cg_obj
                return state, self.contactgroups
            else:
                return state, None
        else:
            return state, cgs

    def addcontactgroup(self, contactgroups):
        c = "|".join(common.build_param(contactgroups, ContactGroup))
        return self.webservice.call_clapi(
            'addcontactgroup',
            self._clapi_action,
            self._prepare_values(c))

    def setcontactgroup(self, contactgroups):
        c = "|".join(common.build_param(contactgroups, ContactGroup))
        return self.webservice.call_clapi(
            'setcontactgroup',
            self._clapi_action,
            self._prepare_values(c))

    def deletecontactgroup(self, contactgroups):
        c = "|".join(common.build_param(contactgroups, ContactGroup))
        return self.webservice.call_clapi(
            'delcontactgroup',
            self._clapi_action,
            self._prepare_values(c))
