import random

class MarketMaker:
    def __init__(self, sides, rolls, players):
        self.sides = sides
        self.rolls_left = rolls
        self.players = players
        self.total = 0

    def make_markets(self):
        markets = {}
        for player in self.players:
            market = player.make_market(self.sides, self.rolls_left, self.total)
            markets[player] = market
            print(f"Player: {player.name} makes the following market {market}")
        
        self.match_markets(markets)
        self.roll_dice()
        self.final_markets()

    
    def match_markets(self, markets):
        for player1 in markets:
            for player2 in markets:
                if player1.name != player2.name:
                    _, ask1 = markets[player1]
                    bid2, _ = markets[player2]
                    if ask1 < bid2:
                        # player 1 sells to player 2
                        player1.shares -= 1
                        player2.shares += 1
                        player1.money += bid2
                        player2.money -= bid2
                        print(f"{player1.name} sold 1 share to {player2.name} at {bid2}")
    
    def roll_dice(self):
        rigged_player_exists = False
        for player in self.players:
            if type(player) == rigged_player:
                num = player.nextroll
                rigged_player_exists = True
            if type(player) == rigged_player2:
                self.sides = player.sides
                rigged_player_exists = False
        if not rigged_player_exists:
            num = random.randint(1, self.sides)
        num = random.randint(1, self.sides)
        self.total += num
        self.rolls_left -= 1
        print(f"Rolled a {num} for a total of {self.total}")

    def final_markets(self):
        # makes everyone buy back / sell shares
        for player in self.players:
            if player.shares > 0:
                player.money += player.shares * self.total
                player.shares = 0
            elif player.shares < 0:
                player.money += player.shares * self.total
                player.shares = 0
            print(f"{player.name} has ${player.money}")

class smart_player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.shares = 0
    
    def make_market(self, sides, rolls_left, total):
        ev = ((sides+1)*(sides)/2/sides) * rolls_left + total
        stdev = sides/4*rolls_left
        return (ev-stdev, ev+stdev)
    
class bad_player:
    # low market
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.shares = 0
    
    def make_market(self, rolls_left, total):
        return (rolls_left + total, rolls_left + total)
    
class bad_player2:
    # high market
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.shares = 0
    
    def make_market(self, sides, rolls_left, total):
        return (rolls_left * sides+ total, rolls_left * sides + total)
    
class human_player:
    def __init__(self, name) -> None:
        self.name = name
        self.money = 0
        self.shares = 0
    
    def make_market(self, sides, rolls_left, total):
        bid = int(input("Enter your bid: "))
        ask = int(input("Enter your ask: "))
        return (bid, ask)
    
class rigged_player:
    def __init__(self, name) -> None:
        self.name = name
        self.money = 0
        self.shares = 0
        self.nextroll = 1
    
    def make_market(self, sides, rolls_left, total):
        print("Number of rolls left: ", rolls_left)
        print("Total: ", total)
        print("Number of sides: ", sides)
        bid = int(input("Enter your bid: "))
        ask = int(input("Enter your ask: "))
        return (bid, ask)
    
    def roll_dice(self, sides):
        self.nextroll = int(input(f"Enter your roll within the range (1-{sides}): "))
        return self.nextroll
    
class rigged_player2:
    def __init__(self, name) -> None:
        self.name = name
        self.money = 0
        self.shares = 0
        self.sides = 6
    
    def make_market(self, sides, rolls_left, total):
        self.sides = self.change_sides(sides)
        print("Number of rolls left: ", rolls_left)
        print("Total: ", total)
        print()
        bid = int(input("Enter your bid: "))
        ask = int(input("Enter your ask: "))
        return (bid, ask)
    
    def change_sides(self, sides):
        self.sides = int(input(f"Enter your new number of sides and old: {sides}: "))
        return self.sides

if __name__ == "__main__":
    player1 = smart_player("Daniel")
    player2 = rigged_player2("Patrick")
    simulator = MarketMaker(6,3, [player1, player2])
    while(simulator.rolls_left > 0):
        simulator.make_markets()
    
