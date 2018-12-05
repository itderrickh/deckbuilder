from AppState.Session import ses, ElasticStore
from Models.ModelBase import Base, JSONType
from Models.Card import Card
from Models.Deck import Deck
from Models.DeckCard import DeckCard
from Models.User import User
from Models.CardSet import CardSet
from Models.Event import Event
from AppState.Session import Engine
from passlib.hash import pbkdf2_sha256
import datetime
import json
import glob

Base.metadata.bind = Engine
Base.metadata.create_all()

def getSet(sets, setName):
	return next((s.setName for s in sets if s.name == setName), "")

def seed():
    if len(ses.query(CardSet).all()) <= 0:
        s1 = CardSet(name="XY - Kalos Starter Set", setName="KSS", standard=False)
        s2 = CardSet(name="XY - XY", setName="XY", standard=False)
        s3 = CardSet(name="XY - Flashfire", setName="FLF", standard=False)
        s4 = CardSet(name="XY - Furious Fists", setName="FFI", standard=False)
        s5 = CardSet(name="XY - Phantom Forces", setName="PHF", standard=False)
        s6 = CardSet(name="XY - Primal Clash", setName="PRC", standard=False)
        s7 = CardSet(name="XY - Roaring Skies", setName="ROS", standard=False)
        s8 = CardSet(name="XY - Ancient Origins", setName="AOR", standard=False)
        s9 = CardSet(name="XY - BREAKthrough", setName="BKT", standard=False)
        s10 = CardSet(name="XY - BREAKpoint", setName="BKP", standard=False)
        s11 = CardSet(name="XY - Fates Collide", setName="FCO", standard=False)
        s12 = CardSet(name="XY - Steam Seige", setName="STS", standard=False)
        s13 = CardSet(name="XY - Double Crisis", setName="DCR", standard=False)
        s41 = CardSet(name="XY - Evolutions", setName="EVO", standard=False)

        s14 = CardSet(name="XY - Generations", setName="GEN", standard=True)
        s15 = CardSet(name="XY - XY Trainer Kit", setName="TK", standard=True)
        s16 = CardSet(name="Sun & Moon - Sun & Moon", setName="SUM", standard=True)
        s17 = CardSet(name="Sun & Moon - Guardians Rising", setName="GRI", standard=True)
        s18 = CardSet(name="Sun & Moon - Burning Shadows", setName="BUS", standard=True)
        s19 = CardSet(name="Sun & Moon - Crimson Invasion", setName="CIN", standard=True)
        s20 = CardSet(name="Sun & Moon - Ultra Prism", setName="UPR", standard=True)
        s40 = CardSet(name="Sun & Moon - Forbidden Light", setName="FLI", standard=True)
        s42 = CardSet(name="Sun & Moon - Celestial Storm", setName="CES", standard=True)
        s43 = CardSet(name="Sun & Moon - Dragon Majesty", setName="DRM", standard=True)
        s44 = CardSet(name="Sun & Moon - Lost Thunder", setName="LOT", standard=True)

        s21 = CardSet(name="Sun & Moon - Shining Legends", setName="SLG", standard=True)
        s22 = CardSet(name="Sun & Moon Trainer Kit", setName="TK", standard=True)
        s23 = CardSet(name="Black & White - BW Black Star Promos", setName="PR-BW", standard=False)
        s24 = CardSet(name="XY - XY Black Star Promos", setName="PR-XY", standard=True)
        s26 = CardSet(name="Sun & Moon - SM Black Star Promos", setName="PR-SM", standard=True)
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
        ses.add(s40)
        ses.add(s41)
        ses.add(s42)
        ses.add(s43)
        ses.add(s44)
        ses.commit()

    sets = ses.query(CardSet).all()

    if(len(ses.query(Card).all()) <= 0):
        ElasticStore.indices.delete(index='card-index')
        for item in glob.glob('./Data/json/cards/*'):
            print(item)
            with open(item, encoding="utf8") as f:
                data = json.load(f)
                for d in data:
                    card = Card(
                        name=d['name'].replace("◇", "Prism Star").replace("{*}", "Prism Star"),
                        subtype=d.get('subtype'),
                        type=d.get('supertype'),
                        evolvesFrom=d.get('evolvesFrom', ''),
                        ability=d.get('ability'),
                        hp=int(d.get('hp') if str(d.get('hp')) != "None" else 0),
                        retreatCost=d.get('convertedRetreatCost'),
                        artist=d['artist'],
                        rarity=d.get('rarity'),
                        setName=d['series'] + " - " + d['set'],
                        setCode=d['setCode'],
                        types=d.get('types'),
                        localImageUrl="/" + d['setCode'] + "/" + d.get('number') + ".png",
                        imageUrl=d.get('imageUrl'),
                        attacks=d.get('attacks'),
                        weaknesses=d.get('weaknesses'),
                        number=d['number'])
                    ses.add(card)
                    ses.flush()
                    ElasticStore.index(index="card-index", doc_type='card', id=card.Id, body=card.serialize())
        ses.commit()

    if len(ses.query(User).all()) <= 0:
        u1 = User(
            name="Derrick Heinemann",
            username="itderrickh",
            password=pbkdf2_sha256.hash('itderrickh'),
            playerid='2548696',
            dateofbirth=datetime.date(1993, 9, 14),
            zipCode='54904',
            theme="darkly"
        )
        ses.add(u1)

        ses.commit()
