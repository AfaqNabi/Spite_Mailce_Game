from lectureStructures import Stack, BoundedQueue
import random


class Card:
    def __init__(self, value):
        '''
        takes in value of the card and assigns the face given the value
        :param value:
        '''
        assert -1 <= value <= 9, 'invalid entry'
        self.value = value
        self.face = str(self.value)
        if self.value == -1:
            self.face = '*'
        else:
            self.face = str(self.value)

    def assign(self, v):
        '''
        reassigns the value of the joker to a given value
        :param value:
        :return:
        '''
        assert -1 <= v <= 9, 'invalid value'
        if 0 <= self.value <= 9 and self.face == '*':
            self.face = '*'
            self.value = v
        if self.value == -1:
            self.value = v
            self.face = '*'

    def getValue(self):
        '''
        gets the value of the card
        :return: value of card
        '''
        return self.value

    def getFace(self):
        '''
        :return: the face of card
        '''
        return self.face

    def __str__(self):
        '''
        :return: string representation of card
        '''
        return '[' + self.face + ']'

    def __repr__(self):
        '''
        :return: representation of the object of this class
        '''
        return '.'+str(self.value)


class PlayStack:
    def __init__(self):
        '''
        initialize empty list
        '''
        self.cards = []

    def peekValue(self):
        '''
        :return: the value at the top of the play stack
        '''
        try:
            if len(self.cards) == 0:
                raise
            return self.cards[len(self.cards) - 1].getValue()
        except:
            return None

    def peekFace(self):
        '''
        :return: the face at the top of the play stack
        '''
        assert len(self.cards) >= 0, 'Error: No cards in the playing stack'
        return str(self.cards[len(self.cards)-1])

    def playCard(self, card):
        '''
        play the given card based on some conditions
        :param card:
        :return:
        '''
        play_stack_list = []

        # try to play card
        try:
            if len(self.cards) == 0:
                assert card.getValue() == 0, 'must play zero on top'
                self.cards.append(card)
            elif self.peekValue()+1 == card.getValue():  # play the appropriate value
                self.cards.append(card)
            else:
                raise
        except Exception:
            print('Error: Card rejected ')
            raise

        # if the value at the top of the stack is 9 clear the stack and return it as a list
        if self.peekValue() == 9:
            for i in self.cards:
                play_stack_list.append(i.getFace())
            self.cards.clear()
        return play_stack_list

    def __str__(self):
        '''
        :return: string representation of the play stack
        '''
        some_string = '|'
        for i in self.cards:
            some_string += str(i)
        return some_string+'|'


class Hand:
    # hand is a list of 5 cards in the players hand
    def __init__(self):
        '''
        hand is a list of 5 cards in the players hand
        '''
        self.hand = []

    def sort1(self):
        '''
        sort the list of cards in hand from lowest to highest
        :return:
        '''
        return self.hand.sort(key=lambda Card: Card.value)

    def pop(self):
        '''
        pops and retuns the last index in the list
        :return:
        '''
        assert len(self.hand) > 0
        return self.hand.pop()

    def pop1(self, pos):
        '''
        pops and returns the card at pos
        :param pos:
        :return: card at pos
        '''
        assert (len(self.hand) > 0) and (type(pos) is type(0)) and (pos < len(self.hand))
        return self.hand.pop(pos)

    def index(self, v):
        '''
        finds the index of the value v
        :param v:
        :return:
        '''
        assert -1 <= v <= 9
        index = 0
        found = False
        while not found and index < len(self.hand):
            if v == self.hand[index].getValue():
                found = True
            index += 1
        if not found:
            index -= 1
        return index

    def check0(self):
        '''
        check for the index of the first card with value 0 in hand
        :return:
        '''
        index = 0
        found = False
        while not found and index<len(self.hand):
            if self.hand[index].getValue() == 0:
                found = True
            index += 1
        if not found:
            index = -1
        return index

    def size(self):
        '''
        returns how many cards in hand
        :return:
        '''
        return len(self.hand)

    def add(self, cardList):
        '''
        adds cards to hand till there are 5 cards in hand
        :param cardList:
        :return:
        '''
        assert len(cardList) < 6, 'too many cards'
        for i in cardList:
            self.hand.append(i)
        for j in range(0,len(cardList)):
            cardList.pop()
        Hand.sort1(self)

    def __str__(self):
        '''
        turns the class object into its tring representtation
        :return: str reprepesentation of object
        '''
        some_string = '['
        for i in self.hand:
            some_string += str(i)
        return some_string + ']'


def shuffle(cardsList):
    '''
    return the shuffled deck of cards
    :param cardsList:
    :return:
    '''
    return random.sample(cardsList,len(cardsList))


def main():
    '''
    test the classes
    :return:
    '''

    deck=[]
    for j in range(0, 10):
        for i in range(0, 1):
            deck.append(Card(j))
    for i in range(0, 5):
        deck.append(Card(-1))
    deck = shuffle(deck)
    hand = Hand()
    # print(deck)
    hand.add(deck)
    # print(deck)
    print(hand)
    hand.sort1()

    # print(x)
    # print(hand.sort1())
    # print(deck1)
    play = PlayStack()
    print(play)

    # print(x)
    print(hand.pop1(0).getFace())
    play.playCard(hand.pop1(0).assign(0))
    play.playCard(hand.pop1(0).assign(1))
    # play.playCard(hand.pop1(0))
    # print(play.peekValue()+1,'ss')
    # play.playCard(hand.pop1(0))
    # play.playCard(hand.pop1(0))
    print(play)
    print(hand)


if __name__ == "__main__":
    main()
