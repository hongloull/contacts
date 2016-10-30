#!/usr/bin/env python

from contacts import displayer
from contacts.tests import contactstest


class DisplayerTest(contactstest.ContactsTest):
    def setUp(self):
        self._textDisplayer = displayer.TextDisplayer()
        self._htmlDisplayer = displayer.HtmlDisplayer()

    def testShow(self):
        for displayerObj in [self._textDisplayer, self._htmlDisplayer]:
            displayerObj.show(self.records)
            # TODO:


if __name__ == '__main__':
    DisplayerTest.main()
