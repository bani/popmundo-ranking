# -*- coding: utf-8 -*-

import urllib
import re
import logging
import cgi
import datetime
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch
from model import Artist

class RankWriter(webapp.RequestHandler):
    " " " Classe responsavel por obter todas as informacoes de cada banda e gerar o html com o resultado " " "
    
    def createRank(self, genre, save):
        rank = self.getInfo(genre.bands, genre.id)
        self.printHtml(rank, genre.name)
        if save:
            logging.info("Atualizando dados na base")
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
        return rank


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
            except:
                x.rank = 99999
                x.brRank = 999
                x.name = "ERRO"
                x.put()

        rankList.sort(key=lambda x:x.rank)
        return rankList

    def printHtml(self, rank, genre):
        html = "<HTML><HEAD><TITLE>Ranking Brasil/Portugal - %s</TITLE></HEAD><BODY><FONT FACE=Arial SIZE=-1>" % genre
        today = datetime.date.today()
        html+=("Atualizado em %s<br/><br/>" % today.strftime("%d/%m/%Y"))
        i = 1
        for position in rank:
            try:
                oldRank = db.get(position.key())
                if oldRank is None:
                    oldRank = Artist(brRank=i,rank=position.rank)
                if i%10==1:
                    html += "<br>"
                    html += "<b><i>TOP "
                    html += str(i/10+1)
                    html += "0:</i></b><br>"
                html += "%02d" % i
                brDiff = oldRank.brRank - i
                html += " (%s)" % ("=" if brDiff == 0 else str(brDiff) if brDiff < 0 else "+"+str(brDiff))
                html += " #"
                html += "<b>%03d</b>" % position.rank
                html += " [artistid=%d name=%s]" % (position.artistId, position.name.decode("utf-8"))
                globalDiff = oldRank.rank - position.rank
                html += " (%s)" % ("=" if globalDiff == 0 else str(globalDiff) if globalDiff < 0 else "+"+str(globalDiff))
                html += "<br>"
                i+=1
            except:
                logging.error("Erro ao imprimir artista %d", position.artistId)
        html += "</FONT></BODY></HTML>"
        self.response.out.write(html)

    def save(self, rank):
        i = 1
        for position in rank:
            position.brRank = i
            position.put()
            i+=1

class Classica(RankWriter):
    def get(self):
        save = (cgi.escape(self.request.get('save')))
        genre = db.GqlQuery("SELECT * FROM Genre WHERE id = 16").fetch(1)[0]
        logging.info("Gerando ranking de musica classica")
        self.createRank(genre, True if save == "true" else False)
        
class Latina(RankWriter):
    def get(self):
        genre = db.GqlQuery("SELECT * FROM Genre WHERE id = 17").fetch(1)[0]
        logging.info("Gerando ranking de musica latina")
        self.createRank(genre, True)

class ListUnranked(webapp.RequestHandler):
    " " " Lista as bandas que nao conseguiram entrar no rank na ultima atualizacao " " "
    def get(self):
        genres = {16: 'Classica', 17: 'Latina'}
        unranked = db.GqlQuery("SELECT * FROM Artist WHERE rank = 99999").fetch(10)
        for band in unranked:
            self.response.out.write("%s: <a href='http://www.popmundo.com/Common/Artist.asp?action=view&ArtistID=%d'>banda fora do ranking</a><br/>" % (genres[band.genre], band.artistId))

application = webapp.WSGIApplication(
                                     [
                                      ('/', Classica),
                                      ('/classica', Classica),
                                      ('/latina', Latina),
                                      ('/list', ListUnranked)],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
