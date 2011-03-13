import urllib
import logging
import datetime
from google.appengine.ext import db
from google.appengine.api import urlfetch
from model import Artist

class RankGenerator():
    " " " Classe responsavel por obter todas as informacoes de cada banda e salvar o resultado " " "
    
    def __init__(self):
        self.rank = []
        self.skipSave = True
    
    def updateRank(self, genre):
        logging.info("Ranking de " + genre.name)
        self.fillData(genre.bands, genre.id)
        self.save()
            
    def readChart(self, genre):
        chart = ""
        for division in range(1, 13):
            form_fields = {
                           "CountryID": "0",
                           "GenreTypeID": genre,
                           "DivisionID": division
            }
            form_data = urllib.urlencode(form_fields)
            chart += urlfetch.fetch(url="http://www.popmundo.com/common/Charts.asp?action=ArtistRankings",
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'}).content
            utf8=chart.decode("utf-8")
        return utf8

    def fillData(self, bands, genre):
        chart = self.readChart(genre)
        for artistId in bands:
            x = Artist(key_name=str(artistId))
            x.artistId = artistId
            x.genre = genre
            try:
                pos = chart.index('<a href="Artist.asp?action=view&ArtistID=%d">' % artistId)
                posRank = chart.rindex('&nbsp;',0,pos) + 6
                x.rank = int(chart[posRank:chart.rindex('</td>',posRank,pos)])
                posName = chart.index('">',pos) + 2
                x.name = chart[posName:chart.index('</',posName)]
            except:
                x.rank = 99999
                x.brRank = 999
                x.name = "Artista id %s fora do ranking nesta atualiza&ccedil;&atilde;o" % artistId
            self.rank.append(x)
        self.rank.sort(key=lambda x:x.rank)
        self.calculateDiff()
    
    def calculateDiff(self):
        i = 1
        for x in self.rank:
            saveData = db.get(x.key())
            x.brRank = i
            try:
                x.diff = saveData.rank - x.rank
                x.brDiff = saveData.brRank - i
                if x.diff != 0:
                    self.skipSave = False
            except:
                x.diff = 0
                x.brDiff = 0
                self.skipSave = False
            i+=1
                
    def save(self):
        if self.skipSave or self.rank is None or len(self.rank) == 0 or self.rank[0].rank == 99999:
            return
        logging.info("Atualizando dados na base")
        for position in self.rank:
            position.put()
        genre = db.GqlQuery("SELECT * FROM Genre WHERE id = :1", self.rank[0].genre).fetch(1)[0]
        genre.lastUpdate = datetime.date.today()
        genre.put()
