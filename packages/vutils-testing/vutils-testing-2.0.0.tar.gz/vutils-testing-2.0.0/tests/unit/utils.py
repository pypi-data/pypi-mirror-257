#
# File:    ./tests/unit/utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-22 23:46:47 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""
Unit tests utilities.

:const FOO_CONSTANT: The auxiliary constant used in tests
"""

import io
import sys

from vutils.testing.mock import PatcherFactory

FOO_CONSTANT = 42


class FooError(Exception):
    """
    Dummy exception.

    :ivar detail: The error detail
    """

    __slots__ = ("detail",)

    def __init__(self, detail):
        """
        Initialize the exception object.

        :param detail: The error detail
        """
        Exception.__init__(self, detail)
        self.detail = detail


class StderrPatcher(PatcherFactory):
    """
    :mod:`sys.stderr` patcher.

    :ivar stream: The new error stream
    """

    __slots__ = ("stream",)

    def setup(self):
        """Set up the patcher."""
        self.stream = io.StringIO()
        self.add_spec("sys.stderr", new=self.stream)


class StderrWriter:
    """
    Dummy standard error output writer.

    :ivar stream: The error stream to write
    :ivar code: The error code
    :ivar label: The label of an error message
    """

    __slots__ = ("stream", "code", "label")

    def __init__(self, code, label=""):
        """
        Initialize the writer.

        :param code: The code
        :param label: The label
        """
        self.stream = sys.stderr
        self.code = code
        self.label = label

    @staticmethod
    def format(code, label, text):
        """
        Format the message.

        :param code: The code
        :param label: The label
        :param text: The text
        :return: the formatted message
        """
        return f"({code})[{label}] {text}\n"

    def write(self, text):
        """
        Write :arg:`text` to stream.

        :param text: The text
        """
        self.stream.write(self.format(self.code, self.label, text))


def func_a(mock):
    """
    Modify :arg:`mock`.

    :param mock: The mock object
    """
    mock.foo = FOO_CONSTANT


def func_b(mock):
    """
    Modify :arg:`mock` and raise :exc:`.FooError`.

    :param mock: The mock object
    :raises .FooError: when called
    """
    func_a(mock)
    raise FooError(FOO_CONSTANT)
