from models.shared import db

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text())
    cover = db.Column(db.Text())
    release_date = db.Column(db.DateTime)
    platform = db.Column(db.Text())
    rating = db.Column(db.Float)
    developer = db.Column(db.Text())


    def __init__(self, name, game_id, cover, release_date, platform, rating, developer):
     self.name = name
     self.game_id = game_id
     self.cover = cover
     self.release_date = release_date
     self.platform = platform
     self.rating = rating
     self.developer = developer
     
