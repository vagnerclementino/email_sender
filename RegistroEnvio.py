#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime
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
        str_data_envio = self._data_envio_email.strftime('%d/%M/%Y%H:%M:%s')
        rep = rep + ', e-mail: {}'.format(self._email_participante)
        rep = rep + ', data envio:: {}'.format(str_data_envio)
        rep = rep + ', URL: {}'.format(self._url_formulario)
        rep = rep + '>'
        return rep

    def get_total_envios(self, participante, session):
        """
           Recupera o total de e-mail enviando para determinado
           participante

        :participante: Um objetivo do tipo participante do qual se quer
                       verificar o total de envios
        :session: Um objeto de sessão para realizar a consulta
        :returns: O total de envios para determinado participante

        """
        total_envios = session.Query(self).select()
        return total_envios

    def get_ultima_data_envio(self, participante, session):
        """
           Recupera a ultima data de envio de envio
           registrada para determinado participante

        :participante: Um objetivo do tipo participante do qual se quer
                       verificar a última data de envio
        :session: Um objeto de sessão para realizar a consulta
        :returns: O último registro de envio. Caso não tenha sido
                  enviado será retornado None

        """
        ultimo_envio = session.Queary(self).select()
        return ultimo_envio
