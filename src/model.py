# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Artist(db.Model):
    artistId = db.IntegerProperty()
    name = ""
    rank = db.IntegerProperty()
    brRank = db.IntegerProperty()
    genre = db.IntegerProperty()
    
class Genre(db.Model):
    name = db.StringProperty(required=True)
    ids = db.ListProperty(int)
