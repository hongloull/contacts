#!/usr/bin/env python

from contacts import session
from contacts.tests import contactstest


class SessionTest(contactstest.ContactsTest):
    def setUp(self):
        self._sessions = []
        self._outputFiles = [contactstest.getTempFile() for i in range(4)]
        for displayerName in ['text', 'html']:
            for readerName, writeName, inputFile, outputFile in zip(['csv',
                                                                     'csv',
                                                                     'pickle',
                                                                     'yaml'],
                                                                    ['csv',
                                                                     'csv',
                                                                     'pickle',
                                                                     'yaml'],
                                                                    [
                                                                        self.csvFile,
                                                                        self.csvDelimiterFile,
                                                                        self.pickleFile,
                                                                        self.yamlFile],
                                                                    self._outputFiles):
                self._sessions.append(session.Session(
                    inputFile=inputFile,
                    displayerName=displayerName,
                    outputFile=outputFile,
                    readerName=readerName,
                    writerName=writeName))

                self._sessions.append(session.Session(
                    inputFile=inputFile,
                    displayerName=displayerName,
                    readerName=readerName))

    def testRun(self):
        for sessionObj in self._sessions:
            sessionObj.main()


if __name__ == '__main__':
    SessionTest.main()
