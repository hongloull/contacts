
from contacts.io import reader, writer


class AbsFormat(object):
    _READER_CLASS = reader.DefaultReader
    _WRITER_CLASS = writer.DefaultWriter

    def __init__(self):
        self.reader = self._READER_CLASS()
        self.writer = self._WRITER_CLASS()


class DefaultFormat(AbsFormat):
    _READER_CLASS = reader.DefaultReader
    _WRITER_CLASS = writer.DefaultWriter


class JosnFormat(AbsFormat):
    _READER_CLASS = reader.JsonReader
    _WRITER_CLASS = writer.JsonWriter
