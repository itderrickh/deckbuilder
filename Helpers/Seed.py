from AppState.Session import ses
from Models.ModelBase import Base
from Models.Card import Card
from Models.Deck import Deck
from Models.User import User
from AppState.Session import Engine
from passlib.hash import pbkdf2_sha256

Base.metadata.bind = Engine        
Base.metadata.create_all()

def seed():
    if len(ses.query(User).all()) <= 0:
        u1 = User(name="Derrick Heinemann", username="itderrickh", password=pbkdf2_sha256.hash('itderrickh'))
        ses.add(u1)
        ses.commit()
    #d1 = Deck(name="Zoropod", userId=1)
    #c1 = Card(name="Zoroark-GX",count=4,setName="SLG",deckId=1,type="Trainer Cards",number="SM84")
    
    #ses.add(d1)
    #ses.add(c1)
    