from collections import defaultdict


class Graph:
    def __init__(self, directed=False):
        self.nodes = defaultdict(set)
        self.directed = directed

    def __repr__(self):
        return f"{self.nodes}"

    def add_node(self, origin, destination):
        self.nodes[origin].add(destination)
        if directed:
            self.nodes[destination].add(origin)

    def connected_components(self):
        def _build_group(key, group):
            if key in visited:
                """
                Recursion end case, go back up
                """
                return
            visited.add(key)
            group.add(key)
            for k in self.nodes[key]:
                _build_group(k, group)

        visited = set()
        groups = []
        for key in self.nodes.keys():
            if key in visited:
                continue
            groups.append(set())
            _build_group(key, groups[-1])
        return groups

    def connected_components_iterative_dfs(self):
        visited = set()
        groups = []

        for node in self.nodes.keys():
            stack = []
            stack.append(node)
            i = 0
            group = []
            while stack:
                curr_node_key = stack.pop()

                if curr_node_key not in visited:
                    group.append(curr_node_key)
                    visited.add(curr_node_key)

                    for key in self.nodes[curr_node_key].keys():
                        stack.append(key)

            if group:
                groups.append(group)

        return groups

    def find_all_paths(self, start, end, path=[]):
        graph = self.nodes
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph.keys():
            return []
        paths = []
        for node in graph[start].keys():
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def remove_node(self, node):
        pass
