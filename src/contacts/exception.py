class ContactsException(Exception):
    """
    Base exception.
    """
    _PREFIX = ''

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return '{0}\n{1}'.format(self._PREFIX, self._value)


class SessionArgsInvalid(ContactsException):
    """
    Exception for Session's input parameters are not correct.
    """

    _PREFIX = 'Session\'s input parameters are not correct.'


class DisplayerShowException(ContactsException):
    """
    Exception for Displayer.
    """
    _PREFIX = 'Displayer got exception to show file.'


class DeSerialisationOperationException(ContactsException):
    """
    Exception for Operation.
    """
    _PREFIX = 'Error during deserialisation(reading from input file).'


class SerialisationOperationException(ContactsException):
    """
    Exception for Operation.
    """
    _PREFIX = 'Error during serialisation(writing to output file).'