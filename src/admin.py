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
        genre = int(cgi.escape(self.request.get('genre')))
        artistList = db.GqlQuery("SELECT * FROM Genre WHERE id = :1", genre).fetch(1)[0]
        exists = artistList.bands.count(id) > 0
        if exists:
            logging.info("Removendo a banda %d do genero %s" % (id, artistList.name))
            artistList.bands.remove(id)
        else:
            logging.info("Adicionando a banda %d para o genero %s"  % (id, artistList.name))
            artistList.bands.append(id)
        artistList.put()
        
        self.response.out.write("A banda %d foi %s com sucesso!" % (id, "removida" if exists else "adicionada"))

class Redirect(webapp.RequestHandler):
    " " " Redireciona para a interface administrativa " " "
    def get(self):
        self.redirect("http://classicamundo.appspot.com/a/admin.html")
        
class Create(webapp.RequestHandler):
    " " " Recria tabela de generos " " "
    def get(self):
        classica = Genre(id=16, name='Classica', bands=[113188, 808615, 339774, 1463261, 1151965, 1195728, 39303, 313967, 1281661, 1531321, 1343033, 1052575, 1418803, 307738, 1277278, 1005654, 1401702, 1445010, 357148, 1043727, 1353451, 1565808, 1508232, 1489418, 855456, 1463301, 1392207, 744395, 133680, 1423891, 1268107, 385407, 1620949, 1651907, 1608536, 1647328, 501288, 1274742, 1443245, 1574905, 1618233, 1677115, 1595502, 255494, 1633169, 783825, 726273, 1266364])
        classica.put()
        latina = Genre(id=17, name='Latina', bands=[948336, 894957, 104252, 165655, 329990, 1014075, 96062, 44674, 223858, 220085, 230885, 1642306, 1610108, 1670412, 819632])
        latina.put()
        teste = Genre(id=1, name='Teste', bands=[1,2])
        teste.put()
        
application = webapp.WSGIApplication(
                                     [('/admin/update', Manage), ('/admin/create', Create), ('/admin', Redirect)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


