from random import randint as r


class Game:
    @staticmethod
    def roll_dice():
        return r(0, 6)
