import pickle
import yaml
from abc import ABCMeta, abstractmethod
import csv


class Writer(object):
    __metaclass__ = ABCMeta

    def __init__(self, writeOptions=None):
        """
        :param dict writeOptions: options which will be used by write method.
        """
        self._writeOptions = writeOptions or {}

    @abstractmethod
    def write(self):
        raise NotImplementedError


class PickleWriter(Writer):
    """
    Native serializing by pickle.
    """

    def write(self, filePath, records):
        """
        :param str filePath: output file path.
        :param `contacts.records.Records` records: records object will be
        write.
        """
        with open(filePath, 'wb') as f:
            return pickle.dump(records.obj, f, **self._writeOptions)


class YamlWriter(Writer):
    """
    Serializing by json format.
    """

    def write(self, filePath, records):
        """
        :param str filePath: output file path.
        :param `contacts.records.Records` records: records object will be
        write.
        """
        with open(filePath, 'w') as f:
            return yaml.dump(records.obj, f, **self._writeOptions)


class CsvWriter(Writer):
    """
    Serializing by csv format, in fact, just save it as a .cvs file.
    """

    def __init__(self, **kwargs):
        super(CsvWriter, self).__init__(**kwargs)
        self._writeOptions.setdefault('delimiter', '\t')

    def write(self, filePath, records):
        """
        :param str filePath: output file path.
        :param `contacts.records.Records` records: records object will be
        write.
        """
        delimiter = self._writeOptions.get('delimiter', '\t')
        # TODO: there is a issue for writing, the format is not correct.
        with open(filePath, 'wb') as f:
            csvWriter = csv.writer(f, **self._writeOptions)
            csvWriter.writerow(delimiter.join(records.headers))
            for row in records.flattenRows:
                csvWriter.writerow('\n{0}'.format(row))
