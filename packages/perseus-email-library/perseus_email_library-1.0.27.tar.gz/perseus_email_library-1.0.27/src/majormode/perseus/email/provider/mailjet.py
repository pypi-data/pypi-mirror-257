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
from __future__ import annotations

import base64
import os
import uuid

from mailjet_rest import Client
from majormode.perseus.model.email import Email

from majormode.perseus.email.email_service import EmailServiceBase


class MailjetService(EmailServiceBase):
    DEFAULT_MAILJET_VERSION = 'v3.1'

    ENVIRONMENT_KEY_NAME_MAILJET_API_KEY = 'MAILJET_API_KEY'
    ENVIRONMENT_KEY_NAME_MAILJET_API_SECRET = 'MAILJET_API_SECRET'

    @classmethod
    def __build_attached_file_item(
            cls,
            file_path_name: str,
            mime_type: str = None
    ) -> dict:
        """
        Return a dictionary identifying the file to be attached to the email.
        https://dev.mailjet.com/email/guides/send-api-v31/#send-with-attached-files


        @param file_path_name: The asbolute path and name of the file to be
            attached.

        @param mime_type: The media type that indicates the nature and format
            of the resource.


        @return: An dictionary composed of the following keys:

            - `ContentType` (required): The Multipurpose Internet Mail Extensions
              (MIME) type associated to the attached file.

            - `Filename` (required): The name of the file.

            - `Base64Content` (required): The content of the file encoded to Base64.
        """
        with open(file_path_name, 'rb') as fd:
            file_content = fd.read()
            file_base64_content = base64.b64encode(file_content)
            file_name = os.path.basename(file_path_name)

            if not mime_type:
                mime_type = cls._find_file_extension_mime_type(file_name)

            attached_file_item = {
                'ContentType': mime_type,
                'Filename': file_name,
                'Base64Content': file_base64_content.decode(),
            }

            return attached_file_item

    @classmethod
    def __build_attached_file_items(cls, attached_files: list[str]) -> list[dict]:
        attached_file_items = [
            cls.__build_attached_file_item(file_path_name)
            for file_path_name in  attached_files
        ]
        return attached_file_items

    def __init__(
            self,
            api_key=None,
            api_secret=None,
            api_version=None
    ):
        super().__init__()

        api_key = api_key or os.getenv(self.ENVIRONMENT_KEY_NAME_MAILJET_API_KEY)
        if api_key is None:
            raise ValueError(f"An API Key must be passed or defined in the environment variable {self.ENVIRONMENT_KEY_NAME_MAILJET_API_KEY}")

        api_secret = api_secret or os.getenv(self.ENVIRONMENT_KEY_NAME_MAILJET_API_SECRET)
        if api_secret is None:
            raise ValueError(f"An API Secret must be passed or defined in the environment variable {self.ENVIRONMENT_KEY_NAME_MAILJET_API_SECRET}")

        self.__client = Client(
            auth=(api_key, api_secret),
            version=api_version or self.DEFAULT_MAILJET_VERSION
        )

    @classmethod
    def __build_mailjet_data(cls, emails) -> dict:
        data = {
            'Messages': [
                cls.__build_message(email)
                for email in emails
            ]
        }

        return data

    @classmethod
    def __build_message(cls, email: Email) -> dict:
        message = {
            'From': {
                'Email': email.author.email_address,
                'Name': email.author.name,
            },
            'To': cls.__build_recipients(email.recipients),
            'Subject': email.subject,
            'TextPart': email.text_content,
            'HTMLPart': email.html_content,
            'CustomID': uuid.uuid4().hex,
            'Attachments': email.attached_files and cls.__build_attached_file_items(email.attached_files),
        }

        return message

    @staticmethod
    def __build_recipients(recipients: list | set | tuple) -> list:
        return [
            {
                'Email': recipient.email_address,
                'Name': recipient.name
            }
            for recipient in recipients
        ]

    def send_emails(self, emails):
        emails = self._validate_emails(emails)
        data = self.__build_mailjet_data(emails)
        result = self.__client.send.create(data=data)
        return result
