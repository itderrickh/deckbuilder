import os
from AppState.Session import ses
from Models.Card import Card
from Models.CardSet import CardSet

def getSet(sets, setName):
	return next((" " + s.setName for s in sets if s.name == setName), "")

def get_shared_decklist(deck_one, deck_two):
	''' Takes two deck lists and combines them to the minimum '''
	shared = dict()
	deck_one_dict = dict()
	deck_two_dict = dict()
	sets = ses.query(CardSet).all()

	deck_one_cards = [x.name + getSet(sets, x.setName) for x in deck_one]
	deck_two_cards = [x.name + getSet(sets, x.setName) for x in deck_two]
	# Store all the cards in the decks
	all_props = list(set(deck_one_cards) | set(deck_two_cards))

	# Go through all the properties
	for prop in all_props:
		cards_in_deck_one = [x for x in deck_one if x.name + getSet(sets, x.setName) == prop]
		cards_in_deck_two = [y for y in deck_two if y.name + getSet(sets, y.setName) == prop]
		# Adjust the two decks and the shared decks accordingly
		if len(cards_in_deck_one) > 0 and len(cards_in_deck_two) > 0:
			min_val = min(cards_in_deck_one[0].count, cards_in_deck_two[0].count)
			shared[prop] = min_val
			deck_one_dict[prop] = cards_in_deck_one[0].count - min_val
			deck_two_dict[prop] = cards_in_deck_two[0].count - min_val
		elif len(cards_in_deck_one) > 0:
			deck_one_dict[prop] = cards_in_deck_one[0].count
		elif len(cards_in_deck_two) > 0:
			deck_two_dict[prop] = cards_in_deck_two[0].count
	return shared, deck_one_dict, deck_two_dict

def print_deck(deck):
    ''' Print the decks with only cards that have values to the console '''
    for key, value in deck.items():
        if value > 0:
            print(key + " " + str(value))
