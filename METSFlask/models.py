from METSFlask import db


class METSFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metsfile = db.Column(db.String(120), index=True, unique=True)
    nickname = db.Column(db.String(120))
    fsfiles = db.relationship('FSFile', backref='metsfile', lazy=True,
                              cascade='all,delete')

    def __init__(self, metsfile, nickname):
        self.metsfile = metsfile
        self.nickname = nickname

    def __repr__(self):
        return '<METSFile {}>'.format(self.metsfile)


class FSFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)
    use = db.Column(db.String)
    file_uuid = db.Column(db.String)
    file_id = db.Column(db.String)
    metsfile_id = db.Column(db.Integer, db.ForeignKey('mets_file.id'),
                            nullable=False)

    admids = db.relationship('ADMID', backref='fsfile', lazy=True,
                             cascade='all,delete')
    premis_objects = db.relationship('PREMISObject', backref='fsfile',
                                     lazy=True, cascade='all,delete')
    premis_events = db.relationship('PREMISEvent', backref='fsfile',
                                    lazy=True, cascade='all,delete')

    def __init__(self, path, use, file_uuid, file_id, metsfile_id):
        self.path = path
        self.use = use
        self.file_uuid = file_uuid
        self.file_id = file_id
        self.metsfile_id = metsfile_id

    def __repr__(self):
        return '<FSFile {}>'.format(self.file_uuid)


class ADMID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admid = db.Column(db.String)
    fsfile_id = db.Column(db.Integer, db.ForeignKey('fs_file.id'),
                          nullable=False)

    def __init__(self, admid, fsfile_id):
        self.admid = admid
        self.fsfile_id = fsfile_id

    def __repr__(self):
        return '<ADMID {}>'.format(self.admid)


class PREMISObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_output = db.Column(db.String)
    message_digest = db.Column(db.String)
    message_digest_algorithm = db.Column(db.String)
    size = db.Column(db.String)
    format_name = db.Column(db.String)
    format_version = db.Column(db.String)
    format_registry_key = db.Column(db.String)
    format_registry_name = db.Column(db.String)
    fsfile_id = db.Column(db.Integer, db.ForeignKey('fs_file.id'),
                          nullable=False)

    def __init__(self, raw_output, message_digest, message_digest_algorithm,
                 size, format_name, format_version, format_registry_key,
                 format_registry_name, fsfile_id):
        self.raw_output = raw_output
        self.message_digest = message_digest
        self.message_digest_algorithm = message_digest_algorithm
        self.size = size
        self.format_name = format_name
        self.format_version = format_version
        self.format_registry_key = format_registry_key
        self.format_registry_name = format_registry_name
        self.fsfile_id = fsfile_id

    def __repr__(self):
        return '<PREMISObject {}, file {}>'.format(self.id, self.fsfile_id)


class PREMISEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_output = db.Column(db.String)
    fsfile_id = db.Column(db.Integer, db.ForeignKey('fs_file.id'),
                          nullable=False)

    def __init__(self, raw_output, fsfile_id):
        self.raw_output = raw_output
        self.fsfile_id = fsfile_id

    def __repr__(self):
        return '<PREMISEvent {}, file {}>'.format(self.id, self.fsfile_id)

# class DCMetadata(db.Model)
# class PREMISEvent(db.Model)
