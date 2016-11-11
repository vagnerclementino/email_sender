#!/usr/bin/env python
# -*- coding: utf-8 -*-
import emails
import docs.conf as cfg
import datetime


def main():
    """TODO: Docstring for main.
    :returns: None

    """
    try:
        retry = True
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html_content = '<p><b>EU TE AMO! Mesmo as #h!</b></p>'
        html_content = html_content.replace('#h', now, 1)
        email_subejct = 'Amor da minha vida'
        email_sender = ('Vagner Clementino',
                        'vagnercs@dcc.ufmg.br')
        email_receiver = ('Vagner Clementino',
                          'vagnerclementino@pbh.gov.br')
        email_cc = ("Andreza Vieira",
                    'a.vieiralelis@gmail.com')
        while retry:
            message = emails.html(html=html_content,
                                  subject=email_subejct,
                                  mail_from=email_sender,
                                  cc=email_cc
                                  )
            response = message.send(to=email_receiver,
                                    smtp={'host': cfg.smtp_dcc['host'],
                                          'port': cfg.smtp_dcc['port'],
                                          'tls': cfg.smtp_dcc['tls'],
                                          'user': cfg.smtp_dcc['user'],
                                          'password': cfg.smtp_dcc['password']
                                          }
                                    )
            if response.status_code not in [250, ]:
                retry = True
            else:
                retry = False
                message_text = message.as_string()
                print("Enviado o e-mail:\n {0}".format(message_text))
    except emails.backend.smtp.exceptions.SMTPConnectNetworkError as e:
        print(e)

if __name__ == "__main__":
    main()
