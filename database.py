from sqlalchemy.orm import DeclarativeBase,sessionmaker,Session,declarative_base
from sqlalchemy import create_engine,engine,MetaData

# class Base(DeclarativeBase):
    # pass
Base=declarative_base()
engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)

with Session(engine) as session:
    Session=sessionmaker(bind=engine)
    session=Session()
    
    

