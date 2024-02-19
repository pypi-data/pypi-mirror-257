from dataclasses import dataclass
from enum import Enum


class Surface(Enum):
    HARD = 0
    GRASS = 1
    CLAY = 2
    ANY = 3


@dataclass(frozen=True)
class Player:
    id: int
    name: str


@dataclass(frozen=True)
class Match:
    winner: Player
    loser: Player
    win_weight: float = 1.0
    surface: Surface = Surface.ANY


@dataclass(frozen=True)
class PlayerRank:
    player: Player
    rank: float
    surface: Surface = Surface.ANY
