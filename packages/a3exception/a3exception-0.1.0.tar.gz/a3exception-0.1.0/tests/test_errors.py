# -*- coding: utf-8 -*-
import unittest

from a3exception import errors


class T(unittest.TestCase):

    def test__error(self):
        message = 'message'
        cause = 'cause'
        error = errors.Error(message=message, cause=cause)

        self.assertEqual(str(error), message)
        self.assertEqual(repr(error), cause)

    def test__client_errors(self):
        text = 'text'
        self.assertEqual(errors.ClientKnownError(message=text).message, text)
        self.assertEqual(errors.ValidationError(message=text).message, text)
        self.assertEqual(errors.NotFoundError(message=text).message, text)
        self.assertEqual(errors.InvalidTokenError(message=text).message, text)
        self.assertEqual(errors.ForbiddenError(message=text).message, text)
        self.assertEqual(errors.NotAvailableError(message=text).message, text)

    def test__server_errors(self):
        text = 'text'
        self.assertEqual(errors.ServerKnownError(cause=text).cause, text)
        self.assertEqual(errors.ServerUnknownError(cause=text).cause, text)

