from os import path
from tempfile import NamedTemporaryFile
import unittest
import inspect

from contacts.io import reader, writer


def getTempFile():
    """
    Create named temp file.
    :return: temp file name
    :rtype: str
    """
    with NamedTemporaryFile('w+t', delete=True) as f:
        return f.name


class ContactsTest(unittest.TestCase):
    """
    Base class for unit test, all TestCase should inherit this to get init data.
    """

    srcDir = path.dirname(path.dirname(
        path.dirname(inspect.getfile(inspect.currentframe()))))

    _dataDir = path.join(srcDir, 'data')
    csvFile = path.join(_dataDir, 'addressbook.csv')
    # csv file with delimiter ":"
    csvDelimiterFile = path.join(_dataDir,
                                 'addressbook_delimiter.csv')
    pickleFile = path.join(_dataDir, 'addressbook.pik')
    yamlFile = path.join(_dataDir, 'addressbook.yaml')

    inputFileReaderNameMaps = (
        (csvFile, 'csv'), (pickleFile, 'pickle'),
        (yamlFile, 'yaml'))

    outputFileWriterNameMaps = (
        (getTempFile(), 'csv'), (getTempFile(), 'pickle'),
        (getTempFile(), 'yaml'))

    # store records object
    records = reader.PickleReader().read(pickleFile)

    invalidDisplayerNames = ['invalidDisplayerName']
    invalidReaderNames = ['invalidReaderName']
    invalidWriterNames = ['invalidWriteName']
    invalidReadOptions = ['invalidReadOptions',
                          'invalidReadOptions=']
    invalidWriteOptions = ['invalidWriteOptions',
                           'invalidWriteOptions=']

    # make readers
    pickleReader = reader.PickleReader()
    csvReader = reader.CsvReader()
    yamlReader = reader.YamlReader()
    readers = (csvReader, pickleReader, yamlReader)

    # make writers
    pickleWriter = writer.PickleWriter()
    csvWriter = writer.CsvWriter()
    yamlWriter = writer.YamlWriter()
    writers = (csvWriter, pickleWriter, yamlWriter)

    def __init__(self, *args, **kwargs):
        super(ContactsTest, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    ContactsTest()
