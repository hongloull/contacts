#!/usr/bin/env python

from os import path
import subprocess
import itertools

from contacts.tests import contactstest
from contacts.session import Session


class ContactsAppTestCase(contactstest.ContactsTest):
    def setUp(self):
        # make sure contactsBin exist both in src and installed package
        # directories.
        contactsBin = path.join(self.srcDir, '..', 'bin', 'contacts')
        if not path.isfile(contactsBin):
            contactsBin = 'contacts'
        self._appPath = contactsBin

    def _getCmds(self, displayerNames=None,
                 inputFileReaderNameMaps=None,
                 withWriter=False,
                 outputFileWriterNameMaps=None
                 ):
        """
        Get writing(serialisation) commands list, each command looks as below:
        "contacts -d <> -i <> -r <> -w <>"
        :param bool withWriter: If False, just list reader commands,
        else list writer commands.
        :rtype: `list(str)`
        """
        displayerNames = displayerNames or Session.DISPLAYER_MAPS.keys()
        inputFileReaderNameMaps = inputFileReaderNameMaps or \
                                  self.inputFileReaderNameMaps
        outputFileWriterNameMaps = outputFileWriterNameMaps or \
                                   self.outputFileWriterNameMaps

        displayerNames = (
            '-d {displayerName}'.format(displayerName=displayerName) for
            displayerName in displayerNames)
        inputFiles = (
            '-i {inputFile} -r {readerName}'.format(inputFile=inputFile,
                                                    readerName=readerName) for
            inputFile, readerName in inputFileReaderNameMaps)
        if not withWriter:
            return self._product((self._appPath,), displayerNames, inputFiles)
        else:
            outputFiles = (
                '-o {outputFile} -w {writerName}'.format(outputFile=outputFile,
                                                         writerName=writerName)
                for
                outputFile, writerName in outputFileWriterNameMaps)
        return self._product((self._appPath,), displayerNames, inputFiles,
                             outputFiles)

    def _product(self, *args):
        """
        Example:
            _produt(('a',),('A','B'),('0','1','2')) get below list:
            ['aA0','aB0','aA1',...]
        """
        return [' '.join(item) for item in itertools.product(*args)]

    def testMain(self):
        # test commands with correct arguments
        for withWriter in (False, True):
            for cmd in self._getCmds(
                    displayerNames=Session.DISPLAYER_MAPS.keys(),
                    withWriter=withWriter,
                    inputFileReaderNameMaps=self.inputFileReaderNameMaps,
                    outputFileWriterNameMaps=self.outputFileWriterNameMaps):
                self.assertEqual(subprocess.check_call(cmd, shell=True), 0)

        # test commands with invalid arguments
        # Cmds looks as below:
        #     ontacts -d invalidDisplayerName -i addressbook.csv -r csv
        for cmd in self._getCmds(displayerNames=self.invalidDisplayerNames):
            # TODO: comment below line since it raises
            # subprocess.CalledProcessError
            # self.assertRaises(SessionArgsInvalid, subprocess.check_call,
            # cmd,shell=True)
            pass

        # test some special cases
        # no arguments which should just print help and exit
        subprocess.check_call('{0} --help'.format(self._appPath), shell=True)


if __name__ == '__main__':
    ContactsAppTestCase.main()
