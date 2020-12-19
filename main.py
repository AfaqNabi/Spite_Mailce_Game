from SpiteAndMalice import Card, PlayStack, Hand, shuffle
from lectureStructures import Stack, CircularQueue


class Error(Exception):
    '''
    used to raise exceptions
    '''
    pass


class MustPlayZero(Error):
    '''
    this is used to define exceptions so that they
    can be called and caught
    '''
    pass


class Game:
    def __init__(self):
        '''
        initialize all game attributes
        '''
        # game players
        self.player1 = 'PlayerA'
        self.player2 = 'PlayerB'
        self.shoe = CircularQueue(120)  # card shoe
        self.deck = []
        self.turn = ''

        # make the playing stacks
        self.p1 = PlayStack()
        self.p2 = PlayStack()
        self.p3 = PlayStack()
        self.p4 = PlayStack()

        # goal piles
        self.PA_goal = Stack()
        self.PB_goal = Stack()

        # make discard piles
        self.discard_PA1 = Stack()
        self.discard_PA2 = Stack()
        self.discard_PA3 = Stack()
        self.discard_PA4 = Stack()
        self.discard_PB1 = Stack()
        self.discard_PB2 = Stack()
        self.discard_PB3 = Stack()
        self.discard_PB4 = Stack()

        # hand stacks
        self.PA_hand = Hand()
        self.PB_hand = Hand()

        # temporary list to store cleared cards from playing stacks
        self.cleared_play_stacks = []

    def first_turn(self):
        '''
        used to decide which player goes first
        this is based on which ever has the card with the higher value on
        the top of their respective goal stack
        :return: either player 1 or player 2
        '''
        # account for the joker if it is in the top
        if (self.PA_goal.peek().getValue() == -1) and (self.PB_goal.peek().getValue() != -1):
            return self.player1
        elif (self.PA_goal.peek().getValue() != -1) and (self.PB_goal.peek().getValue() == -1):
            return self.player2
        if self.PA_goal.peek().getValue() == self.PB_goal.peek().getValue():
            return self.player1
        elif self.PA_goal.peek().getValue() > self.PB_goal.peek().getValue():
            return self.player1
        elif self.PA_goal.peek().getValue() < self.PB_goal.peek().getValue():
            return self.player2

    def changeTurn(self):
        '''
        used to switch turns between players
        :return: turn of player
        '''
        # change player turn on some conditions
        if self.turn == 'PlayerA':
            self.PB_hand.add(self.replenish_cards(self.PB_hand, self.shoe))
            return self.player2
        elif self.turn == 'PlayerB':
            self.PA_hand.add(self.replenish_cards(self.PA_hand, self.shoe))
            return self.player1

    def deck_of_cards(self):
        '''
        creates the deck of cards with 120 cards
        shuffles the cards
        :return: shuffled deck
        '''
        # initialize 120 cards with 20 jokers
        # and 100 of the cards are numbered 0-9
        # the value is the integer and the face is a string to be printed
        for j in range(0, 10):
            for i in range(0, 10):
                self.deck.append(Card(j))
        for i in range(0, 20):
            self.deck.append(Card(-1))
        deck1 = shuffle(self.deck)
        for i in deck1:
            self.shoe.enqueue(i)

    def deal_cards(self):
        '''
        deal the cards to the goal pile of each player
        they each get 15 from the shuffled deck
        each player gets 5 cards in hand
        :param some_list:
        :return:
        '''
        # deal cards to players and remove cards from shoe
        for i in range(0, 15):
            self.PA_goal.push(self.shoe.dequeue())
        for i in range(0, 15):
            self.PB_goal.push(self.shoe.dequeue())
        playerA = []  # temp list
        playerB = []  # temp list
        for i in range(0, 5):
            playerA.append(self.shoe.dequeue())
        self.PA_hand.add(playerA)
        for i in range(0, 5):
            playerB.append(self.shoe.dequeue())
        self.PB_hand.add(playerB)
        # decide turn
        self.turn = self.first_turn()

    def assign_joker(self, card, playing_stack):
        '''
        takes in the playing stack and the card
        checks if the card is a wild card and assigns the appropriate value
        :param card:
        :param playing_stack:
        :return: card object
        '''
        if self.check_empty_stacks() and self.PA_hand.check0() != -1 and self.turn == self.player1:
            return card
        elif self.check_empty_stacks() and self.PB_hand.check0() != -1 and self.turn == self.player2:
            return card
        if playing_stack.peekValue() == None:
            number = 0
        else:
            number = playing_stack.peekValue() + 1
        if card.getValue() == -1:
            card.assign(number)
        return card

    def find_playing_stack(self, number):
        '''
        used to find common playing stack
        decides which playing stack the user has picked
        :param number:
        :return: playing stack
        '''
        if number == 1:
            return self.p1
        elif number == 2:
            return self.p2
        elif number == 3:
            return self.p3
        elif number == 4:
            return self.p4

    def find_discard_pile(self, number):
        '''
        finds the common discard stack
        used to return the discard stack the player has choosed
        :param number:
        :return: discard stack
        '''
        if self.turn == self.player1:
            if number == 1:
                return self.discard_PA1
            elif number == 2:
                return self.discard_PA2
            elif number == 3:
                return self.discard_PA3
            elif number == 4:
                return self.discard_PA4
        elif self.turn == self.player2:
            if number == 1:
                return self.discard_PB1
            elif number == 2:
                return self.discard_PB2
            elif number == 3:
                return self.discard_PB3
            elif number == 4:
                return self.discard_PB4

    def check_empty_stacks(self):
        '''
        used to check if any stacks are empty
        used to determine if the zero in  hand must be played or not
        :return: True if a playing stack is empty
        '''
        if self.p1.peekValue() is None:
            return True
        elif self.p2.peekValue() is None:
            return True
        elif self.p3.peekValue() is None:
            return True
        elif self.p4.peekValue() is None:
            return True
        return False

    def check_zeros_in_hand(self, hand):
        '''
        check if all cards in hand are zeros
        :param hand:
        :return: Bool if all cards in hand are zero
        '''
        temp_list = []
        for i in str(hand):
            temp_list.append(i)
        zeros = temp_list.count('0')
        return zeros == hand.size()

    def update(self, action, position, play_stack):
        '''
        updates the game board based on various conditions
        :param action:
        :param position:
        :param play_stack:
        :return:
        '''
        # assign the hand and goal of the player whose turn it is to go
        hand = None
        goal = None
        if self.turn == self.player1:
            hand = self.PA_hand
            goal = self.PA_goal
        elif self.turn == self.player2:
            hand = self.PB_hand
            goal = self.PB_goal

        # find the playing stack if needed
        common_stack = self.find_playing_stack(play_stack)

        # find the discard stack if needed
        discard = None
        if position[0] == 'd':
            discard = self.find_discard_pile(int(position[1]))
        elif action == 'x':
            discard = self.find_discard_pile(play_stack)

        # if play mode
        if action == 'p':
            card_from_hand = None  # to prevent popping multiple times

            # if playing from hand
            if position[0] == 'h':  # playing from hand
                card_from_hand = hand.pop1(int(position[1]) - 1)
                card = self.assign_joker(card_from_hand, common_stack)
                try:
                    # check if any zeros in hand and any empty playing stacks
                    if self.check_empty_stacks() and hand.check0() != -1:
                        if card_from_hand.getValue() != 0:
                            raise MustPlayZero
                    try:
                        # try to play the card
                        temp = common_stack.playCard(card)
                        self.clear_play_stack(temp)
                    except:
                        # if exception raised put card back in hand
                        temp_list = [card]
                        hand.add(temp_list)
                except MustPlayZero:
                    # if exception raised put card back in hand
                    temp_list = [card]
                    hand.add(temp_list)
                    print('must play zero')

            # if playing from goal pile
            elif position[0] == 'g':
                card_from_goal = goal.pop()  # remove from goal pile
                card = self.assign_joker(card_from_goal, common_stack)  # check if joker

                # try to play card
                try:
                    temp = common_stack.playCard(card)
                    self.clear_play_stack(temp)
                except Exception:
                    # if exception is caught return card to goal
                    goal.push(card)
                try:
                    # reveal whatever card is on top of the goal pile
                    return goal.peek()
                except:
                    # incase the goal pile is empty
                    pass

            # if playing from the discard pile
            elif position[0] == 'd':
                card_from_discard = None
                # try to pop from the discard stack
                try:
                    card_from_discard = discard.pop()
                except:
                    # if the stack is empty
                    print('discard stack is empty please choose another')
                try:
                    card = self.assign_joker(card_from_discard, common_stack)
                    temp = common_stack.playCard(card)
                    self.clear_play_stack(temp)
                except Exception:
                    discard.push(card_from_discard)
            if hand.size() == 0:
                hand.add(self.replenish_cards(hand, self.shoe))

        # discard mode
        elif action == 'x':  # must be discarded from hand
            card = hand.pop1(int(position[1]) - 1)  # pop card from hand
            # try to push card unless it is zero
            try:
                if card.getValue() != 0:
                    discard.push(card)
                    self.turn = self.changeTurn()
                else:
                    raise
            except:
                # if exception is caught return card to playing stack
                temp_list = [card]
                hand.add(temp_list)
                print('cannot discard zeros')

        # If only zeros in hand and no other legal moves so turn is switched
        if (self.check_zeros_in_hand(self.PA_hand)) and (self.turn == self.player1) and (
                self.check_empty_stacks() == False):
            self.turn = self.changeTurn()
        elif (self.check_zeros_in_hand(self.PB_hand)) and (self.turn == self.player2) and (
                self.check_empty_stacks() == False):
            self.turn = self.changeTurn()

    def clear_play_stack(self, play_stack_list):
        '''
        takes in the list returned from the playCard class
        pnce 5 playing stacks have been cleared the cards are shuffled
        the 50 cards are then enqueued to the shoe
        :param play_stack_list:
        :return:
        '''
        if len(play_stack_list) == 10:
            for i in play_stack_list:
                if i == '*':
                    self.cleared_play_stacks.append(Card(-1))
                else:
                    self.cleared_play_stacks.append(Card(int(i)))

        # enqueue once the list reaches 50
        if len(self.cleared_play_stacks) == 50:
            temp_list = shuffle(self.cleared_play_stacks)
            for i in temp_list:
                self.shoe.enqueue(i)
            temp_list.clear()
            self.cleared_play_stacks.clear()

    def draw_game_board(self):
        '''
        draw the game board
        :return:
        '''
        print('----------------------------------------')
        print(self.player1 + ' Hand ' + str(self.PA_hand))
        print(self.player1 + ' Discard 1: ' + str(self.discard_PA1))
        print(self.player1 + ' Discard 2: ' + str(self.discard_PA2))
        print(self.player1 + ' Discard 3: ' + str(self.discard_PA3))
        print(self.player1 + ' Discard 4: ' + str(self.discard_PA4))
        print(self.player1 + ' Goal ' + str(self.PA_goal.peek()) + ' ' + str(self.PA_goal.size()) + ' cards left', '\n')
        print('Play Stack 1 : ' + str(self.p1))
        print('Play Stack 2 : ' + str(self.p2))
        print('Play Stack 3 : ' + str(self.p3))
        print('Play Stack 4 : ' + str(self.p4), '\n')
        print(self.player2 + ' PlayerB Hand ' + str(self.PB_hand))
        print(self.player2 + ' Discard 1: ' + str(self.discard_PB1))
        print(self.player2 + ' Discard 2: ' + str(self.discard_PB2))
        print(self.player2 + ' Discard 3: ' + str(self.discard_PB3))
        print(self.player2 + ' Discard 4: ' + str(self.discard_PB4))
        print(self.player2 + ' Goal ' + str(self.PB_goal.peek()) + ' ' + str(self.PB_goal.size()) + ' cards left')
        print('----------------------------------------')

    def replenish_cards(self, hand, cards):
        '''
        puts the players cards back up to five
        :return:
        '''
        temp_list = []
        for i in range(0, 5 - hand.size()):
            temp_list.append(cards.dequeue())
        return temp_list


