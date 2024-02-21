# Copyright (C) 2021 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc
import pathlib


from majormode.perseus.model.email import Email
from majormode.perseus.constant.email import FILE_EXTENSION_MIME_TYPE_MAP


class EmailServiceBase(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @staticmethod
    def _find_file_extension_mime_type(
            file_name: str,
            strict: bool = False) -> str or None:
        """
        Return the Multipurpose Internet Mail Extensions (MIME) type of a file
        extension.

        A media type indicates the nature and format of a document, file, or
        assortment of bytes. MIME types are defined and standardized in IETF's
        RFC 6838.


        @param file_name: A file name.

        @param strict: Indicate whether the function must throw an exception
            if the MIME type of the file's extension has not been found.


        @return: The MIME type of the file or `None` if not found.
        """
        file_extension = pathlib.Path(file_name).suffix
        mime_type = FILE_EXTENSION_MIME_TYPE_MAP.get(file_extension)

        if not file_extension and strict:
            raise ValueError(f"The MIME type of the file extension '{file_extension}' has not been found")

        return mime_type

    @staticmethod
    def _validate_emails(emails):
        if isinstance(emails, (list, set, tuple)):
            if any([not isinstance(email, Email) for email in emails]):
                raise ValueError("Items of argument 'emails' MUST be instances of 'Email'")
        else:
            if not isinstance(emails, Email):
                raise ValueError("Argument 'emails' MUST be an instance of 'Email'")
            emails = [emails]

        return emails

    @abc.abstractmethod
    def send_emails(self, emails):
        raise NotImplementedError()
