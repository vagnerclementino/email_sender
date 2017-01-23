#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.orm import sessionmaker


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
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        try:
            # The return value of create_engine() is our connection object
            self.engine = sqlalchemy.create_engine(url,
                                                   client_encoding='utf8',
                                                   connect_args={
                                                       'connect_timeout': 60
                                                       }
                                                   )
            # recuperando a conexão
            self.connection = self.engine.connect()
            self.connection.execute("SET search_path TO email_sender")

            # We then bind the connection to MetaData()
            self.metadata = sqlalchemy.MetaData(bind=self.engine,
                                                reflect=True)
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

    def get_connection(self):
        """Retorna uma conexão com o banco
        :returns: Um objeto de conexão ou lança uma exeção no caso de erro

        """
        if self.connection is not None:
            return self.connection
        else:
            msg = "Nenhum conexão válida foi encontrada!"
            raise sqlalchemy.exc.SQLAlchemyError(msg)

    def get_metadata(self):
        """Retorna o objeto de metados do banco de daos
        :returns: TODO

        """
        if self.metadata is not None:
            return self.metadata
        else:
            msg = (("Não foi possível recuperar o"
                   " metadados do banco de dados."
                    )
                   )
            raise sqlalchemy.exc.SQLAlchemyError(msg)

    def close_connection(self):
        """Fechar a conexão com o banco de dados
        :returns: TODO

        """
        try:
            self.connection.connect().close()
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise e

    def get_engine(self):
        """TODO: Retorna uma engine.
        :returns: TODO

        """
        if self.engine is not None:
            return self.engine
        else:
            msg = "Nenhuma engine válida foi encontrada"
            raise sqlalchemy.exc.SQLAlchemyError(msg)

    def get_session(self):
        """Retornar um objeto de sessão para o eu chamado
        :returns: TODO
        """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session
