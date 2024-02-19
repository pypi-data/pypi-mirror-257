import networkx as nx
import pytest

from tennisrank.algorithm import MatchGraphBuilder, TennisRank
from tennisrank.model import Player, Match, Surface


@pytest.fixture
def players():
    return [
        Player(id=0, name='Alice'),
        Player(id=1, name='Bob'),
        Player(id=2, name='Carol'),
        Player(id=3, name='Dan')
    ]


@pytest.fixture
def matches(players):
    return [
        Match(winner=players[0], loser=players[1],
              win_weight=1, surface='hard'),
        Match(winner=players[0], loser=players[1],
              win_weight=2, surface='hard'),
        Match(winner=players[1], loser=players[0],
              win_weight=3, surface='hard'),
        Match(winner=players[1], loser=players[2],
              win_weight=4, surface='grass'),
        Match(winner=players[2], loser=players[3],
              win_weight=5, surface='clay'),
        Match(winner=players[2], loser=players[3],
              win_weight=6, surface='hard'),
    ]


@pytest.fixture
def graph_builder(matches):
    return MatchGraphBuilder(matches)


class TestMatchGraphBuilder:

    def test_get_same_players(self, players, graph_builder):
        computed_players = graph_builder._get_players()
        assert set(computed_players) == set(players)

    def test_get_multigraph_names(self, players, graph_builder):
        G = graph_builder.get_multigraph()
        assert isinstance(G, nx.MultiDiGraph)
        player_names = {p.name for p in players}
        node_names = {d['name'] for n, d in G.nodes(data=True)}
        for player_name in player_names:
            assert player_name in node_names
        for node_name in node_names:
            assert node_name in player_names

    def test_get_digraph_weights(self, graph_builder):
        G = graph_builder.get_digraph()
        # pdb.set_trace()
        assert isinstance(G, nx.DiGraph)
        # Check win weights on all edges
        assert G.get_edge_data(2, 3) is None
        assert G.get_edge_data(3, 4) is None
        assert G.get_edge_data(1, 0)['weight'] == 3
        assert G.get_edge_data(0, 1)['weight'] == 3
        assert G.get_edge_data(2, 1)['weight'] == 4
        assert G.get_edge_data(3, 2)['weight'] == 11

    def test_tennis_rank_all_unit(self, matches):
        tr = TennisRank(matches)
        ranks = tr.get_ranks(surface=Surface.ANY)
        pids = [rp.player.id for rp in ranks]
        assert pids
