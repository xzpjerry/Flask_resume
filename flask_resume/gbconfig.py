from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_uploads import UploadSet, IMAGES
AVATARS = UploadSet('avatars', IMAGES, default_dest=lambda x: 'avatars')#AVATARs are in ./avatars