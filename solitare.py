#yo toby i gonna make my own solitare cause 
# computer vision is killing me

#made some classes for some of the parts of the game
#no actual game play
#i think the stock and waste might be wrong
#as i not sure how the draw 3 logic works
import random

class Card:
    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank
        self.face_up = False

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def output_deck(self):
        return self.cards
    
class Tableau: #this is the 7 colums
    def __init__(self):
        self.columns = [[] for _ in range(7)]

    def add_card(self, card, column):
        self.columns[column].append(card)

    def remove_card(self, column):
        return self.columns[column].pop()

    def get_top_card(self, column):
        return self.columns[column][-1] if self.columns[column] else None

    def is_empty(self, column):
        return len(self.columns[column]) == 0

class Foundation:#this is where aces go
    def __init__(self):
        self.piles = {suit: [] for suit in Deck.suits}

    def add_card(self, card):
        self.piles[card.suit].append(card)

    def can_add_card(self, card):
        if not self.piles[card.suit]:
            return card.rank == 'Ace'
        top_card = self.piles[card.suit][-1]
        return Deck.ranks.index(card.rank) == Deck.ranks.index(top_card.rank) + 1

class Stock:
    def __init__(self, deck):
        self.cards = deck.cards

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def is_empty(self):
        return len(self.cards) == 0

    def refill_from_waste(self, waste):
        self.cards = waste.cards[::-1]  # Reverse the waste pile to maintain order
        waste.cards.clear()

class Waste:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        return self.cards.pop() if self.cards else None

    def top_card(self):
        return self.cards[-1] if self.cards else None

    def is_empty(self):
        return len(self.cards) == 0



deck=Deck()
print(deck.output_deck())