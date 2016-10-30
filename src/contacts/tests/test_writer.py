#!/usr/bin/env python

from contacts.io import writer, reader
from contacts.tests import contactstest


class WriterTest(contactstest.ContactsTest):
    def setUp(self):
        self._writers = []
        self._writers.append(
            (writer.YamlWriter(), contactstest.getTempFile()))
        self._writers.append(
            (writer.PickleWriter(), contactstest.getTempFile()))

        self._readers = []
        self._readers.append(reader.YamlReader())
        self._readers.append(reader.PickleReader())

    def testWrite(self):
        def compareRecords():
            writeObj.write(outputFile, self.records)
            self.assertEqual(readerObj.read(outputFile), self.records)

        for (writeObj, outputFile), readerObj in zip(self._writers,
                                                     self._readers):
            compareRecords()


if __name__ == '__main__':
    WriterTest.main()
