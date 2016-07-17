from models.shared import db

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer)
    name = db.Column(db.Text())
    cover = db.Column(db.Text())
    own = db.Column(db.Boolean())
    release_date = db.Column(db.DateTime)
    platform = db.Column(db.Text())
    rating = db.Column(db.Float)
    developer = db.Column(db.Text())
    


    def __init__(self, name, user_id, game_id, cover, own, platform, release_date=None, rating=None, developer=None):
     self.name = name
     self.user_id = user_id
     self.game_id = game_id
     self.cover = cover
     self.own = own
     self.platform = platform
     self.release_date = release_date
     self.rating = rating
     self.developer = developer
     
