MST: Graph x Vertex -> Tree

Returns a minimum spanning tree of the input graph using the input vertex as
a starting point.

Walks: Graph x Vertex x Vertex -> List of Walk

Returns a set of walks from the first vertex to the second vertex,
under the following contraint: Let E be the intersection of edges
reachable from the first vertex and the set of edges that can reach
the second vertex.  Every edge in E must be used by at least one walk
in the set of output walks.

Flatten: Tree -> List of Vertex

Returns a list of the vertices reachable from the root vertex of the
input tree.

Leaves: Tree -> List of Vertex

Returns the leaf vertices in the input tree.

TreeWalk: Tree x Vertex -> Walk

Returns the walk from the root of the input tree to the target vertex.

LeafWalks: Tree -> List of Walk

Returns the walks from the root vertex of the tree to the leaf vertices.

LeftDerivation: Walk -> Vector of Symbol

Returns the string of symbols that is derived by the input walk
(assumes the walk is of a production graph), starting with the start
symbol.  Each application of a production in the walk is applied to
the leftmost nonterminal matching the left hand side of the
production.

LHS: Vertex -> Symbol

Returns the the left hand side of the production represented by the
input vertex.

SymmetricAssociation: (Map from (A x A) to B) x A x A x B -> (Map from
                                                              (A x A) to B)

Sets both orderings of the A type inputs to reference the B type value
in the input map.


BaseTree : Tree
TestStrings : List of List of Symbol
TestMap : Map from (Vertex x Vertex) to Walk
ReachableMap : Map from Symbol to List of Vertex
ReachMap : Map from (Symbol x Vertex) to Walk

# Now populate mapping for all case 1 test cases (these are already in
# the test string list).

Input: Grammar G.

BaseTree = MST(PG(G), p_0)

TestStrings = Map(LeftDerivation, LeafWalks(BaseTree, p_0))

for p_i in (PV(G) - {p_0}):
    walk = TreeWalk(BaseTree, p_i)
    for p_j in walk[1:-1]:
        TestMap = SymmetricAssociation(TestMap, p_i, p_j, walk)

# Populate mapping for case 2 test cases.

for p_i in (PV(G) - {p_0}):
    tree = MST(PG(G), p_i)
    symbol_i = LHS(p_i)
    ReachableMap[symbol_i] = {}
    for p_j in Flatten(tree):
        if (p_j, p_i) not in TestMap:
            walk = TreeWalk(BaseTree, p_i) + TreeWalk(tree, p_j)
            TestMap = SymmetricAssociation(TestMap, p_j, p_i, walk)
            TestStrings = Union(TestStrings, LeftDerivation(walk))
        # Initialize data for case 3
        symbol_j = LHS(p_j)
        walk_i_to_j = First(Walks(tree, p_i, p_j))
        if symbol_j not in ReachableMap[symbol_i]:
            ReachableMap[symbol_i] = Union(ReachableMap[symbol_i], {p_j})
            ReachMap[(symbol_i, p_j)] =  MinWalk(
                ReachMap[(symbol_i, p_j)],
                walk_i_to_j)

# Populate mapping for case 3 test cases.

for p_i in (P - {p_0}):
    for walk in Walks(PG(G), p_0, p_i):
        passed = False
        derivation = LeftDerivation(walk[:-1])
        for symbol in (derivation - {LHS(p_i)}):
            for p_j in ReachableMap[symbol]:
                if (p_j, p_i) not in TestMap:
                    crntWalk = walk + ReachMap[(symbol, p_j)]
                    TestMap = SymmetricAssociation(TestMap, p_j, p_i,
                                                   crntWalk)
                    TestStrings = Union(TestStrings,
                                        LeftDerivation(crntWalk))


# XXX Ordered attempt:

for p_i in (P - {p_0}):
    for walk in Walks(PG(G), p_0, p_i):
        passed = False
        derivation = LeftDerivation(walk[:-1])
        index = 0
        while derivation[index] != LHS(p_i):
            for p_j in ReachableMap[derivation[index]]:
                if (p_j, p_i) not in TestMap:
                    crntWalk = walk + ReachMap[(derivation[index],
                                                p_j)]
                    TestMap = SymmetricAssociation(TestMap, p_j, p_i,
                                                   crntWalk)
                    TestStrings = Union(TestStrings, LeftDerivation(crntWalk))
            index = index + 1
        index = index + 1
        while index < (len(derivation) - 1):
            for p_j in ReachableMap[derivation[index]]:
                if (p_j, p_i) not in TestMap:
                    crntWalk = walk + ReachMap[(derivation[index],
                                                p_j)]
                    TestMap = SymmetricAssociation(TestMap, p_i, p_j,
                                                   crntWalk)
                    TestStrings = Union(TestStrings, LeftDerivation(crntWalk))
            index = index + 1
