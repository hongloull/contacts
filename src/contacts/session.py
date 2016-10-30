from os import path

from contacts import operation, displayer
from contacts.io import reader, writer
from contacts.exception import SessionArgsInvalid


class Session(object):
    """
    Session instantiates Operation, Displayer, Reader and Writer depend on the
    user inputs, and then call main() method to serialise/deserialise and
    show data.
    The operation steps looks as below:
            1) Read/deserialise the input file.
                It supports three kinds of formats: pickle, csv and yaml.
            2) Write/serialise to the output file.
                It supports the same three formats as reading. But user can
                combine the formats, for example, reading csv format and then
                writing as yaml. If "outputFile" specified, then it would do
                serialisation operation, else it would skip this step and do
                display operation(described by step 3).
            3) Display the deserialised data as human readable format.
                There are two kinds of displaying modes, one is "text" and the
                other is "html". The "text" mode calls Terminal command "cat" to
                display in Terminal. The "html" mode calls web browser to open a
                html file.
    """
    # store the relationship between diaplayer name and Displayer.
    DISPLAYER_MAPS = {'text': displayer.TextDisplayer,
                      'html': displayer.HtmlDisplayer}
    DEFAULT_DISPLAYER_NAME = 'text'
    # store the relationship between reader name and Reader.
    READER_MAPS = {'pickle': reader.PickleReader,
                   'yaml': reader.YamlReader,
                   'csv': reader.CsvReader}
    DEFAULT_READER_NAME = 'csv'
    # store the relationship between writer name and Writer.
    WRITER_MAPS = {'pickle': writer.PickleWriter,
                   'yaml': writer.YamlWriter,
                   'csv': writer.CsvWriter}
    DEFAULT_WRITER_NAME = 'pickle'

    def __init__(self, displayerName='', readerName='',
                 writerName='', inputFile='',
                 outputFile='', readOptions='',
                 writeOptions=''):
        """
        :param str displayerName: displayer name.
        :param str readerName: reader name(deserialise format).
        :param str writerName: writer name(serialise format).
        :param str inputFile: input file(source file).
        :param str outputFile: output file(will be write).
        :param str readOptions: reading options during deserialisation.
        :param str writeOptions: writing options during serialisation.
        """
        self._displayerName = displayerName
        self._readerName = readerName
        self._writerName = writerName
        self._inputFile = inputFile
        self._outputFile = outputFile
        self._readOptions = readOptions
        self._writeOptions = writeOptions

        # Validate arguments.
        self._validateArgs()

        # Load read options or write options depend on input arguments.
        self._confArgs()

        # Initialize Operation, Displayer, Reader and Writer.
        self._initInstances()

    def _initInstances(self):
        """
        Initialize Operation, Displayer, Reader and Writer.
        """
        readerObj = Session.READER_MAPS.get(self._readerName)(
            readOptions=self._readKwargs)

        if self._writerName:
            writerObj = Session.WRITER_MAPS.get(self._writerName)(
                writeOptions=self._writeKwargs)

        self._displayer = Session.DISPLAYER_MAPS.get(self._displayerName)()

        if self._outputFile:
            # If specified output file, serialise input file to output file.
            self._operation = operation.Operation(
                reader=readerObj,
                writer=writerObj,
                inputFile=self._inputFile,
                outputFile=self._outputFile)

        else:
            # Not specified output file, deserialise input file and display
            # the result.
            self._operation = operation.Operation(
                reader=readerObj,
                inputFile=self._inputFile
            )

    def _validateArgs(self):
        """
        Validate input arguments.
        """
        if not path.isfile(self._inputFile):
            raise SessionArgsInvalid('Specified input file path {0} is not a '
                                     'regular file.'.format(self._inputFile))
        if self._readerName not in Session.READER_MAPS:
            raise SessionArgsInvalid(
                'Specified reader(deserialise) format name '
                '{0} is not correct. It should be one of "{'
                '1}".'.format(self._readerName,
                              ', '.join(Session.READER_MAPS)))
        if self._writerName:
            if self._writerName not in Session.WRITER_MAPS:
                raise SessionArgsInvalid(
                    'Specified writer(serialise) format name {0} is not '
                    'correct. It should be one of "{1}"'.format(
                        self._writerName,
                        ', '.join(Session.WRITER_MAPS)))
        if self._outputFile:
            if not path.isdir(path.dirname(self._outputFile)):
                raise SessionArgsInvalid(
                    'Specified parent directory of input file {0} is not a '
                    'directory.'.format(
                        self._outputFile))
        if self._displayerName not in Session.DISPLAYER_MAPS:
            raise SessionArgsInvalid(
                'Specified displayer name {0} is not correct. It should be '
                'one of "{1}"'.format(
                    self._displayerName,
                    ', '.join(Session.DISPLAYER_MAPS)))
        for option, optionName in (
                (self._readOptions, 'read'), (self._writeOptions, 'write')):
            if option and option.find('=') == -1:
                raise SessionArgsInvalid(
                    'Can not find "=" in the specified {0} options "{'
                    '1}". The correct format should be "key=value,key=value,'
                    '...".'.format(
                        optionName,
                        option))

    def _confArgs(self):
        """
        Load read options or write options depend on input arguments.
        """

        def confStrOptions(option):
            """
            Get read options or write options depend on input string.
            :param str option: input string options, it should be split by ",
            " if there are more than one.
            :return: `dict`
            """
            kwargs = {}
            if option:
                for opt in option.split(','):
                    key, value = opt.split('=')
                    kwargs[key] = value
            return kwargs

        self._readKwargs = confStrOptions(self._readOptions)
        self._writeKwargs = confStrOptions(self._writeOptions)

    def main(self):
        """
        Serialise/deserialise input file and display the result.
        :return: Return True if show has been executed successfully, else False.
        :rtype: bool
        """
        status, records = self._operation.run()
        return self._displayer.show(records)
