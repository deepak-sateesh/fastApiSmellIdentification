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
                return True

    return False