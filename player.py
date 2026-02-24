from dataclasses import dataclass
import pandas as pd

@dataclass(frozen = True)
class Player:
    name: str
    row: pd.Series 
    def get(self, col: str, default=None):
        if col not in self.row.index:
            return default
        val = self.row[col]
        if pd.isna(val):
            return default
        return val