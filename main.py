class Hand():
    def __init__(self):
        self.pocket = ""
        self.flop = False
        self.showdown = False
        self.won = False
        self.position = 0
        self.first_action = ""
        self.hand_played = False

    def set_pocket(self, cards):
        self.pocket = cards

    def saw_flop(self):
        self.flop = True

    def went_showdown(self):
        self.showdown = True

    def won_hand(self):
        self.won = True

    def set_position(self, position):
        self.position = position

    def set_first_action(self, action):
        self.first_action = action

    def hand_was_played(self):
        self.hand_played = True

positions = {
    0: "button",
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
}

actions = { #lookup for hand actions formatting
    'folds': 'fold',
    'checks': 'check',
    'calls': 'call',
    'raises': 'raise',
    'did': 'won without actions'
}

seats = []
button = ""
players = 0

sng = open("hand.txt", "r")
hand_count = 0
hands_played_count = 0
flop_count = 0
show_count = 0
won_count = 0
hands = []
hand = None
cards_dealt = False
flop_dealt = False
showdown = False

for ln in sng:
    if "#Game No" in ln:
        if hand:
            hands.append(hand)
        hand_count += 1
        hand = Hand()
        cards_dealt = False
        showdown = False
        flop_dealt = False
        button = ""
        players = 0
        seats = []

    if "Seat" in ln:
        if "button" in ln:
            button = ln[:6]
        else:
            stop = ln.find(" ", 8)
            name = ln[:stop]
            seats.append(name)
            if len(seats) == players:
                while button not in seats[0]:
                    seats.append(seats.pop(0))
                for i, player in enumerate(seats):
                    if "Moejay1021" in player:
                        hand.set_position(positions[i])

    if "players" in ln:
        players = int(ln[-2])

    if cards_dealt and "Moejay1021" in ln:
        '''
        Find if hero played in this hand
        Only want the first action the hero makes
        Possible values of ln: ($ amounts are arbitrary)
        Moejay1021 folds
        Moejay1021 raises [$60]
        Moejay1021 checks
        Moejay1021 calls [$150]
        Moejay1021 did not show his hand

        That last option is only when hero is big blind
        all other players fold to big blind
        hero wins the hand without taking any actions
        the first occurance of the name is in ** Summary **
        '''
        cards_dealt = False
        action = ln[11:] # remove hero name
        stop = action.find(" ")
        action = action[:stop] # isolate action
        hand.set_first_action(actions[action])
        if action != 'folds':
            hand.hand_was_played()
            hands_played_count += 1

    if "Dealt to Moejay1021" in ln:
        start = ln.find("[")
        stop = ln.find("]")
        #formating for hand layout [ 6h, Kc ] = 6h, Kc
        pocket = ln[start + 2:stop - 1]
        hand.set_pocket(pocket)
        cards_dealt = True

    if "Dealing flop" in ln:
        flop_dealt = True

    if flop_dealt and "Moejay1021" in ln and not hand.flop:
        hand.saw_flop()
        flop_count += 1

    if "shows" in ln:
        showdown = True

    if showdown and "Moejay1021" in ln and not hand.showdown:
        hand.went_showdown()
        show_count += 1

    if "Moejay1021 collected" in ln:
        hand.won_hand()
        won_count += 1
hands.append(hand)

for hand in hands:
    print("position:", hand.position)
    print("dealt:", hand.pocket)
    print("played hand:", hand.hand_played)
    print("first action:", hand.first_action)
    print("saw flop:", hand.flop)
    print("showdown:", hand.showdown)
    print("won:", hand.won)

print("hands dealt:", hand_count)
print("hands played:", hands_played_count)
print("hands flopped:", flop_count)
print("saw showdown:", show_count)
print("hands won:", won_count)
