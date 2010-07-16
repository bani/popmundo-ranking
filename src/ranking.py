# -*- coding: utf-8 -*-

import urllib
import logging
import cgi
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch
from model import Artist

class RankWriter(webapp.RequestHandler):
    " " " Classe responsavel por obter todas as informacoes de cada banda e gerar o html com o resultado " " "
    
    def createRank(self, genre):
        rank = self.getInfo(genre.bands, genre.id)
        self.save(rank)
            
    def getFullRank(self, genre):
        rank = ""
        for division in range(2, 12):
            form_fields = {
                           "CountryID": "0",
                           "GenreTypeID": genre,
                           "DivisionID": division
            }
            form_data = urllib.urlencode(form_fields)
            rank += urlfetch.fetch(url="http://www.popmundo.com/common/Charts.asp?action=ArtistRankings",
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'}).content
            rankUTF8=rank.decode("utf-8")
        return rankUTF8


    def getInfo(self, bands, genre):
        rankList = []
        fullRank = self.getFullRank(genre)
        for artistId in bands:
            x = Artist(key_name=str(artistId))
            x.artistId = artistId
            x.genre = genre
            try:
                pos = fullRank.index('<a href="Artist.asp?action=view&ArtistID=%d">' % artistId)
                posRank = fullRank.rindex('&nbsp;',0,pos) + 6
                x.rank = int(fullRank[posRank:fullRank.rindex('</td>',posRank,pos)])
                posName = fullRank.index('">',pos) + 2
                x.name = fullRank[posName:fullRank.index('</',posName)]
                rankList.append(x)
            except Exception, e:
                logging.debug("Banda: " + str(artistId) + ". Erro: " + str(e))
                x.rank = 99999
                x.brRank = 999
                x.name = "ERRO"

        rankList.sort(key=lambda x:x.rank)
        self.calculateDiff(rankList)
        
        return rankList
    
    def calculateDiff(self, rank):
        i = 0
        for x in rank:
            i+=1
            saveData = db.get(x.key())
            x.brRank = i
            try:
                x.diff = saveData.rank - x.rank
                x.brDiff = saveData.brRank - i
            except:
                x.diff = 0
                x.brDiff = 0
        
    def printHtml(self, rank, genre):
        html = "<HTML><HEAD><TITLE>Ranking Brasil/Portugal - %s</TITLE></HEAD><BODY><FONT FACE=Arial SIZE=-1>" % genre.name
        html+=("Atualizado em %s<br/><br/>" % genre.lastUpdate.strftime("%d/%m/%Y"))
        i = 1
        for position in rank:
            try:
                if i%10==1:
                    html += "<br>"
                    html += "<b><i>TOP "
                    html += str(i/10+1)
                    html += "0:</i></b><br>"
                html += "%02d" % position.brRank
                html += " (%s)" % ("=" if position.brDiff == 0 else str(position.brDiff) if position.brDiff < 0 else "+"+str(position.brDiff))
                html += " #"
                html += "<b>%03d</b>" % position.rank
                html += " [artistid=%d name=%s]" % (position.artistId, position.name)
                html += " (%s)" % ("=" if position.diff == 0 else str(position.diff) if position.diff < 0 else "+"+str(position.diff))
                html += "<br>"
                i+=1
            except:
                logging.error("Erro ao imprimir artista %d", position.artistId)
        html += "</FONT></BODY></HTML>"
        self.response.out.write(html)

    def save(self, rank):
        if len(rank) == 0 or rank[0].rank == 99999:
            return
        logging.info("Atualizando dados na base")
        for position in rank:
            position.put()
        genre = db.GqlQuery("SELECT * FROM Genre WHERE id = :1", rank[0].genre).fetch(1)[0]
        genre.lastUpdate = datetime.date.today()
        genre.put()
        
    def go(self, id, name):
        force = (cgi.escape(self.request.get('save')))
        genre = db.GqlQuery("SELECT * FROM Genre WHERE id = :1", id).fetch(1)[0]
        save = force == "true" or genre.lastUpdate < datetime.date.today() - datetime.timedelta(days=1)
        if id == 16:
            save = True if force == "true" else False
        if save:
            logging.info("Gerando ranking de " + name)
            self.createRank(genre)
        logging.info("=> Ranking de " + name) 
        rank = db.GqlQuery("SELECT * FROM Artist WHERE genre = :1 ORDER BY rank", id).fetch(100)
        self.printHtml(rank, genre)

class Classica(RankWriter):
    def get(self):
        self.go(16, "musica classica")
        
class Latina(RankWriter):
    def get(self):
        self.go(17, "musica latina")
        
class ModernRock(RankWriter):
    def get(self):
        self.go(4, "modern rock")
        
class HeavyMetal(RankWriter):
    def get(self):
        self.go(5, "heavy metal")

class ListUnranked(webapp.RequestHandler):
    " " " Lista as bandas que nao conseguiram entrar no rank na ultima atualizacao " " "
    def get(self):
        genres = {16: 'Classica', 17: 'Latina', 4: 'Modern Rock', 5: 'Heavy Metal', 99: 'Remover'}
        unranked = db.GqlQuery("SELECT * FROM Artist WHERE rank = 99999").fetch(10)
        for band in unranked:
            self.response.out.write("%s: <a href='http://www.popmundo.com/Common/Artist.asp?action=view&ArtistID=%d'>banda fora do ranking</a><br/>" % (genres[band.genre], band.artistId))

class Home(RankWriter):
    def get(self):
        self.redirect("/classica")

application = webapp.WSGIApplication(
                                     [
                                      ('/', Home),
                                      ('/classica', Classica),
                                      ('/latina', Latina),
                                      ('/mr', ModernRock),
                                      ('/hm', HeavyMetal),
                                      ('/list', ListUnranked)],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
