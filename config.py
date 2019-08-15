import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['xml'])

# NOTE: ALWAYS REPLACE THE SECRET KEY BEFORE RUNNING IN PRODUCTION!
SECRET_KEY = b'_5sdfasdfy2LaspoFdfew\n\xec]/'  