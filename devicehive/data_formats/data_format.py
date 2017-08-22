class DataFormat(object):
    """Data format class."""

    TEXT_DATA_TYPE = 'text'
    BINARY_DATA_TYPE = 'binary'

    def __init__(self, name, data_type):
        self._name = name
        self._data_type = data_type

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    @property
    def text_data_type(self):
        return self._data_type == self.TEXT_DATA_TYPE

    @property
    def binary_data_type(self):
        return self._data_type == self.BINARY_DATA_TYPE

    def encode(self, data):
        raise NotImplementedError

    def decode(self, data):
        raise NotImplementedError
