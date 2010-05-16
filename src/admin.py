# -*- coding: utf-8 -*-

import logging
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from model import Genre

class Manage(webapp.RequestHandler):
    " " " Adiciona ou remove bandas do ranking " " "
    def get(self):
        id = int(cgi.escape(self.request.get('id')))
        genre = cgi.escape(self.request.get('genre'))
        artistList = db.GqlQuery("SELECT * FROM Genre WHERE name = :1", genre).fetch(1)[0]
        exists = artistList.ids.count(id) > 0
        if exists:
            logging.info("Removendo a banda " + str(id) + " do genero " + genre)
            artistList.ids.remove(id)
        else:
            logging.info("Adicionando a banda " + str(id) + " para o genero " + genre)
            artistList.ids.append(id)
        artistList.put()
        
        self.response.out.write("Operacao concluida com sucesso!")

class Redirect(webapp.RequestHandler):
    " " " Redireciona para a interface administrativa " " "
    def get(self):
        self.redirect("http://classicamundo.appspot.com/a/admin.html")

application = webapp.WSGIApplication(
                                     [('/admin/update', Manage), ('/admin', Redirect)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


