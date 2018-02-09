from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine('sqlite:///deck_builder.db')   

Session = sessionmaker(bind=Engine)
ses = Session()