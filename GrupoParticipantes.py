#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime

Base = declarative_base()


class GrupoParticipantes(Base):

    """Docstring for Participantes. """
    __tablename__ = 'grupo_participante'
    sequence_name = 'grupo_participante_id_grupo_participante_seq'
    id_grupo_participante = Column('id_grupo_participante',
                                   Integer,
                                   Sequence(sequence_name),
                                   primary_key=True
                                   )
    nome_grupo = Column('nome_grupo',
                        String(500),
                        nullable=False)
    url_grupo = Column('url_grupo',
                       String(500),
                       nullable=False)
    url_formulario = Column('url_formulario',
                            String(100),
                            nullable=False)
    data_atualizacao = Column('data_atualizacao',
                              TimeStamp,
                              nullable=False)

    def __init__(self,
                 nome_grupo,
                 url_grupo,
                 url_formulario,
                 data_atualizacao=datetime.now()):
        """TODO: to be defined1. """
        self.nome_grupo = nome_grupo
        self.url_grupo = url_grupo
        self.url_formulario = url_formulario
        self.data_atualizacao = data_atualizacao

    def repr__(self):
        rep = str()
        rep = rep + '<nome: {}'.format(self._nome_grupo)
        rep = rep + ', URL Grupo: {}'.format(self._nome_grupo)
        rep = rep + ', URL Formulário: {}'.format(self._url_formulario)
        rep = rep + '>'
        return rep
