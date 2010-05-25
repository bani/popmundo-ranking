# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Artist(db.Model):
    artistId = db.IntegerProperty()
    name = ""
    rank = db.IntegerProperty()
    brRank = db.IntegerProperty()
    genre = db.IntegerProperty()
    
class Genre(db.Model):
    id = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    bands = db.ListProperty(int)
