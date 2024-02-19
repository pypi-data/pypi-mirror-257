from tennisrank.model import Player, Match, PlayerRank, Surface


def test_player():
    assert Player(id=0, name='X')


def test_match():
    assert Match(
        winner=Player(id=0, name='X'),
        loser=Player(id=1, name='Y'),
        win_weight=42.0,
        surface=Surface.HARD
    )


def test_player_rank():
    assert PlayerRank(Player(id=0, name='X'), rank=42.0, surface=Surface.ANY)
