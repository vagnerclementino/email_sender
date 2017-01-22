#!/usr/bin/env python
# -*- coding: utf-8 -*-


import boto3

class SESClient(object):

    """Docstring for SESClient. """

    def __init__(self,
                 aws_access_key_id,
                 aws_secret_access_key):
        """TODO: to be defined1. """
        __aws_access_key_id = aws_access_key_id
        __aws_secret_access_key = aws_secret_access_key

        #Conetando com o SES
        __clientSES = boto3.client('ses',
                                   aws_access_key_id=self.__aws_access_key_id
                                   aws_secret_access_key=self.__aws_secret_access_key
                                   )
  def send_email(self, source, destination, message):
      """TODO: Docstring for send_email.

      :source: TODO
      :destination: TODO
      :message: TODO
      :returns: TODO

      """
      response = self.__clienSES.send_mail(Source = source,
                                           Destination = destination,
                                           Message = message
                                           )
      return response



