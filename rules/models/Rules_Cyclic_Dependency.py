import networkx as nx
def find_cyclic_dependency(lst):
    graph = {}
    for item in lst:
        parent, child = item
        if parent not in graph:
            graph[parent] = []
        graph[parent].append(child)

    visited = set()
    stack = set()

    def dfs(node):
        visited.add(node)
        stack.add(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    return True

        stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                cycles = return_cycles(lst)
                return (True, cycles)

    return (False, ())


def return_cycles(lst):

    # Create a directed graph
    G = nx.DiGraph()
    for l in lst:
        # Add edges to the graph
        G.add_edge(l[0], l[1])


    # Find all cycles in the graph
    cycles = list(nx.simple_cycles(G))

    # Print the cycles as list of tuples
    cycle_tuples = [tuple(cycle) for cycle in cycles]
    return cycle_tuples