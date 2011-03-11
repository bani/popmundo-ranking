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
        classica = Genre(id=16, name='Classica', bands=[113188, 808615, 339774, 1195728, 39303, 313967, 1281661, 1052575, 1418803, 1277278, 1353451, 1489418, 1463301, 133680, 1620949, 1651907, 1608536, 501288, 1618233, 1633169, 783825, 1266364, 1717490, 1666056, 1716718, 1393156, 1738858, 1628526, 1669886, 1779793, 1798078, 1715270, 1708060, 1746029, 1799192, 1796946, 1206821, 1206460, 256866, 1792370, 1847960, 1839493, 1853756, 1657350, 259537, 1378877, 1374360, 1843422, 1882197, 1890789, 1802124, 1663947, 1868661, 1846493, 1658152, 1838241], lastUpdate=datetime.date.today())
        classica.put()
        latina = Genre(id=17, name='Latina', bands=[948336, 894957, 104252, 165655, 329990, 1014075, 44674, 223858, 220085, 230885, 1642306, 1610108, 819632, 1654512, 61109, 187271, 1681099, 871890, 1728908, 1247081, 1612914], lastUpdate=datetime.date.today())
        latina.put()
        modernrock = Genre(id=4, name='Modern Rock', bands=[59459, 237592, 494751, 459617, 582172, 47124, 1485900, 287309, 1346842, 88786, 792062, 932064, 225831, 95601, 794125, 649206, 94328, 214999, 76251, 779202, 517415, 1083916, 197107, 69990, 995032, 729200, 1701373, 136804, 1141297, 1524696, 1155149, 18098, 501642, 709839, 148237, 36914, 1674139, 750834, 1619704, 1057074, 1623540, 1193499, 1614002, 131517, 1732778, 1837308, 34732], lastUpdate=datetime.date.today())
        modernrock.put()
        heavymetal = Genre(id=5, name='Heavy Metal', bands=[685621, 184355, 1604461, 40495, 130432, 124776, 497259, 883774, 51111, 353585, 42927, 746451, 833908, 42958, 54572, 890871, 1549561, 136816, 1553909, 1507013, 1522802, 741261, 1142787, 1158539, 1111306, 94964, 465392, 254192, 1228187, 1190663, 1021031, 1687974, 577080, 1545119, 531902, 214263, 1494750, 1492071, 1387141, 648662, 614310, 479483, 1403380, 1711639, 373429, 413933, 115212, 1652129, 935858, 1060418, 1214004, 1167355, 72611, 918372], lastUpdate=datetime.date.today())
        heavymetal.put()
        eletronica = Genre(id=7, name='Eletronica', bands=[209379, 902742, 1188719, 129130, 93848, 828030, 1306258, 883108, 1476371, 1404501, 953840, 520897, 1338341, 1411183, 635238, 1517085, 249924, 532295, 1639623, 457800, 477559, 387106, 59564, 120854, 887093, 147319, 898091, 451098, 1685021, 1214895, 1367600, 1142771, 1204371, 906371, 1722167, 1727614, 1261678, 1031179, 1689196, 1761628, 1520601, 305199, 780831, 926863, 1295958, 1705741, 1131026, 1554098, 1374478, 581120, 794062, 805432, 1635713, 665196, 1332974], lastUpdate=datetime.date.today())
        eletronica.put()
        pop = Genre(id=8, name='Pop', bands=[49096, 543264, 424075, 42324, 1534850, 376842, 469749, 142508, 264133, 1352680, 279057, 1415253, 1459182, 1498991, 1392869, 1038625, 452107, 1567962, 596419, 532662, 551198, 492602, 1370384, 1522284, 1131420, 1578977, 230885, 890882, 51666, 1628578, 34275], lastUpdate=datetime.date.today())
        pop.put()
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


