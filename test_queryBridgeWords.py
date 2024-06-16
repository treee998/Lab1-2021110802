import pytest
from main import buildGraphFromText, queryBridgeWords

@pytest.fixture
def graph():
    file_path = "tst.txt"
    return buildGraphFromText(file_path)

@pytest.mark.parametrize("word1, word2, expected", [
    ("exploring", "places", "The bridge words from exploring to places are: new."),
    ("learning", "others", "The bridge words from learning to others are: from."),
    ("people", "us", "The bridge words from people to us are: around.")
])
def test_queryBridgeWords_case1(graph, word1, word2, expected):
    assert queryBridgeWords(graph, word1, word2) == expected

@pytest.mark.parametrize("word1, word2, expected", [
    ("people", "new", "No bridge words from people to new!"),
    ("people", "life", "No bridge words from people to life!"),
    ("people", "learn", "No bridge words from people to learn!")
])
def test_queryBridgeWords_case2(graph, word1, word2, expected):
    assert queryBridgeWords(graph, word1, word2) == expected

@pytest.mark.parametrize("word1, word2, expected", [
    ("apple", "world", "No apple in the graph!"),
    ("world", "banana", "No banana in the graph!"),
    ("apple", "banana", "No apple and banana in the graph!")
])
def test_queryBridgeWords_case3(graph, word1, word2, expected):
    assert queryBridgeWords(graph, word1, word2) == expected

@pytest.mark.parametrize("word1, word2, expected", [
    ("", "world", "Both words must be provided!"),
    ("world", "", "Both words must be provided!"),
    ("", "", "Both words must be provided!")
])
def test_queryBridgeWords_case4(graph, word1, word2, expected):
    assert queryBridgeWords(graph, word1, word2) == expected

@pytest.mark.parametrize("word1, word2, expected", [
    ("and learn", "world", "Both inputs must be single words!"),
    ("world", "new people learn", "Both inputs must be single words!"),
    ("full of beauty", "waiting to be discovered", "Both inputs must be single words!")
])
def test_queryBridgeWords_case5(graph, word1, word2, expected):
    assert queryBridgeWords(graph, word1, word2) == expected
