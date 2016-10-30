import fnmatch
import os
import os.path
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print >> sys.stderr, "install failed - requires setuptools"
    sys.exit(1)

if sys.version_info < (2, 7):
    print >> sys.stderr, "install failed - requires python v2.7 or greater"
    sys.exit(1)


def find_files(pattern, path=None, root="contacts"):
    paths = []
    basepath = os.path.realpath(os.path.join("src", root))
    path_ = basepath
    if path:
        path_ = os.path.join(path_, path)

    for root, _, files in os.walk(path_):
        files = [x for x in files if fnmatch.fnmatch(x, pattern)]
        files = [os.path.join(root, x) for x in files]
        paths += [x[len(basepath):].lstrip(os.path.sep) for x in files]

    return paths


scripts = [
    "contacts",
]

setup(
    name="contacts",
    version=0.1,
    description=("Technical test task."),
    long_description=None,
    author="Jerry Ma",
    author_email="hongloull@outlook.com",
    license="LGPL",
    scripts=[os.path.join('bin', x) for x in scripts],
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=["bin", "build", "dist"]),
    package_data={
        'contacts':
            ['../README.md'] +
            find_files('*.*', '../data') +
            find_files('*.*', '../templates'),
    },
)
