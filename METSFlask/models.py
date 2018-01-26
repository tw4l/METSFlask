from METSFlask import db

class METS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metsfile = db.Column(db.String(120), index=True, unique=True)
    nickname = db.Column(db.String(120))
    metslist = db.Column(db.PickleType, index=True, unique=True)
    dcmetadata = db.Column(db.PickleType)
    originalfilecount = db.Column(db.Integer())

    def __init__(self, metsfile, nickname, metslist, dcmetadata, originalfilecount):
        self.metsfile = metsfile
        self.nickname = nickname
        self.metslist = metslist
        self.dcmetadata = dcmetadata
        self.originalfilecount = originalfilecount

    def __repr__(self):
        return '<File %r>' % self.metsfile
