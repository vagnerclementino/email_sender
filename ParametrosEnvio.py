#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP as TimeStamp
from datetime import datetime

Base = declarative_base()


class ParametrosEnvio(Base):

    """Docstring for ParametroEnvio. """

    __tablename__ = 'parametros_envio'
    sequence_name = 'parametros_envio_id_parametros_envio_seq'
    id_parametros_envio = Column('id_parametros_envio',
                                 Integer,
                                 Sequence(sequence_name),
                                 primary_key=True)
    ind_bloqueio_envio = Column('ind_bloqueio_envio',
                                String(1),
                                nullable=False)
    max_num_envios = Column('max_num_envios',
                            Integer,
                            nullable=False)
    data_atualizacao = Column('data_atualizacao',
                              TimeStamp,
                              nullable=False)

    def __init__(self,
                 ind_bloqueio_envio,
                 max_num_envios,
                 data_atualizacao=datetime.now()):
        self.ind_bloqueio_envio = ind_bloqueio_envio
        self.max_num_envios = max_num_envios
        self.data_atualizacao = data_atualizacao

    def is_envio_bloqueado(self):
        """TODO: Docstring for is_envio_bloqueado.
        :returns: TODO

        """
        if self.ind_bloqueio_envio == 'S':
            return True
        else:
            return False

    def get_max_num_envios(self):
        """TODO: Docstring for get_max_num_envios.
        :returns: TODO

        """
        return self.max_num_envios
