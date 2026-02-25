import math
from player import Player
from functions import get_player_row

SURFACE_MAP = {
    "All": "Elo",
    "Hard": "hElo",
    "Clay": "cElo",
    "Grass": "gElo",
}

class MatchPredictor:
    def __init__(self, df):
        self.df = df

    def get_player(self, name):
        row = get_player_row(self.df, name)
        if row is None:
            return None
        return Player(row["Player"], row)

    def predict_winner(self, name_A, name_B, surface):
        player_A = self.get_player(name_A)
        player_B = self.get_player(name_B)
        if player_A is None or player_B is None:
            return None
        elo_col = SURFACE_MAP.get(surface,"Elo")
        eloA = float(player_A.get(elo_col))
        eloB = float(player_B.get(elo_col))
        probA = 1 / (1 + 10 ** ((eloB - eloA) / 400))
        probB = 1 - probA
        return probA, probB

    def power(self, name, surface):
        player = self.get_player(name)
        if player is None:
            return None
        elo_col = SURFACE_MAP.get(surface,"Elo")
        elo = float(player.get(elo_col))
        spw = float(player.get("ServicePointsWonPercentage"))
        fsrp = float(player.get("FirstServeReturnPointsWonPercentage"))
        ssrp = float(player.get("SecondServeReturnPointsWonPercentage"))
        tb_won = float(player.get("TieBreaksWon"))
        tb = float(player.get("TieBreaks"))
        if tb > 0:
            tb_ratio = (tb_won / tb) 
        else:
            tb_ratio = 0.0
        bpc = float(player.get("BreakPointsConvertedPercentage"))
        ace = float(player.get("AcePercentage"))
        dfp = float(player.get("DoubleFaultPercentage"))
        pwr = (
            3 * spw 
            + 2 * (ssrp + fsrp)
            + 1.5 * tb_ratio 
            + 1.5 * bpc
            + 1 * ace
            - 1.5 * dfp
            + 1.25 * (elo - 2000)/400
        )
        return pwr

    def win_set_odds(self, name_A, name_B, surface):
        pA = self.power(name_A, surface)
        pB = self.power(name_B, surface)
        if pA is None or pB is None:
            return None
        diff = pA - pB
        return 1 / (1 + math.exp(-diff))
