""" Wrapper to make tempfile.NamedTemporaryFile work as we need on Windows and *nix.

Desired behaviour: with delete=True, we want to be able to write to the file, and open
it again with a different file handle for reading. On Linux, closing the file deletes it
right away, while on Windows, you cannot reopen the file unless you've closed it first.
So this wrapper deletes the file on exit or object deletion instead of closing.
"""

import os
from tempfile import NamedTemporaryFile, template


class _PortableNamedTemporaryFileWrapper:
    """ Wrapper object around the real NamedTemporaryFile that forwards calls as needed

    The difference with NamedTemporaryFile is that we cleanup on exit and del, rather
    than on close.
    """

    def __init__(self, named_temporary_file):
        self.named_temporary_file = named_temporary_file
        self.name = named_temporary_file.name

    def __enter__(self):
        self.named_temporary_file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        result = self.named_temporary_file.__exit__(exc_type, exc_value, traceback)
        self.cleanup()
        return result

    def __del__(self):
        self.cleanup()

    def __getattr__(self, name):
        return self.named_temporary_file.__getattr__(name)

    def close(self):
        return self.named_temporary_file.close()

    # def __iter__(self):
    #    for line in self.named_temporary_file:
    #        yield line

    def cleanup(self):
        self.close()
        try:
            os.unlink(self.named_temporary_file.name)
        except FileNotFoundError:
            pass  # cleaning up more than once is not an error


def PortableNamedTemporaryFile(
    mode="w+b", suffix="", prefix=template, dir=None, delete=True
):
    """ Portable named temporary file that works on Windows, Linux and Mac.

    This class wraps tempfile.NamedTemporaryFile() with a portable behaviour that works
    on Windows, Linux and Mac as we need it to.

    See https://docs.python.org/3/library/tempfile.html for full documentation.
    The difference is that if you specify delete=True, the temporary file will be
    deleted when the returned object is destroyed rather than when the file is closed.
    On windows, it is not possible to reopen the file while the original handle is still
    open, so this function makes temporary files work across OS's.
    """
    if not delete:
        return NamedTemporaryFile(
            mode=mode, suffix=suffix, prefix=prefix, dir=dir, delete=delete
        )
    else:
        named_temporary_file = NamedTemporaryFile(
            mode=mode, suffix=suffix, prefix=prefix, dir=dir, delete=False
        )
        return _PortableNamedTemporaryFileWrapper(
            named_temporary_file=named_temporary_file
        )
