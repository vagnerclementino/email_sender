#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime
from time import strftime
Base = declarative_base()


class RegistroEnvio(Base):

    """Docstring for RegistroEnvio. """
    __tablename__ = 'registro_envio'
    _sequence_name = 'registro_envio_id_registro_envio_seq'
    _id_registro_envio = Column('id_registro_envio',
                                      Integer,
                                      Sequence(_sequence_name),
                                      primary_key=True
                                      )
    _email_participante = Column('email_participante',
                                 String(500),
                                 nullable=False)
    _data_envio_email = Column('data_envio_email',
                               TimeStamp,
                               nullable=False)

    _data_atualizacao = Column('data_atualizacao',
                               TimeStamp,
                               nullable=False)

    def __init__(self,
                 email_participante,
                 data_envio_email=datetime.now(),
                 data_atualizacao=datetime.now()
                 ):
            """TODO: to be defined1. """
            self._email_participante = email_participante
            self._data_envio_email = data_envio_email
            self._data_atualizacao = data_atualizacao

    def __repr__(self):
        rep = str()
        str_data_envio = str(self._data_envio_email).strftime('%d/%M/%Y%H:%M:%s')
        rep = rep + ', email: {}'.format(self._email_participante)
        rep = rep + ', data envio:: {}'.format(str_data_envio)
        rep = rep + ', url: {}'.format(self._url_formulario)
        rep = rep + '>'
        return rep
