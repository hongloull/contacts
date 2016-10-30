class Records(object):
    """
    Class to describe internal data. Use it as exchange data between
    Displayer, Reader, Writer and Session.
    """

    def __init__(self, obj=None):
        """
        :param obj: Python's serialise able object and it is iterable.
        """
        self._obj = obj
        self._headers = self._obj[0].keys()
        self._rows = None
        self._flattenRows = None

    @property
    def obj(self):
        return self._obj

    @property
    def headers(self):
        """
        :return: get headers as: ["name", "address", "phone"]
        :rtype: `list(str)`
        """
        return self._headers

    @property
    def rows(self):
        """
        :return: get rows as: [["Daniel", "Room 101", "123456"],["Tom",
        "Room 102",
        "234567"]]
        :rtype: `list(list)`
        """
        if self._rows is None:
            lines = []
            for item in self._obj:
                row = []
                for header in self.headers:
                    row.append(item.get(header))
                lines.append(row)
            return lines

    @property
    def flattenRows(self):
        """
        :return: get rows as: ['123456\tHank\tRoom 101', '\tKarl\tRoom 102',]
        :rtype: `list(str)`
        """
        if self._flattenRows is None:
            lines = []
            for row in self.rows:
                lines.append('\t'.join(row))
            return lines

    def __repr__(self):
        return '{headers}\n{rows}'.format(headers='\t'.join(self.headers),
                                          rows='\n'.join(self.flattenRows))

    def __eq__(self, other):
        return self.obj == other.obj
