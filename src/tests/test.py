import os.path
import inspect
import unittest


def main(pattern='test*.py'):
    rootTestDir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    srcDir = os.path.join(rootTestDir, '..')
    srcTestDir = os.path.join(srcDir, 'contacts', 'tests')

    testSuite = unittest.defaultTestLoader.discover(srcTestDir,
                                                    pattern=pattern)

    unittest.TextTestRunner(verbosity=1).run(testSuite)
    unittest.main()

if __name__ == '__main__':
    main()
