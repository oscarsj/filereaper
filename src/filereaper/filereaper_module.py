class FileReaperModule(object):

    name = None
    _attributes = None

    def __init__(self, name, items):
        self._attributes = list()
        self.name = name
        for item in items:
            value = self._normalizeTypes(item[1])
            self._attributes.append(item[0])
            setattr(self, item[0], value)

    def _normalizeTypes(self, value):
        if isinstance(value, bool) or value in ['True', 'False',
                                                'true', 'false']:
            return bool(value)
        try:
            return int(value)
        except ValueError:
            pass
        return value

    @property
    def attributes(self):
        return self._attributes
