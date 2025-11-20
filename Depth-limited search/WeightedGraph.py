class WeightedGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        # Initialize a 2D matrix with zeros
        self.adj_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    def add_edge(self, node1, node2, w):
        # Add an undirected edge between node1 and node2
        self.adj_matrix[node1][node2] = w
        self.adj_matrix[node2][node1] = w
        pass

    def remove_edge(self, node1, node2):
        # Remove the edge between node1 and node2
        self.adj_matrix[node1][node2] = 0
        self.adj_matrix[node2][node1] = 0

    def num_edges(self):
        num_edges = 0
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if self.adj_matrix[i][j] != 0:
                    num_edges += 1
        return num_edges

    def print_graph(self):
        # Print the adjacency matrix
        for row in self.adj_matrix:
            print(" ".join(map(str, row)))

if __name__ == "__main__":
    # use case
    test_graph = WeightedGraph(3)
    test_graph.add_edge(1,0, 2)
    test_graph.add_edge(1, 2, 3)
    test_graph.print_graph()
    print(test_graph.num_edges())