#!/usr/bin/env python

from contacts.io import reader
from contacts.tests import contactstest


class ReaderTest(contactstest.ContactsTest):
    def setUp(self):
        self._reads = []
        self._reads.append((reader.CsvReader(readOptions={'delimiter': ':'}),
                            self.csvDelimiterFile))
        self._reads.append((reader.CsvReader(), self.csvFile))
        self._reads.append((reader.YamlReader(), self.yamlFile))
        self._reads.append((reader.PickleReader(), self.pickleFile))

    def testRead(self):
        def compareRecords():
            records = readObj.read(inputFile)
            self.assertEqual(records, self.records)

        for readObj, inputFile in self._reads:
            compareRecords()


if __name__ == '__main__':
    ReaderTest.main()
