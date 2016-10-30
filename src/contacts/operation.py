from contacts.exception import DeSerialisationOperationException, \
    SerialisationOperationException
from contacts.io import log


class Operation(object):
    """
    Class to do the actual operation. There are two operations right now,
    one is deserialication(reading/loading) and the other is serialication(
    writing/dumping). If need to add new operations(e.g. add, remove or
    replace), it can be add here.
    Operation calls Reader and Writer for reading and writing.
    """

    def __init__(self, reader=None, writer=None, inputFile='',
                 outputFile=''):
        """
        :param `contacts.io.Reader` reader: Reader object.
        :param `contacts.io.Writer` writer: Writer object.
        :param `str` inputFile: source file to read.
        :param `str` outputFile: dest file to write.
        """
        self._reader = reader
        self._writer = writer
        self._inputFile = inputFile
        self._outputFile = outputFile

    def run(self):
        """
        Serialise/deserialise.
        :return: a tuple which first item is Status and the second is Records.
        :rtype: `tuple(bool,records)`
        """
        try:
            records = self._reader.read(self._inputFile)
        except Exception as e:
            log.error('Failed to read/deserialise {0}.'.format(self._inputFile))
            raise DeSerialisationOperationException(e)
        else:
            log.write(
                'Read/deserialise {0} successfully.'.format(self._inputFile))

        if self._outputFile:
            try:
                # serialise if output file specified
                self._writer.write(self._outputFile, records)
            except Exception as e:
                log.error(
                    'Failed to write/serialise {0}.'.format(self._outputFile))
                raise SerialisationOperationException(e)
            else:
                log.write('Wrote/serialised {0} successfully.'.format(
                    self._outputFile))

        return True, records
