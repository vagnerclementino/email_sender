#!/usr/bin/env python
# -*- coding: utf-8 -*-
import emails
import docs.conf as cfg
import argparse
# import ipdb as pdb
import csv
import os.path
from emails.template import JinjaTemplate as T
import time
import logging as log
import sys
from database import Database
from sqlitalchemy.exc import SQLAlchemyError
reload(sys)
sys.setdefaultencoding('utf8')


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
    return parser


def print_args(args):
    """Print out the input arguments."""
    print ('Sending test email by file: %s' % args.html)


def get_recipients(csv_file_path, limit=-1):
    """TODO: Docstring for get_recipients.

    :csv_file: TODO
    :limit: TODO
    :returns: TODO

    """
    # pdb.set_trace()
    with open(csv_file_path, 'rb') as csv_file:
        counter = 0
        pythonbt_reader = csv.reader(csv_file,
                                     delimiter=','
                                     )
        next(pythonbt_reader)
        for row in pythonbt_reader:
            if counter == limit:
                return
            else:
                counter = counter + 1
                yield row


def main():
    """
        TODO: Docstring for main.
        :returns: None

    """
    SECONDS_NEW_SEND = 60
    log_path = './log/'
    file_name = 'email_sender'
    log_format = "[%(asctime)s] [%(levelname)s] : %(message)s"
    logFormatter = log.Formatter(log_format,
                                 datefmt='%d-%m-%Y %H:%m:%S'
                                 )
    rootLogger = log.getLogger()
    rootLogger.setLevel(log.INFO)

    fileHandler = log.FileHandler("{0}/{1}.log".format(log_path, file_name))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    args = parse_args()
    total_email_enviados = 0

    try:
        db = Database(user=cfg.db_dissertacao["user"],
                      password=cfg.db_dissertacao["password"],
                      db=cfg.db_dissertacao["database"],
                      host=cfg.db_dissertacao["host"],
                      port=cfg.db_dissertacao["port"])
        conn = db.get_connection()
        meta = db.get_metadata()
        log.info("Iniciando o processo de envio de email's")
        '''
        retry = True
        recipients_list = get_recipients(csv_file_path=args.recipients,
                                         limit=LIMIT_SENDER)
        with open(args.html, 'rb') as html_file:
            html_content = T(html_file.read())
            email_subejct = 'Survey about Issue Tracking System'
            email_sender = ('Vagner Clementino',
                            'vagnercs@dcc.ufmg.br')
            for r in recipients_list:
                real_name = unicode(r[0]).encode('utf8')
                user_mail = r[1]
                project_name = r[2]
                email_ccb = ("Vagner Clementino",
                             'vagner.clementino@gmail.com')
                retry = True
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
                            'password': cfg.smtp_dcc['password']
                            }

                    response = message.send(to=user_mail,
                                            render={'real_name': real_name},
                                            smtp=smtp
                                            )
                    if response.status_code not in [250, ]:
                        retry = True
                    else:
                        retry = False
                        log.info(("Enviado para o participante"
                                  " {0} do Projeto {1}"
                                  " através do e-mail {2}"
                                  ).format(real_name,
                                           project_name,
                                           user_mail))
                    u_message = ("Aguardando {0} segundos para um "
                                 "novo envio").format(SECONDS_NEW_SEND)
                    log.info(u_message)
                    total_email_enviados = total_email_enviados + 1
                    time.sleep(60)'''
    except emails.backend.smtp.exceptions.SMTPConnectNetworkError as esmtp:
        log.error(esmtp)
        return
    except IOError as ioe:
        log.error(ioe)
        return
    except UnicodeError as ue:
        log.error(ue)
        return
    except SQLAlchemyError as sqle:
        log.error(sqle)
        db.close_connetion()
        return
    except Exception as e:
        log.error(e)
        return
    log.info(("Finalizado o processo de envio de email's."
              " Enviado um total de {0} emails").format(total_email_enviados))
if __name__ == "__main__":
    main()
