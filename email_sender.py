#!/usr/bin/env python
# -*- coding: utf-8 -*-
import emails
import docs.conf as cfg
import argparse
# import ipdb as pdb
import os.path
from emails.template import JinjaTemplate as T
import time
import logging as log
import sys
from Database import Database
from sqlalchemy.exc import SQLAlchemyError
from ParametrosEnvio import ParametrosEnvio
from Participantes import Participantes
from RegistroEnvio import RegistroEnvio
from datetime import datetime
from GrupoParticipantes import GrupoParticipantes
from ListaNegraParticipantes import ListaNegraParticipantes
from emails.backend.smtp.exceptions import SMTPConnectNetworkError


def parse_args():
    """
    Parse script input arguments.

    Returns the parsed args, having validated that the input
    file can be read, and that there is a valid Username.
    """
    parser = get_parser()
    args = parser.parse_args()

    # pdb.set_trace()
    if os.path.isfile(args.html_filename):
        args.html = args.html_filename
        return args


def get_parser():
    """ Return the parser used to interpret the script arguments."""
    usage = (
        "Script to send an HTML file as an HTML email."
        "\nExamples:"
        "\n1. Send the contents of test_file.html to fred"
        "\n$ send_html_email.py test_file.html"
        "\n"
    )
    epilog = "NB This script requires a Gmail account."

    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=usage,
                                     epilog=epilog,
                                     formatter_class=formatter_class
                                     )
    parser.add_argument('html_filename',
                        help='The HTML file as Jinja template')

    parser.add_argument('-t', '--title',
                        help=('The test email subject line (defaults to "Test'
                              'email")'
                              ),
                        default="Improving Issue Tracking System"
                        )
    return parser


def print_args(args):
    """Print out the input arguments."""
    print ('Sending test email by file: %s' % args.html)


def get_recipients(session):
    """TODO: Docstring for get_recipients.

    """
    # Recupera a lista de participantes incluídos na lista negra
    subquery_notin = (session.query(ListaNegraParticipantes
                                    ._email_participante).all()
                      )
    # Recupera todos os participantes
    query_all = (session.query(Participantes,
                               GrupoParticipantes)
                 .filter(Participantes.id_grupo_participante ==
                         GrupoParticipantes.id_grupo_participante)
                 .filter(Participantes.ind_ativo == 'S')
                 )
    # Aplicando os filtros
    query = query_all.filter((Participantes.email_participante
                              .notin_(subquery_notin)))
    for participante in query.all():
        yield participante


def get_current_timestamp():
    """Retorna a data e hora atual
    :returns: Data e hora atual

    """
    return datetime.now()


def obtem_dias_entre_data(data_inicio, data_fim):
    """

    :data_inicio: TODO
    :data_fim: TODO
    :returns: TODO

    """
    total_dias = (data_fim - data_inicio).days
    return total_dias


def avalia_envio_participante(parametros_envio,
                              participante,
                              registro_envio,
                              session
                              ):
    """Avalia se o e-mail pode ser enviado para um participante
    dado o registro de envios anteriores e o parâmetros de envio
    definidos

    :parametros_envio: Um objeto do tipo ParametrosEnvio
    :participante:  Um objeto do tipo Participantes
    :registro_envio: Um objeto do tipo RegistroEnvio
    :returns: True se o envio pode ser realizado
    False se o envio NÃO pode ser realizado

    """
    is_envio_permitido = False
    # pdb.set_trace()
    total_envio = registro_envio.get_total_envios(participante,
                                                  session)
    max_envio_permitido = parametros_envio.max_num_envios
    if total_envio == 0:
        is_envio_permitido = True
    elif total_envio >= max_envio_permitido:
        is_envio_permitido = False
    elif total_envio == 1:
        ultima_data_envio = (registro_envio
                             .get_ultima_data_envio(participante, session))
        data_hora_atual = get_current_timestamp()
        dif_em_dias = obtem_dias_entre_data(ultima_data_envio,
                                            data_hora_atual)
        if dif_em_dias >= 2:
            is_envio_permitido = True
        else:
            is_envio_permitido = False

    elif total_envio == 2:
        ultima_data_envio = (registro_envio
                             .get_ultima_data_envio(participante, session)
                             )
        data_hora_atual = get_current_timestamp()

        dif_em_dias = obtem_dias_entre_data(ultima_data_envio,
                                            data_hora_atual)
        if dif_em_dias >= 3:
            is_envio_permitido = True
        else:
            is_envio_permitido = False
    else:
        is_envio_permitido = False
    return is_envio_permitido


