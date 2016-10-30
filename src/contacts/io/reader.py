import pickle
import yaml
from abc import ABCMeta, abstractmethod
import csv

from contacts import records


class Reader(object):
    __metaclass__ = ABCMeta

    def __init__(self, readOptions=None):
        """
        :param dict readOptions: options which will be used by read method.
        """
        self._readOptions = readOptions or {}

    @abstractmethod
    def read(self):
        raise NotImplementedError


class PickleReader(Reader):
    def read(self, filePath):
        """
        Read pickle file.
        :param str filePath: pickle file path.
        :return: a Record object.
        :rtype: `contacts.records.Record`
        """
        with open(filePath, 'rb') as f:
            return records.Records(obj=pickle.load(f, **self._readOptions))


class CsvReader(Reader):
    def __init__(self, **kwargs):
        super(CsvReader, self).__init__(**kwargs)
        self._readOptions.setdefault('delimiter', '\t')

    def read(self, filePath):
        """
        Read cvs file.
        :param str filePath: cvs file path.
        :return: a Record object.
        :rtype: `contacts.records.Record`
        """
        with open(filePath, 'r') as f:
            lines = f.read().splitlines()
        reader = csv.reader(lines, **self._readOptions)
        headers = reader.next()
        items = []
        for row in reader:
            item = dict()
            for i, header in enumerate(headers):
                item[header] = row[i]
            items.append(item)
        return records.Records(obj=items)


class YamlReader(Reader):
    def read(self, filePath):
        """
        Read yaml file.
        :param str filePath: yaml file path.
        :return: a Record object.
        :rtype: `contacts.records.Record`
        """
        with open(filePath, 'r') as f:
            return records.Records(obj=yaml.load(f, **self._readOptions))
