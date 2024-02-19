import difflib
import pandas as pd

from tennisrank.model import Player, Match, PlayerRank, Surface


def df_to_matches(df: pd.DataFrame):
    df['win_weight'] = 1.0
    for _, row in df.iterrows():
        winner = Player(id=row['winner_id'], name=row['winner_name'])
        loser = Player(id=row['loser_id'], name=row['loser_name'])
        surface = Surface.HARD if pd.isna(
            row['surface']) else Surface[row['surface'].upper()]
        win_weight = row['win_weight']
        yield Match(winner=winner, loser=loser, win_weight=win_weight, surface=surface)


def ranks_to_df(ranks: list[PlayerRank]) -> pd.DataFrame:
    dicts = [
        {
            'player_id': r.player.id, 'player_name': r.player.name,
            'rank': r.rank, 'surface': r.surface.name.title()
        }
        for r in ranks
    ]
    return pd.DataFrame(dicts)


def fuzzy_match(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def load_matches(urls: list[str]):
    def iter_matches():
        for url in urls:
            df = pd.read_csv(url)
            yield from df_to_matches(df)
    return list(iter_matches())


def load_atp(*years):
    urls = [(
            'https://raw.githubusercontent.com/JeffSackmann/'
            f'tennis_atp/master/atp_matches_{year}.csv'
            )
            for year in years
            ]
    return load_matches(urls)


def load_wta(*years):
    urls = [(
            'https://raw.githubusercontent.com/JeffSackmann/'
            f'tennis_wta/master/wta_matches_{year}.csv'
            )
            for year in years
            ]
    return load_matches(urls)
