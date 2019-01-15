from AppState.Session import ses, ElasticStore
from Models.ModelBase import Base, JSONType
from Models.Card import Card
from Models.Deck import Deck
from Models.DeckCard import DeckCard
from Models.User import User
from Models.CardSet import CardSet
from Models.Event import Event
from Models.UserEvent import UserEvent
from AppState.Session import Engine
from passlib.hash import pbkdf2_sha256
from unidecode import unidecode
from Helpers.DeckLib import get_deck_from_source
from Helpers.SetHelper import getSet
import datetime
import json
import glob
import os

Base.metadata.bind = Engine
Base.metadata.create_all()

def seed():
    if len(ses.query(CardSet).all()) <= 0:
        s1 = CardSet(name="XY - Kalos Starter Set", setName="KSS", standard=False, shortName="Kalos Starter Set", fileName="Kalos Starter Set.json")
        s2 = CardSet(name="XY - XY", setName="XY", standard=False, shortName="XY", fileName="XY.json")
        s3 = CardSet(name="XY - Flashfire", setName="FLF", standard=False, shortName="Flashfire", fileName="Flashfire.json")
        s4 = CardSet(name="XY - Furious Fists", setName="FFI", standard=False, shortName="Furious Fists", fileName="Furious Fists.json")
        s5 = CardSet(name="XY - Phantom Forces", setName="PHF", standard=False, shortName="Phantom Forces", fileName="Phantom Forces.json")
        s6 = CardSet(name="XY - Primal Clash", setName="PRC", standard=False, shortName="Primal Clash", fileName="Primal Clash.json")
        s7 = CardSet(name="XY - Roaring Skies", setName="ROS", standard=False, shortName="Roaring Skies", fileName="Roaring Skies.json")
        s8 = CardSet(name="XY - Ancient Origins", setName="AOR", standard=False, shortName="Ancient Origins", fileName="Ancient Origins.json")
        s9 = CardSet(name="XY - BREAKthrough", setName="BKT", standard=False, shortName="BREAKthrough", fileName="BREAKthrough.json")
        s10 = CardSet(name="XY - BREAKpoint", setName="BKP", standard=False, shortName="BREAKpoint", fileName="BREAKpoint.json")
        s11 = CardSet(name="XY - Fates Collide", setName="FCO", standard=False, shortName="Fates Collide", fileName="Fates Collide.json")
        s12 = CardSet(name="XY - Steam Siege", setName="STS", standard=False, shortName="Steam Siege", fileName="Steam Siege.json")
        s13 = CardSet(name="XY - Double Crisis", setName="DCR", standard=False, shortName="Double Crisis", fileName="Double Crisis.json")
        s41 = CardSet(name="XY - Evolutions", setName="EVO", standard=False, shortName="Evolutions", fileName="Evolutions.json")

        s14 = CardSet(name="XY - Generations", setName="GEN", standard=True, shortName="Generations", fileName="Generations.json")
        #s15 = CardSet(name="XY - XY Trainer Kit", setName="TK", standard=True, shortName="XY Trainer Kit", fileName="XY Trainer Kit.json")
        s16 = CardSet(name="Sun & Moon - Sun & Moon", setName="SUM", standard=True, shortName="Sun & Moon", fileName="Sun & Moon.json")
        s17 = CardSet(name="Sun & Moon - Guardians Rising", setName="GRI", standard=True, shortName="Guardians Rising", fileName="Guardians Rising.json")
        s18 = CardSet(name="Sun & Moon - Burning Shadows", setName="BUS", standard=True, shortName="Burning Shadows", fileName="Burning Shadows.json")
        s19 = CardSet(name="Sun & Moon - Crimson Invasion", setName="CIN", standard=True, shortName="Crimson Invasion", fileName="Crimson Invasion.json")
        s20 = CardSet(name="Sun & Moon - Ultra Prism", setName="UPR", standard=True, shortName="Ultra Prism", fileName="Ultra Prism.json")
        s40 = CardSet(name="Sun & Moon - Forbidden Light", setName="FLI", standard=True, shortName="Forbidden Light", fileName="Forbidden Light.json")
        s42 = CardSet(name="Sun & Moon - Celestial Storm", setName="CES", standard=True, shortName="Celestial Storm", fileName="Celestial Storm.json")
        s43 = CardSet(name="Sun & Moon - Dragon Majesty", setName="DRM", standard=True, shortName="Dragon Majesty", fileName="Dragon Majesty.json")
        s44 = CardSet(name="Sun & Moon - Lost Thunder", setName="LOT", standard=True, shortName="Lost Thunder", fileName="Lost Thunder.json")

        s21 = CardSet(name="Sun & Moon - Shining Legends", setName="SLG", standard=True, shortName="Shining Legends", fileName="Shining Legends.json")
        #s22 = CardSet(name="Sun & Moon Trainer Kit", setName="TK", standard=True, shortName="Sun & Moon Trainer Kit", fileName="Sun & Moon Trainer Kit.json")
        s23 = CardSet(name="Black & White - BW Black Star Promos", setName="PR-BW", standard=False, shortName="BW Black Star Promos", fileName="BW Black Star Promos.json")
        s24 = CardSet(name="XY - XY Black Star Promos", setName="PR-XY", standard=True, shortName="XY Black Star Promos", fileName="XY Black Star Promos.json")
        s26 = CardSet(name="Sun & Moon - SM Black Star Promos", setName="PR-SM", standard=True, shortName="SM Black Star Promos", fileName="Sun & Moon Black Star Promos.json")
        #s27 = CardSet(name="McDonald's Collection", setName="MCD", standard=True, shortName="", fileName="")

        s28 = CardSet(name="Black & White - Legendary Treasures", setName="LTR", standard=False, shortName="Legendary Treasures", fileName="Legendary Treasures.json")
        s29 = CardSet(name="Black & White - Plasma Blast", setName="PLB", standard=False, shortName="Plasma Blast", fileName="Plasma Blast.json")
        s30 = CardSet(name="Black & White - Plasma Freeze", setName="PLF", standard=False, shortName="Plasma Freeze", fileName="Plasma Freeze.json")
        s31 = CardSet(name="Black & White - Plasma Storm", setName="PLS", standard=False, shortName="Plasma Storm", fileName="Plasma Storm.json")
        s32 = CardSet(name="Black & White - Boundaries Crossed", setName="BCR", standard=False, shortName="Boundaries Crossed", fileName="Boundaries Crossed.json")
        s33 = CardSet(name="Black & White - Dragon Vault", setName="DRV", standard=False, shortName="Dragon Vault", fileName="Dragon Vault.json")
        s39 = CardSet(name="Black & White - Dragons Exalted", setName="DRX", standard=False, shortName="Dragons Exaulted", fileName="Dragons Exalted.json")
        s34 = CardSet(name="Black & White - Dark Explorers", setName="DEX", standard=False, shortName="Dark Explorers", fileName="Dark Explorers.json")
        s35 = CardSet(name="Black & White - Next Destinies", setName="NXD", standard=False, shortName="Next Destinies", fileName="Next Destinies.json")
        s36 = CardSet(name="Black & White - Noble Victories", setName="NVI", standard=False, shortName="Noble Victories", fileName="Noble Victories.json")
        s37 = CardSet(name="Black & White - Emerging Powers", setName="EPO", standard=False, shortName="Emerging Powers", fileName="Emerging Powers.json")
        s38 = CardSet(name="Black & White", setName="BLW", standard=False, shortName="Black & White", fileName="Black & White.json")

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
        #ses.add(s15)
        ses.add(s16)
        ses.add(s17)
        ses.add(s18)
        ses.add(s19)
        ses.add(s20)
        ses.add(s21)
        #ses.add(s22)
        ses.add(s23)
        ses.add(s24)
        ses.add(s26)
        #ses.add(s27)
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
        #for item in glob.glob('./Data/json/cards/*'):
        for setList in sets:
            item = "./Data/json/cards/{}".format(setList.fileName)
            print(item)
            with open(item, encoding="utf8") as f:
                data = json.load(f)
                for d in data:
                    card = Card(
                        name=unidecode(d['name'].replace("◇", "Prism Star").replace("{*}", "Prism Star")),
                        subtype=d.get('subtype'),
                        type=d.get('supertype'),
                        evolvesFrom=d.get('evolvesFrom', ''),
                        ability=d.get('ability'),
                        hp=int(d.get('hp') if str(d.get('hp')) != "None" else 0),
                        retreatCost=d.get('convertedRetreatCost'),
                        artist=d['artist'],
                        rarity=d.get('rarity'),
                        setName=d['set'],
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

    if len(ses.query(Deck).all()) <= 0:
        sets = ses.query(CardSet).all()

        for item in glob.glob('./DeckLists/*'):
            base = os.path.basename(item)
            filename = os.path.splitext(base)[0]
            print(filename)
            with open(item, encoding="utf8") as f:
                deck_list = get_deck_from_source(f.read())
                deck = Deck(name=filename, userId=1)

                try:
                    ses.add(deck)
                    ses.flush()

                    for _, value in deck_list.items():
                        if "{*}" in value['card']:
                            value['card'] = value['card'].replace("{*}", "Prism Star")
                        if "◇" in value['card']:
                            value['card'] = value['card'].replace("◇", "Prism Star")
                        if value['type'] == "Energy":
                            if "Energy" not in value['card']:
                                value['card'] += " Energy"
                            card = ses.query(Card).filter(Card.name==value['card']).order_by(Card.Id.desc()).first()
                        else:
                            card = ses.query(Card).filter(Card.name==value['card'], Card.setName==getSet(sets, value['set']), Card.number==value['number']).first()
                        if card is None:
                            cards = ElasticStore.search(index="card-index", body={"size": 1, "query": {"match": { "name": value['card'] }}})
                            card = cards['hits']['hits'][0]['_source']
                        ses.add(DeckCard(deckId=deck.id,cardId=card.Id,count=value['count']))

                    ses.commit()
                except:
                    ses.rollback()
                    raise
