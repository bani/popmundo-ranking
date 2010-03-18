import urllib
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Artist:
    artistId = 0
    name = ""
    rank = 1

class RankWriter(webapp.RequestHandler):
    def writeRank(self,bands,genre):
        rankList = []
        for artistId in bands:
            x = Artist()
            x.artistId = artistId
            try:
                site = urllib.urlopen("http://www.popmundo.com/Common/Artist.asp?action=view&ArtistID=%d"  % (artistId)).read()    
                x.rank = int(re.search ( '<b>#(\d+)</b> %s artist.' % genre, site).group(1))
                x.name = re.search ( 'document.title = "Popmundo - (.+)"', site ).group(1)
            except:
                x.rank = 99999
                x.name = "ERRO"
            rankList.append(x)
        
        self.response.out.write("<HTML><HEAD><TITLE>%s - pt</TITLE></HEAD><BODY><FONT FACE=Arial SIZE=-1>" % (genre))
    
        rankList.sort(key=lambda x:x.rank)
        i = 1
        for position in rankList:
            if i%10==1:
                self.response.out.write("<br>")
                self.response.out.write("<b><i>TOP ")
                self.response.out.write(i/10+1)
                self.response.out.write("0:</i></b><br>")
            self.response.out.write("%02d" % i)
            self.response.out.write(" #")
            self.response.out.write("<b>%03d</b>" % position.rank)
            self.response.out.write(" [artistid=%d name=%s]" % (position.artistId, position.name))
            self.response.out.write("<br>")
            i+=1
        self.response.out.write("</FONT></BODY></HTML>")

class MainPage(RankWriter):
    def get(self):
        br = [113188, 808615, 726273, 339774, 1463261, 1151965, 1195728, 39303, 313967, 1281661, 1531321, 1343033, 1052575, 1418803, 307738, 1277278, 1005654, 1401702, 1445010, 357148, 1043727, 1353451, 1565808, 1508232, 1489418, 854190, 855456, 1463301, 1392207, 744395, 133680, 1423891, 1268107, 385407, 1620949, 1651907, 1608536, 1647328, 1418691]
        self.writeRank(br,'Classical')
        
class Latina(RankWriter):
    def get(self):
        br = [948336, 894957, 104252, 165655, 329990, 1014075, 96062, 44674, 223858, 220085, 230885, 59564, 1642306, 1610108, 952064, 1670412]
        self.writeRank(br,'Latin Music')
        
class Jazz(RankWriter):
    def get(self):
        br = [521474, 498898, 66804]
        self.writeRank(br,'Jazz')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/latina', Latina),
                                     ('/jazz', Jazz)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()