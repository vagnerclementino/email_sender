#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime
Base = declarative_base()


class RegistroEnvio(Base):

    """Docstring for RegistroEnvio. """
    __tablename__ = 'registro_envio'
    sequence_name = 'registro_envio_id_registro_envio_seq'
    id_registro_envio = Column('id_registro_envio',
                               Integer,
                               Sequence(sequence_name),
                               primary_key=True
                               )
    email_participante = Column('email_participante',
                                String(500),
                                nullable=False)
    data_envio_email = Column('data_envio_email',
                              TimeStamp,
                              nullable=False)

    data_atualizacao = Column('data_atualizacao',
                              TimeStamp,
                              nullable=False)

    def __init__(self,
                 email_participante,
                 data_envio_email=datetime.now(),
                 data_atualizacao=datetime.now()
                 ):
        """TODO: to be defined1. """
        self.email_participante = email_participante
        self.data_envio_email = data_envio_email
        self.data_atualizacao = data_atualizacao

    def __repr__(self):
        rep = str()
        str_data_envio = self.data_envio_email.strftime('%d/%M/%Y%H:%M:%s')
        rep = rep + ', e-mail: {}'.format(self.email_participante)
        rep = rep + ', data envio:: {}'.format(str_data_envio)
        rep = rep + ', URL: {}'.format(self.url_formulario)
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
        total_envios = (session.query(func.count(self.email_participante))
                        .filter(RegistroEnvio.email_participante ==
                                participante.email_participante)
                        .scalar()
                        )
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
        ultimo_envio = (session.query(func.max(self.data_envio_email))
                        .filter(RegistroEnvio.email_participante ==
                                participante.email_participante)
                        .scalar()
                        )
        return ultimo_envio
