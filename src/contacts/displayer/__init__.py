from os import path
from abc import ABCMeta, abstractmethod
from tempfile import NamedTemporaryFile

from contacts.io import log
from contacts.exception import  DisplayerShowException


class Displayer(object):
    __metaclass__ = ABCMeta
    _DISPLAY_FILE_SUFFIX = '.txt'

    def __init__(self):
        self._displayFile = self._getDisplayFile()

    def show(self, records):
        """
        Call system command to display file. The steps looks as below:
            1) get file content depend on import records object.
            2) write a temp file which store the step 1's content.
            3) call application to display the saved temp file.
        :param `contacts.records.Records` records: the records(contacts) will
        be display.
        """
        self._writeDisplayFile(content=self._getContent(records))

    @abstractmethod
    def _getContent(self, records):
        raise NotImplementedError

    def _writeDisplayFile(self, content=''):
        with open(self._displayFile, 'w') as f:
            f.write(content)

    def _getDisplayFile(self):
        """
        Create named temp display file.
        :return: temp file name
        :rtype: str
        """
        with NamedTemporaryFile('w+t', suffix=self._DISPLAY_FILE_SUFFIX,
                                delete=True) as f:
            return f.name


class TextDisplayer(Displayer):
    """
    Text displayer class, used to display text file.
    """
    _DISPLAY_FILE_SUFFIX = '.txt'

    def _getContent(self, records):
        """
        Generate html template.
        :param `contacts.records.Records` records: the records(contacts) will
        be display.
        :return: file content.
        :rtype: str
        """
        return str(records)

    def show(self, records):
        """
        Just support linux system, call "cat" to display text file.
        :param `contacts.records.Records` records: the records(contacts) will
        be display.
        :return: return True if show successfully.
        :rtype: bool
        """
        super(TextDisplayer, self).show(records)
        import subprocess
        try:
            returnCode = subprocess.check_call('cat {0}'.format(self._displayFile),
                                         shell=True)
        except subprocess.CalledProcessError as e:
            raise DisplayerShowException(e)
        else:
            if returnCode == 0:
                log.write('Cat opened "{0}" successfully.'.format(
                    self._displayFile))
                return True
            else:
                log.write('Cat was failed to open "{0}".'.format(
                    self._displayFile))
                return False


class HtmlDisplayer(Displayer):
    """
    Html displayer class, used to display html page.
    """
    _DISPLAY_FILE_SUFFIX = '.html'
    _TEMPLATE_DIR = 'templates'
    _BODY_TEMPLATE_FILE = 'body.html'
    _ROW_TEMPLATE_FILE = 'row.html'
    _ITEM_TEMPLATE_FILE = 'item.html'

    def _getContent(self, records):
        """
        Generate html template.
        :param `contacts.records.Records` records: the records(contacts) will
        be display.
        :return: file content.
        :rtype: str
        """
        templateDir = path.join(path.dirname(path.dirname(path.dirname(
            __file__))),
            HtmlDisplayer._TEMPLATE_DIR)

        def getStream(template):
            """
            Get file content of html template.
            :param template: str
            :return: html template's content.
            :rtype: str
            """
            with open(path.join(templateDir,
                                template), 'r') as f:
                return f.read()

        bodyStream = getStream(HtmlDisplayer._BODY_TEMPLATE_FILE)
        rowStream = getStream(HtmlDisplayer._ROW_TEMPLATE_FILE)
        itemStream = getStream(HtmlDisplayer._ITEM_TEMPLATE_FILE)

        headerStreams = []
        for field in records.headers:
            headerStreams.append(itemStream.format(item=field))

        rowStreams = []
        for row in records.rows:
            columnItems = []
            for item in row:
                # get column item
                columnItem = itemStream.format(item=item)
                columnItems.append(columnItem)
            # get row item
            rowItem = rowStream.format(row=' '.join(columnItems))
            rowStreams.append(rowItem)

        return bodyStream.format(headers=' '.join(headerStreams),
                                 contacts=' '.join(rowStreams))

    def show(self, records):
        """
        Call web browser to open html file.
        :param `contacts.records.Records` records: the records(contacts) will
        be display.
        :return: return True if show successfully.
        :rtype: bool
        """
        super(HtmlDisplayer, self).show(records)
        import webbrowser
        try:
            status = webbrowser.open_new_tab(self._displayFile)
        except Exception as e:
            raise DisplayerShowException(e)
        else:
            if status:
                log.write('Web browser opened "{0}" successfully.'.format(
                    self._displayFile))
                return True
            else:
                log.write('Web browser was failed to open "{0}".'.format(
                    self._displayFile))
                return False
