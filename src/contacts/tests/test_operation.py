#!/usr/bin/env python

from contacts import operation
from contacts.tests import contactstest
from contacts.exception import DeSerialisationOperationException


class OperationTest(contactstest.ContactsTest):
    def setUp(self):
        self._operations = self._createOperations(self.readers, self.writers,
                                                  [item[0] for item
                                                   in
                                                   self.inputFileReaderNameMaps],
                                                  [item[0] for item
                                                   in
                                                   self.outputFileWriterNameMaps]
                                                  )
        self._operationsWithWrongInputFiles = self._createOperations(
            self.readers, self.writers,
            ('invalidFile', self.yamlFile,),
            [item[0] for item
             in
             self.outputFileWriterNameMaps]
            )

    def _createOperations(self, readers, writers, inputFiles, outputFiles):
        operations = []
        for readerObj, writerObj, inputFile, outputFile in zip(readers,
                                                               writers,
                                                               inputFiles,
                                                               outputFiles
                                                               ):
            operations.append(
                operation.Operation(reader=readerObj, writer=writerObj,
                                    inputFile=inputFile, outputFile=outputFile))
        return operations

    def testRun(self):
        for operationObj in self._operations:
            self.assertEqual(operationObj.run(), (True, self.records))

        for operationObj in self._operationsWithWrongInputFiles:
            self.assertRaises(DeSerialisationOperationException,
                              operationObj.run)


if __name__ == '__main__':
    OperationTest.main()
