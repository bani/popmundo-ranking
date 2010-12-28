# -*- coding: utf-8 -*-

import logging
import cgi
import datetime
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
        classica = Genre(id=16, name='Classica', bands=[113188, 808615, 339774, 1195728, 39303, 313967, 1281661, 1052575, 1418803, 1277278, 1401702, 1353451, 1489418, 1463301, 133680, 1423891, 1620949, 1651907, 1608536, 501288, 1618233, 1633169, 783825, 1266364, 1717490, 1666056, 1716718, 1393156, 1738858, 1628526, 1749594, 1669886, 1779793, 1798078, 1715270, 1708060, 1746029, 1799192, 1729907, 1796946, 1206821, 1206460, 256866], lastUpdate=datetime.date.today())
        classica.put()
        latina = Genre(id=17, name='Latina', bands=[948336, 894957, 104252, 165655, 329990, 1014075, 44674, 223858, 220085, 230885, 1642306, 1610108, 819632, 1654512, 61109, 187271, 1681099, 871890, 1728908, 1247081, 1612914], lastUpdate=datetime.date.today())
        latina.put()
        modernrock = Genre(id=4, name='Modern Rock', bands=[59459, 237592, 229055, 380939, 494751, 459617, 582172, 47124, 1485900, 287309, 1346842, 88786, 792062, 932064, 440039, 225831, 95601, 794125, 649206, 185570, 94328, 371271, 214999, 76251, 779202, 517415, 255687, 1083916, 360550, 197107, 69990, 995032, 729200, 131517, 1701373, 136804, 1141297, 1524696, 1091828, 1155149, 1251433, 18098, 501642, 709839, 148237, 1520601, 36914, 1674139, 750834, 1619704, 1057074, 1623540, 1193499, 1614002], lastUpdate=datetime.date.today())
        modernrock.put()
        heavymetal = Genre(id=5, name='Heavy Metal', bands=[685621, 184355, 1604461, 40495, 130432, 124776, 497259, 883774, 51111, 353585, 42927, 746451, 833908, 42958, 54572, 890871, 1549561, 136816, 1553909, 1507013, 1522802, 741261, 1142787, 1158539, 1111306, 94964, 465392, 254192, 1228187, 1190663, 1021031, 1687974, 577080, 29046, 1545119, 531902, 214263, 1494750, 379063, 1492071, 1387141, 648662, 999661, 104647, 614310, 885557, 479483, 1403380, 1711639, 373429, 413933, 115212, 1652129, 935858, 1060418, 1214004], lastUpdate=datetime.date.today())
        heavymetal.put()
        eletronica = Genre(id=7, name='Eletronica', bands=[209379,902742,1188719,129130,93848,828030,1306258,120854,883108,1476371,1404501,1051638,953840,887093,520897,1722167,1338341,535621,1411183,635238,1517085,249924,798289,147319,898091,532295,451098,1639623,457800,477559,387106,59564], lastUpdate=datetime.date.today())
        eletronica.put()
        teste = Genre(id=1, name='Teste', bands=[1,2], lastUpdate=datetime.date.today())
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


