from AppState.Session import ses
from Models.ModelBase import Base
from Models.Card import Card
from Models.Deck import Deck
from Models.DeckCard import DeckCard
from Models.User import User
from Models.CardSet import CardSet
from AppState.Session import Engine
from passlib.hash import pbkdf2_sha256
import datetime
import json
import glob

Base.metadata.bind = Engine
Base.metadata.create_all()

def seed():
    for item in glob.glob('../Data/json/cards/*.json'):
        print('../Data/json/cards/{}'.format(item))
        with open('../Data/json/cards/{}'.format(item)) as f:
            data = json.load(f)
            for d in data:
                ses.add(Card())

            #Do Something with the data

    if len(ses.query(User).all()) <= 0:
        u1 = User(name="Derrick Heinemann", username="itderrickh", password=pbkdf2_sha256.hash('itderrickh'),playerid='2548696',dateofbirth=datetime.date(1993, 9, 14))
        ses.add(u1)

        s1 = CardSet(name="XY - Kalos Starter Set", setName="KSS", standard=False)
        s2 = CardSet(name="XY", setName="XY", standard=False)
        s3 = CardSet(name="XY - Flashfire", setName="FLF", standard=False)
        s4 = CardSet(name="XY - Furious Fists", setName="FFI", standard=False)
        s5 = CardSet(name="XY - Phantom Forces", setName="PHF", standard=False)
        s6 = CardSet(name="XY - Primal Clash", setName="PRC", standard=False)
        s7 = CardSet(name="XY - Roaring Skies", setName="ROS", standard=False)
        s8 = CardSet(name="XY - Ancient Origins", setName="AOR", standard=False)
        s9 = CardSet(name="XY - BREAKthrough", setName="BKT", standard=True)
        s10 = CardSet(name="XY - BREAKpoint", setName="BKP", standard=True)
        s11 = CardSet(name="XY - Fates Collide", setName="FCO", standard=True)
        s12 = CardSet(name="XY - Steam Seige", setName="STS", standard=True)
        s13 = CardSet(name="Double Crisis", setName="DCR", standard=True)

        s14 = CardSet(name="Generations", setName="GEN", standard=True)
        s15 = CardSet(name="XY Trainer Kit", setName="TK", standard=True)
        s16 = CardSet(name="Sun & Moon", setName="SUM", standard=True)
        s17 = CardSet(name="Sun & Moon - Guardians Rising", setName="GRI", standard=True)
        s18 = CardSet(name="Sun & Moon - Burning Shadows", setName="BUS", standard=True)
        s19 = CardSet(name="Sun & Moon - Crimson Invasion", setName="CIN", standard=True)
        s20 = CardSet(name="Sun & Moon - Ultra Prism", setName="UPR", standard=True)

        s21 = CardSet(name="Shining Legends", setName="SLG", standard=True)
        s22 = CardSet(name="Sun & Moon Trainer Kit", setName="TK", standard=True)
        s23 = CardSet(name="Black Star Promos BW01 and higher", setName="PR-BW", standard=False)
        s24 = CardSet(name="Black Star Promos XY01-XY66", setName="PR-XY", standard=False)
        s25 = CardSet(name="Black Star Promos XY67 and higher", setName="PR-XY", standard=True)
        s26 = CardSet(name="Black Star Promos SM01 and higher", setName="PR-SM", standard=True)
        s27 = CardSet(name="McDonald's Collection", setName="MCD", standard=True)

        s28 = CardSet(name="Black & White - Legendary Treasures", setName="LTR", standard=False)
        s29 = CardSet(name="Black & White - Plasma Blast", setName="PLB", standard=False)
        s30 = CardSet(name="Black & White - Plasma Freeze", setName="PLF", standard=False)
        s31 = CardSet(name="Black & White - Plasma Storm", setName="PLS", standard=False)
        s32 = CardSet(name="Black & White - Boundaries Crossed", setName="BCR", standard=False)
        s33 = CardSet(name="Black & White - Dragon Vault", setName="DRV", standard=False)
        s39 = CardSet(name="Black & White - Dragons Exaulted", setName="DRX", standard=False)
        s34 = CardSet(name="Black & White - Dark Explorers", setName="DEX", standard=False)
        s35 = CardSet(name="Black & White - Next Destinies", setName="NXD", standard=False)
        s36 = CardSet(name="Black & White - Noble Victories", setName="NVI", standard=False)
        s37 = CardSet(name="Black & White - Emerging Powers", setName="EPO", standard=False)
        s38 = CardSet(name="Black & White", setName="BLW", standard=False)

        ses.add(s1)
        ses.add(s2)
        ses.add(s3)
        ses.add(s4)
        ses.add(s5)
        ses.add(s6)
        ses.add(s7)
        ses.add(s8)
        ses.add(s9)
        ses.add(s10)
        ses.add(s11)
        ses.add(s12)
        ses.add(s13)
        ses.add(s14)
        ses.add(s15)
        ses.add(s16)
        ses.add(s17)
        ses.add(s18)
        ses.add(s19)
        ses.add(s20)
        ses.add(s21)
        ses.add(s22)
        ses.add(s23)
        ses.add(s24)
        ses.add(s25)
        ses.add(s26)
        ses.add(s27)
        ses.add(s28)
        ses.add(s29)
        ses.add(s30)
        ses.add(s31)
        ses.add(s32)
        ses.add(s33)
        ses.add(s34)
        ses.add(s35)
        ses.add(s36)
        ses.add(s37)
        ses.add(s38)
        ses.add(s39)

        ses.commit()


    #d1 = Deck(name="Zoropod", userId=1)
    #c1 = Card(name="Zoroark-GX",count=4,setName="SLG",deckId=1,type="Trainer Cards",number="SM84")

    #ses.add(d1)
    #ses.add(c1)
