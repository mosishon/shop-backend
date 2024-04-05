from sqlalchemy.engine import create_engine
from config import settings

engine = create_engine(settings.database_uri,echo=settings.env=="debug")



