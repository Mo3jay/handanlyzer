class Hand():
    def __init__(self):
        self.pocket = ""
        self.flop = False
        self.showdown = False
        self.won = False
        

    def set_pocket(self, cards):
        self.pocket = cards

    def saw_flop(self):
        self.flop = True

    def went_showdown(self):
        self.showdown = True

    def won_hand(self):
        self.won = True

sng = open("hand.txt", "r")
hand_count = 0
flop_count = 0
show_count = 0
won_count = 0
hands = []
hand = None
flop_dealt = False
showdown = False

for ln in sng:
    if "#Game No" in ln:
        if hand:
            hands.append(hand)
        hand_count += 1
        hand = Hand()
        showdown = False
        flop_dealt = False
        

    if "Dealt to Moejay1021" in ln:
        start = ln.find("[")
        stop = ln.find("]")
        #formating for hand layout [ 6h, Kc ] = 6h, Kc
        pocket = ln[start + 2:stop - 1]
        hand.set_pocket(pocket)

    if "Dealing flop" in ln:
        flop_dealt = True

    if flop_dealt and "Moejay1021" in ln:
        hand.saw_flop()
        flop_count += 1
        flop_dealt = False

    if "shows" in ln:
        showdown = True

    if showdown and "Moejay1021" in ln:
        hand.went_showdown()
        show_count += 1
        showdown = False

    if "Moejay1021 collected" in ln:
        hand.won_hand()
        won_count += 1
hands.append(hand)

for hand in hands:
    print(hand.pocket)
    print(hand.flop)
    print(hand.won)
    print(hand.showdown)

print("hands played:", hand_count)
print("hands flopped:", flop_count)
print("saw showdown:", show_count)
print("hands won:", won_count)
