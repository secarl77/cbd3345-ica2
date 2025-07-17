import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = (
        
"postgresql://postgres:DevOps2024*@database-cdb-3375-final-project.cl2gqc6scvwd.ca-central-1.rds.amazonaws.com/webappdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session configuration (if used)
    SESSION_TYPE = "filesystem"






