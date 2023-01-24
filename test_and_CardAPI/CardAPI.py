from fastapi import FastAPI
from collections import namedtuple
from random import shuffle

app = FastAPI()


def generate_deck(count):
    Card = namedtuple('Card', ['rank', 'suit'])
    card_deck = [Card(rank, suit) for rank in [str(i) for i in range(2, 11)] + [x for x in 'JQKA']
                                  for suit in ['HEART', 'CLUBS', 'SPADE', 'DIAMOND']]
    shuffle(card_deck)
    card_list = []
    for i in range(count):
        card_list.append(card_deck[i])
    return card_list


@app.get('/cardsAPI/{count}')
async def random_cards(count: int):
    response = {
        'cards': {
        }
    }
    if count > 52:
        response['cards'] = 'В колоде 0-51 карта !!!'
        return response
    cards = generate_deck(count)
    for i in range(len(cards)):
        response['cards'][i] = cards[i]
    return response


@app.get('/help')
async def help():
    response = {
        '127.0.0.1:8000/cardsAPI/<<count>>': 'взять случайное количество перетасованных карт'
    }
    return response
