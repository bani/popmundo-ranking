# -*- coding: utf-8 -*-

import cgi
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Mail(webapp.RequestHandler):
    def get(self):
        data = (cgi.escape(self.request.get('data')))
        hora = (cgi.escape(self.request.get('hora')))
        cidade = (cgi.escape(self.request.get('cidade')))
        local = (cgi.escape(self.request.get('local')))
        message = mail.EmailMessage(sender="Popmundo <iris@popmundo.com>", subject="Popmundo - Iris Records")

        message.to = "Bani <borboleta@gmail.com>"
        message.body = """
        Data: %s
        Hora: %s
        Cidade: %s
        Local: %s
        """ % (data, hora, cidade, local)

        message.send()

application = webapp.WSGIApplication(
                                     [
                                      ('/mail', Mail),
                                    ],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