def main():
    """
    TODO: Docstring for main.
    :returns: None

    """
    TOTAL_PAUSA_LONGA = 100
    SEGUNDOS_PAUSA_CURTA = 180
    SEGUNDOS_PAUSA_LONGA = 300
    MAX_ENVIO_DIA = 200
    reload(sys)
    sys.setdefaultencoding('utf-8')

    log_path = './log/'
    # Cria o diretório de log caso ele não exista
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_name = 'email_sender'
    log_format = "[%(asctime)s] [%(levelname)s] : %(message)s"
    logFormatter = log.Formatter(log_format,
                                 datefmt='%d-%m-%Y %H:%M:%S'
                                 )
    rootLogger = log.getLogger()
    rootLogger.setLevel(log.INFO)

    fileHandler = log.FileHandler(("{0}/{1}.log"
                                   .format(log_path, file_name))
                                  )
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    args = parse_args()
    total_email_enviados = 0

    try:
        # pdb.set_trace()
        db = Database(user=cfg.db_dissertacao["user"],
                      password=cfg.db_dissertacao["password"],
                      db=cfg.db_dissertacao["database"],
                      host=cfg.db_dissertacao["host"],
                      port=cfg.db_dissertacao["port"])
        session = db.get_session()
        # Obtendo os parâmetros de envios dos e-mails
        parametros = session.query(ParametrosEnvio).first()
        # Verificando se o envio está bloqueado
        if parametros.is_envio_bloqueado():
            log.warning(("O processo de envio de e-mail "
                         "está bloqueado! Uma nova tentativa "
                         "de envio será feita em breve!"))
            sys.exit(0)
        # Verificando se o envio está bloqueado
        if parametros.is_enviando_email():
            log.warning(("Já existe uma instância do processo de envio"
                         " em execução! Uma nova tentativa "
                         "de envio será feita em breve!"))
            sys.exit(0)
        # Inciando o envio
        log.info("Iniciando o processo de envio de e-mail's")
        parametros.set_inicio_proc_envio()
        try:
            session.add(parametros)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

        recipients_list = get_recipients(session)

        with open(args.html, 'rb') as html_file:
            html_content = T(unicode(html_file.read(), 'utf8'))
            email_subejct = args.title
            email_sender = ('Vagner Clementino',
                            'vagner.clementino@gmail.com')
            email_ccb = ("Vagner Clementino",
                         'vagner.clementino@gmail.com')
            for r in recipients_list:
                # pdb.set_trace()
                try:
                    real_name = (unicode(r.Participantes.nome_participante,
                                         'utf8'))
                    user_mail = (unicode(r.Participantes.email_participante,
                                         'utf8'))
                except TypeError:
                    real_name = r.Participantes.nome_participante
                    user_mail = r.Participantes.email_participante
                project_name = r.GrupoParticipantes.nome_grupo
                url_grupo = r.GrupoParticipantes.url_grupo
                url_formulario = r.GrupoParticipantes.url_formulario
                nome_grupo = r.GrupoParticipantes.nome_grupo
                retry = True
                data_hora_envio = get_current_timestamp()

                registro_envio = RegistroEnvio(user_mail,
                                               data_hora_envio,
                                               data_hora_envio)

                if avalia_envio_participante(parametros,
                                             r.Participantes,
                                             registro_envio,
                                             session):
                    while retry:
                        message = emails.html(html=html_content,
                                              subject=email_subejct,
                                              mail_from=email_sender,
                                              bcc=email_ccb
                                              )
                        smtp = {'host': cfg.smtp_dcc['host'],
                                'port': cfg.smtp_dcc['port'],
                                'tls': cfg.smtp_dcc['tls'],
                                'user': cfg.smtp_dcc['user'],
                                'password': cfg.smtp_dcc['password'],
                                'timeout': cfg.smtp_dcc['timeout']
                                }
                        # pdb.set_trace()
                        response = message.send(to=user_mail,
                                                render={'real_name':
                                                        real_name,
                                                        'url_grupo':
                                                        url_grupo,
                                                        'url_formulario':
                                                        url_formulario,
                                                        'nome_grupo':
                                                        nome_grupo},
                                                smtp=smtp
                                                )
                        if response.status_code not in [250, ]:
                            log.warning(('Resposta do servidor'
                                         'de email {0}'
                                         .format(response.status_code)
                                         ))
                            log.warning(("Não foi possível realizar o "
                                         "envio para o e-mail <{0}>. "
                                         "Uma nova tentativa será realizada")
                                        .format(user_mail)
                                        )
                            retry = True
                        else:
                            retry = False
                            try:
                                session.add(registro_envio)
                                session.commit()
                                total_email_enviados += 1
                            except SQLAlchemyError as e:
                                log.error(e)
                                session.rollback()
                            log.info(("Enviado para o participante"
                                      " {0} do Projeto {1}"
                                      " através do e-mail {2}"
                                      ).format(real_name,
                                     project_name,
                                     user_mail))
                            if total_email_enviados == MAX_ENVIO_DIA:
                                log.info(("O total de envios por dia ({0})"
                                          "foi alcançado. O processo "
                                          "de envio será encerrado.")
                                         .format(MAX_ENVIO_DIA)
                                         )
                                parametros.set_fim_proc_envio()
                                session.add(parametros)
                                session.commit()

                                # Fechando a conexão
                                db.close_connection()
                                sys.exit(1)

                            if (total_email_enviados % TOTAL_PAUSA_LONGA == 0):
                                segundos_pausa = SEGUNDOS_PAUSA_LONGA
                            else:
                                segundos_pausa = SEGUNDOS_PAUSA_CURTA
                            u_message = (("Aguardando {0} segundos"
                                          " para um novo envio")
                                         .format(segundos_pausa)
                                         )
                            log.info(u_message)
                            time.sleep(segundos_pausa)
        log.info(("Finalizado o processo de envio de e-mails's."
                  " Enviado um total de {0} e-mails")
                 .format(total_email_enviados)
                 )
        parametros.set_fim_proc_envio()
        session.add(parametros)
        session.commit()

        # Fechando a conexão
        db.close_connection()
    except SMTPConnectNetworkError as esmtp:
        log.error(esmtp)
    except IOError as ioe:
        log.error(ioe)
    except UnicodeError as ue:
        log.error(ue)
    except SQLAlchemyError as sqle:
        log.error(sqle)
        db.close_connection()
    except Exception as e:
        log.error(e)

if __name__ == "__main__":
    main()
