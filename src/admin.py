# -*- coding: utf-8 -*-

import logging
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from model import Genre
from model import Artist

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
            removed = Artist(key_name=str(id))
            removed.artistId = id
            removed.genre = 99
            removed.brRank = 999
            removed.rank = 99999
            removed.put()
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
        classica = Genre(id=16, name='Classica', bands=[113188, 808615, 339774, 1463261, 1151965, 1195728, 39303, 313967, 1281661, 1531321, 1343033, 1052575, 1418803, 307738, 1277278, 1005654, 1401702, 1445010, 357148, 1043727, 1353451, 1565808, 1508232, 1489418, 855456, 1463301, 744395, 133680, 1423891, 1268107, 385407, 1620949, 1651907, 1608536, 1647328, 501288, 1274742, 1443245, 1618233, 1677115, 1595502, 1633169, 783825, 726273, 1266364, 1717490, 1558800, 1666056, 1716718, 1665563, 1393156, 1738858, 1628526, 1749594, 1669886, 1760674, 1708360, 1711592])
        classica.put()
        latina = Genre(id=17, name='Latina', bands=[948336, 894957, 104252, 165655, 329990, 1014075, 96062, 44674, 223858, 220085, 230885, 1642306, 1610108, 819632])
        latina.put()
        modernrock = Genre(id=4, name='Modern Rock', bands=[59459, 237592, 229055, 380939, 494751, 459617, 582172, 47124, 1485900, 287309, 1346842, 88786, 792062, 932064, 440039, 225831, 95601, 794125, 649206, 185570, 94328, 371271, 214999, 76251, 779202, 517415, 255687, 1083916, 360550, 197107, 1602933, 69990, 995032, 729200, 131517, 1701373, 1375835, 136804, 1141297, 1524696])
        modernrock.put()
        heavymetal = Genre(id=5, name='Heavy Metal', bands=[685621, 184355, 1604461, 40495, 130432, 124776, 497259, 883774, 51111, 353585, 192212, 737760, 42927, 746451, 176033, 1074514, 833908, 42958, 54572, 890871, 1142771, 1549561, 136816, 122449, 1553909, 193166, 1507013, 1480776, 1522802, 631208, 1101677, 741261, 1142787, 1158539, 879431, 1111306, 94964, 465392, 254192, 332742, 887637, 523637, 1228187, 1190663, 1021031, 900679, 1687974, 577080, 415460, 29046, 115212, 1545119, 1129348, 531902, 214263, 1494750, 379063, 1492071, 1387141, 648662, 999661, 1693730, 104647, 614310, 1543473, 85671, 885557, 479483, 1403380, 323496, 546643, 1701837])
        heavymetal.put()
        teste = Genre(id=1, name='Teste', bands=[1,2])
        teste.put()

class New(webapp.RequestHandler):
    " " " Cria uma nova linha de genero (necessario editar manualmente) " " "
    def get(self):
        logging.info("Criando novo genero")
        
application = webapp.WSGIApplication(
                                     [('/admin/update', Manage), ('/admin/create', Create), ('/admin/new', New), ('/admin', Redirect)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


