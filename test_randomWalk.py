import pytest
import networkx as nx
from main import randomWalk

@pytest.fixture
def output_file(tmp_path):
    return tmp_path / "output.txt"

@pytest.fixture
def single_node_graph():
    graph = nx.DiGraph()
    graph.add_node("a")
    return graph

@pytest.fixture
def linear_graph():
    graph = nx.DiGraph()
    graph.add_edges_from([("a", "b"), ("b", "c"), ("c", "d")])
    return graph

@pytest.fixture
def cyclic_graph():
    graph = nx.DiGraph()
    graph.add_edges_from([("a", "b"), ("b", "c"), ("c", "a")])
    return graph

@pytest.fixture
def no_edges_graph():
    graph = nx.DiGraph()
    graph.add_nodes_from(["a", "b", "c", "d"])
    return graph

@pytest.fixture
def repeating_node_graph():
    graph = nx.DiGraph()
    graph.add_edges_from([("a", "a")])
    return graph

def read_and_split(output_file):
    with open(output_file, 'r') as file:
        output = file.read().strip()
    return output.split()

def test_randomWalk_single_node(single_node_graph, output_file):
    randomWalk(single_node_graph, output_file)
    words = read_and_split(output_file)
    assert words == ["a"]

def test_randomWalk_linear_graph(linear_graph, output_file):
    randomWalk(linear_graph, output_file)
    words = read_and_split(output_file)
    assert words[-1] == "d"
    for i in range(len(words) - 1):
        assert words[i + 1] in linear_graph.successors(words[i])

def test_randomWalk_cyclic_graph(cyclic_graph, output_file):
    randomWalk(cyclic_graph, output_file)
    words = read_and_split(output_file)
    assert len(words) > 0
    for i in range(len(words) - 1):
        assert words[i + 1] in cyclic_graph.successors(words[i])

def test_randomWalk_no_edges_graph(no_edges_graph, output_file):
    randomWalk(no_edges_graph, output_file)
    words = read_and_split(output_file)
    assert len(words) == 1

def test_randomWalk_repeating_node_graph(repeating_node_graph, output_file):
    randomWalk(repeating_node_graph, output_file)
    words = read_and_split(output_file)
    for word in words:
        assert word == "a"