def main():
    '''
    main game
    all the main parts of the game occur here
    :return:
    '''
    game = Game()  # initialize game
    game.deck_of_cards()  # make the deck of cards
    game.deal_cards()  # deal cards to players
    GameOver = False  # game condition
    turn = None

    # main game loop
    while not GameOver:
        turn = game.turn
        game.draw_game_board()
        action = ' '
        position = ''
        play_stack = -1
        hand_size = ''
        hand_size_full = ''

        # assign the list of valid inputs for each player
        if turn == 'PlayerA':
            hand_size = ['h' + str(i) for i in range(1, game.PA_hand.size() + 1)]
            hand_size_full = hand_size + ['g', 'd1', 'd2', 'd3', 'd4']
        elif turn == 'PlayerB':
            hand_size = ['h' + str(i) for i in range(1, game.PB_hand.size() + 1)]
            hand_size_full = hand_size + ['g', 'd1', 'd2', 'd3', 'd4']

        # prompt user for input
        while action.lower() not in ['p', 'x']:  # prevent crashing with invalid input
            action = str(input(turn + ', choose action: p (play) or x (discard/end turn) \n'))

        if action == 'p':
            while position[0:2].lower() not in hand_size_full:  # prevent crashing with invalid input
                position = str(input('Play from where: hi = hand at position i (1..5); g = goal; dj = '
                                     'discard pile j (1..4)?\n'))
            while play_stack not in ['1', '2', '3', '4']:  # prevent crashing with invalid input
                play_stack = str(input('Which Play Stack are you targeting (1..4)?\n'))
            game.update(action, position, int(play_stack))

        elif action == 'x':
            while position[0:2].lower() not in hand_size:
                position = str(input('Play from where: hi = hand at position i (1..5) \n'))
            while play_stack not in ['1', '2', '3', '4']:  # prevent crashing with invalid input
                play_stack = str(input('Which discard pile are you targeting (1..4)?\n'))
            game.update(action, position, int(play_stack))

        # game over coniditon
        if game.PA_goal.size() == 0 or game.PB_goal.size() == 0:
            GameOver = True
    print('congragts' + turn + ' wins')


if __name__ == "__main__":
    main()
