#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime

Base = declarative_base()


class Participantes(Base):

    """Docstring for Participantes. """
    __tablename__ = 'participantes_survey'
    sequence_name = 'participantes_survey_id_participantes_survey_seq'
    id_participantes_survey = Column('id_participantes_survey',
                                     Integer,
                                     Sequence(sequence_name),
                                     primary_key=True
                                     )
    nome_participante = Column('nome_participante',
                               String(500),
                               nullable=False)
    email_participante = Column('email_participante',
                                String(500),
                                nullable=False)
    data_atualizacao = Column('data_atualizacao',
                              TimeStamp,
                              nullable=False)
    id_grupo_participante = Column('id_grupo_participante',
                                   Integer,
                                   ForeignKey(("grupo_participante."
                                               "id_grupo_participante"
                                               )
                                              )
                                   )
    ind_ativo = Column('ind_ativo',
                       String(1),
                       nullable=False)

    def __init__(self,
                 nome_participante,
                 email_participante,
                 projeto_participante,
                 url_formulario,
                 ind_ativo,
                 data_atualizacao=datetime.now()
                 ):
        """TODO: to be defined1. """
        self.nome_participante = nome_participante
        self.email_participante = email_participante
        self.projeto_participante = projeto_participante
        self.url_formulario = url_formulario
        self.data_atualizacao = data_atualizacao
        self.ind_ativo = ind_ativo

    def __repr__(self):
        rep = str()
        rep = rep + '<nome: {}'.format(self.nome_participante)
        rep = rep + ', email: {}'.format(self.email_participante)
        rep = rep + ', projeto: {}'.format(self.projeto_participante)
        rep = rep + ', url: {}'.format(self.url_formulario)
        rep = rep + ', Ativo: {}'.format(self.ind_ativo)
        rep = rep + '>'
        return rep
