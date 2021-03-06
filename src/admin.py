# -*- coding: utf-8 -*-

import logging
import cgi
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users
from model import Genre
from model import Artist
from model import Admin

class User(webapp.RequestHandler):
    " " " Cadastra usuario administrador " " "
    def get(self):
        if not auth_admin():
            self.response.out.write("Acesso negado")
            return
        email = cgi.escape(self.request.get('email')).decode("utf-8")
        charid = int(cgi.escape(self.request.get('charid')))
        charname = cgi.escape(self.request.get('charname')).decode("utf-8")
        logging.info("==> %s" % charname)
        genre = int(cgi.escape(self.request.get('genre')))
        user = Admin(email=email, charId=charid, charName=charname, genre=genre)
        user.put()
        self.response.out.write("Cadastro efetuado com sucesso")

class Manage(webapp.RequestHandler):
    " " " Adiciona ou remove bandas do ranking " " "
    def get(self):
        genre = int(cgi.escape(self.request.get('genre')))
        if not auth_genre(genre):
            self.response.out.write("Acesso negado")
            return
        id = int(cgi.escape(self.request.get('id')))
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
        if not auth_admin():
            self.response.out.write("Acesso negado")
            return
        
        logging.error("Recriando a tabela de generos")
        classica = Genre(id=16, name='Classica', bands=[113188, 808615, 339774, 1195728, 39303, 313967, 1281661, 1052575, 1418803, 1277278, 1489418, 1463301, 133680, 1620949, 1651907, 1608536, 501288, 1618233, 1633169, 783825, 1266364, 1717490, 1666056, 1716718, 1393156, 1738858, 1628526, 1669886, 1779793, 1798078, 1715270, 1708060, 1746029, 1799192, 1796946, 1206821, 1206460, 256866, 1792370, 1847960, 1839493, 1853756, 1657350, 259537, 1378877, 1374360, 1843422, 1882197, 1890789, 1802124, 1663947, 1868661, 1846493, 1658152, 1838241, 1729907, 1850868], lastUpdate=datetime.date.today())
        classica.put()
        latina = Genre(id=17, name='Latina', bands=[948336, 894957, 104252, 165655, 329990, 1014075, 44674, 223858, 220085, 1642306, 1610108, 819632, 1654512, 61109, 187271, 1681099, 871890, 1247081, 1612914], lastUpdate=datetime.date.today())
        latina.put()
        modernrock = Genre(id=4, name='Modern Rock', bands=[59459, 237592, 494751, 459617, 582172, 47124, 1485900, 287309, 1346842, 88786, 792062, 932064, 225831, 95601, 794125, 649206, 94328, 214999, 76251, 779202, 517415, 1083916, 197107, 69990, 995032, 729200, 1701373, 136804, 1141297, 1524696, 1155149, 18098, 501642, 709839, 148237, 36914, 1674139, 750834, 1619704, 1057074, 1623540, 1193499, 1614002, 131517, 1732778, 1837308, 34732, 1091828, 255687, 371271, 440039, 726273, 1251433], lastUpdate=datetime.date.today())
        modernrock.put()
        heavymetal = Genre(id=5, name='Heavy Metal', bands=[685621, 184355, 1604461, 40495, 130432, 124776, 497259, 883774, 51111, 353585, 42927, 746451, 833908, 42958, 54572, 890871, 1549561, 136816, 1553909, 1507013, 1522802, 741261, 1142787, 1158539, 1111306, 94964, 465392, 254192, 1228187, 1190663, 1021031, 1687974, 577080, 1545119, 531902, 214263, 1494750, 1492071, 1387141, 648662, 614310, 479483, 1403380, 1711639, 373429, 413933, 115212, 1652129, 935858, 1060418, 1214004, 1167355, 72611, 918372, 999661, 29046, 379063, 885557, 1880504], lastUpdate=datetime.date.today())
        heavymetal.put()
        eletronica = Genre(id=7, name='Eletronica', bands=[209379, 902742, 1188719, 129130, 93848, 828030, 1306258, 883108, 1476371, 1404501, 953840, 520897, 1338341, 1411183, 635238, 1517085, 249924, 532295, 1639623, 457800, 477559, 387106, 59564, 120854, 887093, 147319, 898091, 451098, 1685021, 1214895, 1367600, 1142771, 1204371, 906371, 1722167, 1727614, 1261678, 1031179, 1689196, 1761628, 1520601, 305199, 780831, 926863, 1295958, 1705741, 1131026, 1554098, 1374478, 581120, 794062, 805432, 1635713, 665196, 1332974, 1510957, 407875], lastUpdate=datetime.date.today())
        eletronica.put()
        pop = Genre(id=8, name='Pop', bands=[49096, 543264, 424075, 42324, 1534850, 376842, 469749, 142508, 264133, 1352680, 279057, 1415253, 1459182, 1498991, 1392869, 1038625, 452107, 1567962, 596419, 532662, 551198, 492602, 1370384, 1131420, 1578977, 230885, 890882, 51666, 1628578, 34275, 1645681, 1904870, 1260489, 76291, 1226188, 1522284, 565190], lastUpdate=datetime.date.today())
        pop.put()
        world = Genre(id=12, name='World Music', bands=[93014, 295590, 1797759, 450556, 263800, 1790913, 1404594, 617137, 429012, 773158, 1764394, 59669, 1798452, 777282, 1071578, 544695, 39705, 1263694, 1648063, 287790, 1749992, 1890314, 172247, 1541540, 97115, 930819, 654910, 1769748, 1036208, 1149655, 1808471, 1854504, 1374513, 921654, 37278, 416066, 314006, 701929, 1781690, 1656243, 1876029, 1775571, 1688965], lastUpdate=datetime.date.today())
        world.put()
        rock = Genre(id=3, name='Rock', bands=[88342, 104937, 668859], lastUpdate=datetime.date.today())
        rock.put()
        country = Genre(id=13, name='Country', bands=[878064, 1161118, 460406, 420654, 1736000, 111160, 416977, 432889, 1559517, 1639868, 1785986, 683930, 1706062, 1663974, 1710956, 1255329, 1672775, 1636417, 1043343, 1734123], lastUpdate=datetime.date.today())
        country.put()
        flamenco = Genre(id=19, name='Flamenco', bands=[1239460, 1679342, 1169799, 1435443, 1021031, 1569030, 966987, 1235226, 1874444, 1181254, 1294504, 1110324, 1894517, 1898061, 1145421, 1550637, 1896162, 1670356], lastUpdate=datetime.date.today())
        flamenco.put()
        punk = Genre(id=6, name='Punk Rock', bands=[285550, 198612, 43886, 1090139, 1253380, 94869, 1004668, 444071, 713094, 445527, 1212123, 1064185, 1686531, 777304, 59007, 497141, 1890722, 895187], lastUpdate=datetime.date.today())
        punk.put()
        blues = Genre(id=15, name='Blues', bands=[1114453, 325886, 22358, 908492, 471296, 1408613, 1141973, 1553171, 769437, 1775046, 1553743, 206950, 1260693, 332666, 65634, 314096, 1008820, 765669, 1668154, 798157, 832935, 497624, 443553, 1803588, 1677193, 32635, 1322332, 625994, 580518, 1534005], lastUpdate=datetime.date.today())
        blues.put()
        hiphop = Genre(id=9, name='Hip Hop', bands=[1408987, 1145465, 1888438, 469586, 1735906, 1775030, 537511, 724094, 486917, 635223, 1531885, 1256116, 121814, 1191277, 1781066, 1870652, 1539448, 1610234, 134068, 889270, 1656068, 1364480, 1839483], lastUpdate=datetime.date.today())
        hiphop.put()
        rb = Genre(id=10, name='R&B', bands=[1402222, 1191044, 1671295, 1850711, 1795504, 568320, 1527471, 1533552, 1500414, 1876910], lastUpdate=datetime.date.today())
        rb.put()
        jazz = Genre(id=14, name='Jazz', bands=[521474, 1915216, 66804, 895252, 218507, 979008, 487234, 88789, 641607, 1384114, 1407160, 26863, 1049948 , 664754, 254600, 1030796, 1834523, 1703631, 1418047, 1347204, 1371232 , 850752, 341800, 1518575, 229055, 939292, 586520, 1894212, 41474, 1825807], lastUpdate=datetime.date.today())
        jazz.put()
        african = Genre(id=18, name='Africana', bands=[586072, 333107, 1928978, 1885961, 1817342, 1878518, 1763279, 1937240, 1570136, 1911668, 1872755, 119850, 1694527, 754481, 1951271, 1971304, 1907179, 1917160, 79110, 1854233], lastUpdate=datetime.date.today())
        african.put()
        reggae = Genre(id=11, name='Reggae', bands=[682385, 834788, 277537, 1617800, 1821623], lastUpdate=datetime.date.today())
        reggae.put()
        teste = Genre(id=1, name='Teste', bands=[1,2], lastUpdate=datetime.date.today())
        teste.put()

class New(webapp.RequestHandler):
    " " " Cria uma nova linha de genero (necessario editar manualmente) " " "
    def get(self):
        if not auth_admin():
            self.response.out.write("Acesso negado")
            return
        logging.info("Criando novo genero")




def auth_admin():
    user = users.get_current_user().email()
    if user == "test@example.com" or user == "borboleta@gmail.com":
        return True
    else:
        logging.error("Acesso negado")
        return False

def auth_genre(genre):
    user = users.get_current_user().email()   
    permission = db.GqlQuery("SELECT * FROM Admin WHERE genre = 1").fetch(10)
    for admin in permission:
        if admin.email == user:
            return True
    permission = db.GqlQuery("SELECT * FROM Admin WHERE genre = :1", genre).fetch(10)
    for admin in permission:
        if admin.email == user:
            return True
    logging.error("Acesso negado: genero %s" % genre)
    return False


application = webapp.WSGIApplication(
                                     [('/admin/update', Manage), ('/admin/create_all_genres', Create), ('/admin/new', New), ('/admin/user', User), ('/admin', Redirect)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


