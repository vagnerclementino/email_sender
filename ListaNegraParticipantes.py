#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Sequence, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from sqlalchemy.dialects.postgresql import TEXT as Text
from datetime import datetime

Base = declarative_base()


class ListaNegraParticipantes(Base):

    """Docstring for Participantes. """
    __tablename__ = 'lista_negra_participantes'
    sequence_name = ('lista_negra_participantes_'
                     'id_lista_negra_participantes_seq')
    id_lista_negra_participantes = Column('id_lista_negra_participantes',
                                          Integer,
                                          Sequence(sequence_name),
                                          primary_key=True
                                          )
    _email_participante = Column('email_participante',
                                 String(500),
                                 nullable=False)
    motivo_inclusao = Column('motivo_inclusao',
                             Text,
                             nullable=False)
    data_inclusao = Column('data_inclusao',
                           TimeStamp,
                           nullable=False)
    data_atualizacao = Column('data_atualizacao',
                              TimeStamp,
                              nullable=False)

    def __init__(self,
                 email_participante,
                 motivo_inclusao,
                 data_inclusao=datetime.now(),
                 data_atualizacao=datetime.now()):
        """TODO: to be defined1. """
        self.email_participante = email_participante,
        self.motivo_inclusao = motivo_inclusao
        self.data_inclusao = data_inclusao
        self.data_atualizacao = data_atualizacao

    def __repr__(self):
        rep = str()
        rep = rep + ', e-mail: {}'.format(self.email_participante)
        rep = rep + ', Motivo: {}'.format(self.motivo_inclusao)
        rep = rep + ', Inclusão: {}'.format(self.data_inclusao)
        rep = rep + '>'
        return rep

    def get_email_participante(self):
        """
        :returns: TODO

        """
        return self.email_participante
