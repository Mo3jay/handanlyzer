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

game_states = {
    "new_game": "new_game",
    "ident_button": "ident_button",
    "deal_cards": "deal_cards",
    "pre_flop": "pre_flop",
    "pre_betting": "pre_betting",
    "deal_flop": "deal_flop",
    "flop_betting": "flop_betting",
    "deal_turn": "deal_turn",
    "deal_river": "deal_river",
    "showdown": "showdown",
}
current_state = game_states["new_game"]

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

for ln in sng:
    if "#Game No" in ln:
        current_state = game_states["new_game"]

        if hand:
            hands.append(hand)
        hand_count += 1
        hand = Hand()
        button = ""
        players = 0
        seats = []

    elif "** " in ln:
        if "Dealing down cards" in ln:
            current_state = game_states["deal_cards"]
        elif "Dealing flop" in ln:
            current_state = game_states["deal_flop"]
        elif "Dealing turn" in ln:
            current_state = game_states["deal_turn"]
        elif "Dealing river" in ln:
            current_state = game_states["deal_river"]
        elif "Summary" in ln:
            current_state = game_states["showdown"]

    elif current_state == game_states["new_game"]:
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

    elif current_state == game_states["deal_cards"]:
        if "Dealt to Moejay1021" in ln:
            start = ln.find("[")
            stop = ln.find("]")
            #formating for hand layout [ 6h, Kc ] = 6h, Kc
            pocket = ln[start + 2:stop - 1]
            hand.set_pocket(pocket)
            current_state = game_states["pre_flop"]       
        
    elif current_state == game_states["pre_flop"]:
        if "Moejay1021" in ln:
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
            action = ln[11:] # remove hero name
            stop = action.find(" ")
            action = action[:stop] # isolate action
            hand.set_first_action(actions[action])
            if action != 'folds':
                hand.hand_was_played()
                hands_played_count += 1
            current_state = game_states["pre_betting"]
    
    elif current_state == game_states["deal_flop"]:
        if "Moejay1021" in ln:
            hand.saw_flop()
            flop_count += 1
            current_state = game_states["flop_betting"]
        
    elif current_state == game_states["showdown"]:
        if "Moejay1021" in ln:
            if "collected" in ln:
                hand.won_hand()
                won_count += 1
            elif "shows" in ln or "muck" in ln:
                hand.went_showdown()
                show_count += 1
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
