#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlalchemy
import sys
from sqlalchemy.orm import sessionmaker
reload(sys)
sys.setdefaultencoding('utf8')


class Database(object):

    """Gerencia as conexões com o banco de dados"""

    def __init__(self, user, password, db, host='localhost', port=5432):
        """TODO: to be defined1.

        :user: Usuário de conexeção ao banco de dados
        :password: Password do usuário do banco de dados
        :db: Nome do banco de dados para conexão
        :host: Nome do host onde  o banco está conectado
        :port: Número da porta para conexão

        """
        self._user = user
        self._password = password
        self._db = db
        self._host = host
        self._port = port
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        try:
            # The return value of create_engine() is our connection object
            self._engine = sqlalchemy.create_engine(url,
                                                    client_encoding='utf8')
            # recuperando a conexão
            self._connection = self._engine.connect()

            # We then bind the connection to MetaData()
            self._metadata = sqlalchemy.MetaData(bind=self._engine,
                                                 reflect=True)
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

    def get_connection(self):
        """Retorna uma conexão com o banco
        :returns: Um objeto de conexão ou lança uma exeção no caso de erro

        """
        if self._connection is not None:
            return self._connection
        else:
            msg = "Nenhum conexão válida foi encontrada!"
            raise sqlalchemy.exc.SQLAlchemyError(msg)

    def get_metadata(self):
        """Retorna o objeto de metados do banco de daos
        :returns: TODO

        """
        if self._metadata is not None:
            return self._metadata
        else:
            msg = (("Não foi possível recuperar o")
                   (" metadados do banco de dados.")
                   )
            raise sqlalchemy.exc.SQLAlchemyError(msg)

    def close_connection(self):
        """Fechar a conexão com o banco de dados
        :returns: TODO

        """
        try:
            self._connection.connect().close()
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

    def get_engine(self):
        """TODO: Retorna uma engine.
        :returns: TODO

        """
        if self._engine is not None:
            return self._engine
        else:
            msg = "Nenhuma engine válida foi encontrada"
            raise sqlalchemy.exc.SQLAlchemyError(msg)

    def get_session(self):
        """Retornar um objeto de sessão para o eu chamado
        :returns: TODO
        """
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        return self._session
