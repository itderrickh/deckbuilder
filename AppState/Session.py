from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine('sqlite:///:memory:')   

Session = sessionmaker(bind=Engine)
ses = Session()