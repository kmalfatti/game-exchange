from models.shared import db

# TODO -- Add the RATER's ID to track

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rec_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    stars = db.Column(db.Integer)

def __init__(self, rec_id, stars):
     self.rec_id = rec_id
     self.stars = stars

