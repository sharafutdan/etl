from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.storages.pg.settings import settings

metadata = MetaData(
    schema="content",
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)

engine = create_engine(
    url=settings.url,
)

Session = sessionmaker(
    bind=engine,
)
