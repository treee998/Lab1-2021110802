import re
import random
import networkx as nx
import matplotlib.pyplot as plt


def buildGraphFromText(file_path):
    graph = nx.DiGraph()

    with open(file_path, 'r') as file:
        text = file.read().replace('\n', ' ')
        words = re.findall(r'\b[A-Za-z]+\b', text.lower())

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]

        if not graph.has_edge(current_word, next_word):
            graph.add_edge(current_word, next_word, weight=1)
        else:
            graph[current_word][next_word]['weight'] += 1

    return graph


def showDirectedGraph(graph):
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


def queryBridgeWords(graph, word1, word2):
    def is_single_word(word):
        return len(word.split()) == 1

    if not word1 or not word2:
        return "Both words must be provided!"
    if not is_single_word(word1) or not is_single_word(word2):
        return "Both inputs must be single words!"
    if word1 not in graph and word2 in graph:
        return "No {} in the graph!".format(word1)
    elif word1 in graph and word2 not in graph:
        return "No {} in the graph!".format(word2)
    elif word1 not in graph and word2 not in graph:
        return "No {} and {} in the graph!".format(word1, word2)

    bridge_words = []
    for bridge_word in graph[word1]:
        if bridge_word in graph and word2 in graph[bridge_word]:
            bridge_words.append(bridge_word)

    if not bridge_words:
        return "No bridge words from {} to {}!".format(word1, word2)

    return "The bridge words from {} to {} are: {}.".format(word1, word2, ", ".join(bridge_words))


def generateNewText(graph, text):
    words = re.findall(r'\b[A-Za-z]+\b', text.lower())
    new_text = []
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        new_text.append(current_word)
        if current_word in graph:
            bridge_words_str = queryBridgeWords(graph, current_word, next_word)
            if "The bridge words" in bridge_words_str:
                bridge_words = bridge_words_str.split(": ")[1].strip('.').split(", ")
                if bridge_words:
                    chosen_bridge = random.choice(bridge_words)
                    new_text.append(chosen_bridge)
    new_text.append(words[-1])
    return ' '.join(new_text)


def findShortestPath(graph, start_word, end_word):
    try:
        path = nx.dijkstra_path(graph, start_word, end_word)
        length = nx.dijkstra_path_length(graph, start_word, end_word)
        return path, length
    except nx.NetworkXNoPath:
        return None, None


def showDirectedGraphWithPath(graph, path=None):
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='red')
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)

    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


def calcShortestPath(graph, start_word, end_word):
    path, length = findShortestPath(graph, start_word, end_word)

    if path:
        print(f"The shortest path from '{start_word}' to '{end_word}' is: {' -> '.join(path)}")
        print(f"The path length is: {length}")
        showDirectedGraphWithPath(graph, path)
    else:
        print(f"No path found between '{start_word}' and '{end_word}'")
        showDirectedGraphWithPath(graph)


def randomWalk(graph, output_file):
    start_node = random.choice(list(graph.nodes()))
    visited_nodes = set()
    traversal_path = []

    current_node = start_node
    while current_node:
        traversal_path.append(current_node)
        visited_nodes.add(current_node)

        next_nodes = list(graph.successors(current_node))
        if next_nodes:
            next_node = random.choice(next_nodes)
            traversal_path.append((current_node, next_node))
            current_node = next_node
        else:
            current_node = None

        if current_node in visited_nodes or current_node not in graph:
            break

    with open(output_file, 'w') as file:
        sentence = ""
        prev_word = None
        for item in traversal_path:
            if isinstance(item, tuple):
                word1, word2 = item
                if word1 != prev_word:
                    sentence += ' ' + word1
                sentence += ' ' + word2
                prev_word = word2
            else:
                if item != prev_word:
                    sentence += ' ' + item
                prev_word = item

        sentence = sentence.strip()

        file.write(sentence)


def main():
    file_path = "tst.txt"
    output_file = "out.txt"

    graph = buildGraphFromText(file_path)
    showDirectedGraph(graph)

    while 1:
        print("1.QueryBridgeWords")
        print("2.GenerateNewText")
        print("3.CalcShortestPath")
        print("4.RandomWalk")
        print("5.Exit")
        choice = input("Enter your choice:")

        if choice == "1":
            word1 = input("Enter word 1: ").lower()
            word2 = input("Enter word 2: ").lower()
            bridge_words = queryBridgeWords(graph, word1, word2)
            print(bridge_words)

        elif choice == "2":
            new_text = input("Enter a new text: ")
            modified_text = generateNewText(graph, new_text)
            print("Modified text:", modified_text)

        elif choice == "3":
            start_word = input("Enter start word for shortest path: ").lower()
            end_word = input("Enter end word for shortest path: ").lower()
            calcShortestPath(graph, start_word, end_word)

        elif choice == "4":
            randomWalk(graph, output_file)
            print("Traversal output saved to", output_file)

        elif choice == "5":
            break

        else:
            print("Invaluable choice!\n")


if __name__ == "__main__":
    main()
