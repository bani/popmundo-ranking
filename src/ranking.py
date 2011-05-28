# -*- coding: utf-8 -*-

import logging
import cgi
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import model
from generator import RankGenerator
import os
from google.appengine.ext.webapp import template

class RankWriter(webapp.RequestHandler):
    def printHtml(self, rank, genre):
        for position in rank:
            try:
                position.changeBr = "(%s)" % ("=" if position.brDiff == 0 else "*" if position.brDiff > 500 else str(position.brDiff) if position.brDiff < 0 else "+"+str(position.brDiff))
                position.changeWorld = "(%s)" % ("=" if position.diff == 0 else "*" if position.diff > 5000 else str(position.diff) if position.diff < 0 else "+"+str(position.diff))
            except:
                logging.error("Erro ao imprimir artista %d", position.artistId)
                
        rankCopy = []
        rankCopy.extend(rank)
        max = 30 if len(rankCopy) > 30 else len(rankCopy)
        rankCopy = rankCopy[0:max]
        rankCopy.sort(key=lambda x:x.diff, reverse=True)
        subida = rankCopy[0]
        queda = rankCopy[-1]
        template_values = {'bandas': rank, 'genero': genre.name,'data': genre.lastUpdate.strftime("%d/%m/%Y"), 'subida': subida, 'queda': queda}
        path = os.path.join(os.path.dirname(__file__), 'ranking.html')
        self.response.out.write(template.render(path, template_values))

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

class Eletronica(RankWriter):
    def get(self):
        self.go(7, "eletronica")
        
class Pop(RankWriter):
    def get(self):
        self.go(8, "pop")

class WorldMusic(RankWriter):
    def get(self):
        self.go(12, "world music")

class Rock(RankWriter):
    def get(self):
        self.go(3, "rock")

class Country(RankWriter):
    def get(self):
        self.go(13, "country")

class Flamenco(RankWriter):
    def get(self):
        self.go(19, "flamenco")
        
class Punk(RankWriter):
    def get(self):
        self.go(6, "punk")

class Blues(RankWriter):
    def get(self):
        self.go(15, "blues")
        
class HipHop(RankWriter):
    def get(self):
        self.go(9, "hiphop")

class ListUnranked(webapp.RequestHandler):
    " " " Lista as bandas que nao conseguiram entrar no rank na ultima atualizacao " " "
    def get(self):
        genres = {16: 'Classica', 17: 'Latina', 4: 'Modern Rock', 5: 'Heavy Metal', 7: 'Eletronica', 8: 'Pop', 12: 'World Music', 3: 'Rock', 13: 'Country', 19: 'Flamenco', 6: 'Punk', 15: 'Blues', 9: 'Hip Hop', 99: 'Remover'}
        unranked = db.GqlQuery("SELECT * FROM Artist WHERE rank = 99999").fetch(100)
        if unranked is not None:
            unranked.sort(key=lambda x:x.genre)
        for band in unranked:
            self.response.out.write("%s: banda <a href='http://www.popmundo.com/Common/Artist.asp?action=view&ArtistID=%d'>%d</a> fora do ranking<br/>" % (genres[band.genre], band.artistId, band.artistId))

application = webapp.WSGIApplication(
                                     [
                                      ('/classica', Classica),
                                      ('/latina', Latina),
                                      ('/mr', ModernRock),
                                      ('/hm', HeavyMetal),
                                      ('/eletronica', Eletronica),
                                      ('/pop', Pop),
                                      ('/worldmusic', WorldMusic),
                                      ('/rock', Rock),
                                      ('/country', Country),
                                      ('/flamenco', Flamenco),
                                      ('/punkrock', Punk),
                                      ('/blues', Blues),
                                      ('/hiphop', HipHop),
                                      ('/list', ListUnranked)],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
