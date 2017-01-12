#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime

Base = declarative_base()


class Participantes(Base):

    """Docstring for Participantes. """
    __tablename__ = 'participantes_survey'
    _sequence_name = 'participantes_survey_id_participantes_survey_seq'
    _id_participantes_survey = Column('id_participantes_survey',
                                      Integer,
                                      Sequence(_sequence_name),
                                      primary_key=True
                                      )
    _nome_participante = Column('nome_participante',
                                String(500),
                                nullable=False)
    _email_participante = Column('email_participante',
                                 String(500),
                                 nullable=False)
    _projeto_participante = Column('projeto_participante',
                                   String(100),
                                   nullable=False)
    _url_formulario = Column('url_formulario',
                             String(100),
                             nullable=False)
    _data_atualizacao = Column('data_atualizacao',
                               TimeStamp,
                               nullable=False)

    def __init__(self,
                 nome_participante,
                 email_participante,
                 projeto_participante,
                 url_formulario,
                 data_atualizacao=datetime.now()):
            """TODO: to be defined1. """
            self._nome_participante = nome_participante
            self._email_participante = email_participante
            self._projeto_participante = projeto_participante
            self._url_formulario = url_formulario
            self._data_atualizacao = data_atualizacao

    def __repr__(self):
        rep = str()
        rep = rep + '<nome: {}'.format(self._nome_participante)
        rep = rep + ', email: {}'.format(self._email_participante)
        rep = rep + ', projeto: {}'.format(self._projeto_participante)
        rep = rep + ', url: {}'.format(self._url_formulario)
        rep = rep + '>'
        return rep
