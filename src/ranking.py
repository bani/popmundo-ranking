# -*- coding: utf-8 -*-

import logging
import cgi
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import model
from generator import RankGenerator

class RankWriter(webapp.RequestHandler):
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
  
    def go(self, id, name):
        force = (cgi.escape(self.request.get('save')))
        genre = db.GqlQuery("SELECT * FROM Genre WHERE id = :1", id).fetch(1)[0]
        save = force == "on" or genre.lastUpdate < datetime.date.today()
        if id == 16:
            save = True if force == "true" else False
        if save:
            generator = RankGenerator()
            generator.updateRank(genre)
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
        unranked = db.GqlQuery("SELECT * FROM Artist WHERE rank = 99999").fetch(100)
        for band in unranked:
            self.response.out.write("%s: <a href='http://www.popmundo.com/Common/Artist.asp?action=view&ArtistID=%d'>banda fora do ranking</a><br/>" % (genres[band.genre], band.artistId))

class Home(RankWriter):
    def get(self):
        self.redirect("/static/index.html")

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
