import centreonapi.webservice.configuration.common as common


class Macro(common.CentreonObject):

    def __init__(self, properties):
        self.name = properties.get('macro name')
        self.value = properties.get('macro value')
        self.description = properties.get('description', '')
        self.is_password = properties.get('is_password')
        self.source = properties.get('source')
        if self.is_password == '':
            self.is_password = 0
        self.engine_name = '$_HOST' + self.name + '$'

    def __repr__(self):
        return self.engine_name

    def __str__(self):
        return self.engine_name
