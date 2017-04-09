from app import db

class METS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metsfile = db.Column(db.String(120), index=True, unique=True)
    metslist = db.Column(db.PickleType, index=True, unique=True)

    def __init__(self, metsfile, metslist):
        self.metsfile = metsfile
        self.metslist = metslist

    def __repr__(self):
        return '<File %r>' % self.metsfile