from models.shared import db

# TODO -- Add the RATER's ID to track

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    giv_id = db.Column(db.Integer)
    rec_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    stars = db.Column(db.Integer)

def __init__(self, giv_id, rec_id, stars):
     self.giv_id = giv_id
     self.rec_id = rec_id
     self.stars = stars

