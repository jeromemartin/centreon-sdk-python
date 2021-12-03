class Macro:
    ENGINE_NAME = ""

    def __init__(self, properties):
        self.internal_name = properties.get('macro name')
        self.value = properties.get('macro value')
        self.description = properties.get('description', '')
        self.is_password = properties.get('is_password')
        self.source = properties.get('source')
        if self.is_password == '':
            self.is_password = 0
        if self.internal_name.startswith("$"):
            self.name = self.internal_name.replace(f"$_{self.ENGINE_NAME}", "")[:-1]

    def __repr__(self):
        return self.internal_name

    def __str__(self):
        return self.internal_name
