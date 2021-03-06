"""User Documentation

 A graph holds a collection of nodes and edges.  Each node
 must be derived from Graph.GraphNode and each edge must
 be derived from Graph.GraphEdge.

 You can see example classes in Node.py and Edge.py tailored
 for network topology.

I Implementation details that you don't really need to know about
 Why use handles?
 
 Each node and edge has a unique integer identifier known as
 a handle.  The handle is used to help identify a particular
 object or instance of an object.  For example two different
 nodes may be equivalent but are not the same object.  These
 two nodes will have different handles.

 The handles are used to create the internal graph structure.

 For example a node N might have a handle of 1
 >>> from NetworkGraph.GraphObject import GraphObject
 >>> N = GraphObject()
 >>> print N.handle
 1

 and a node M might have a handle of 2
 >>> M = GraphObject()
 >>> print M.handle
 2

 the nodes might be equivalent
 >>> print N == M
 1

 but they are not the same
 >>> print N is M
 0

 >>> print N.handle == M.handle
 0

 Using an integer handle helps speed up dictionary lookups inside
 the graph class.  Technically they aren't really necessary but
 they speed things up by an order of magnitude.


II Creating a graph
  >>> from NetworkGraph.Graph import Graph
  >>> g = Graph()

  We have just created a graph with no edges or nodes.
  We need to create a node now.
  >>> from NetworkGraph.GraphObject import GraphNode
  >>> node1 = GraphNode()

  This creates an unlabeled node.  To create a labeled
  node:
  >>> node2 = GraphNode(label="blue")

  The label can be any python object that can be used in an
  equivelence statement.

  >>> print node1 == node2
  0

  We can now add the nodes to the graph.
  >>> g.add_node(node1)
  >>> g.add_node(node2)

  Check to see if the graph contains node1?
  >>> print g.has_node(node1)
  1

  We can add an edge between node1 and node2

  >>> from NetworkGraph.GraphObject import GraphEdge
  >>> edge1 = GraphEdge(label="my dog has fleas")
  >>> g.add_edge(edge1, node1, node2)
  >>> print g.has_edge(edge1)
  1

  We can query edges and nodes about their topology
  >>> print edge1.nodes
  (GraphNode(), GraphNode('blue'))

  Let's find the node on the other end of edge1 from node1
  >>> n = edge1.xnode(node1)
  This better be node2 :)  Notice we are not using == here since
  we are checking to see if n is the same object as node2.
  >>> print n is node2
  1

  We could have used handles as well
  >>> print n.handle == node2.handle
  1

  Let's dump the topology
  >>> g.dump()
  Topology
  Nodes
	GraphNode()
	GraphNode(`blue`)

  Edges
	GraphEdge(`my dog has fleas`) (GraphNode(), GraphNode(`blue`))
  
  For fun let's remove an edge
  >>> g.remove_edge(edge1)
  >>> g.dump()
  Topology
  Nodes
	GraphNode()
	GraphNode('blue')

  Edges

  Now let's add it back
  >>> g.add_edge(edge1, node1, node2)

  We can't add the same edge twice
  >>> g.add_edge(edge1, node1, node2)
  Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "GraphObject.py", line 20, in set_parent
    assert self.parent is None, "%s already belongs to a graph!"
  AssertionError: GraphEdge already belongs to a graph!

  
III
  Using graphs.

  This package uses three types of graphs, Graph's, matchable graphs
  and matching graphs.
  
  The matchable and matching graphs are python objects created for
  the sole purpose of subgraph isomorphisms.  They are created from Graph
  objects in the following manner:

  matchableGraph = graph.to_graph()
  matcher = graph.to_matcher()

  a matcher has two methods that both operate on matchable graphs.

  results = matcher.match(matchableGraph, limit=-1)
    The match function returns up to limit matches of the
    matcher topology on the matchableGraph topology.
    This returns all matches found in all permutations.
    
    
  results = matcher.umatch(matchableGraph, limit=-1)
    The match function returns up to limit matches of the
    matcher topology on the matchableGraph topology.
    This returns all the unique matches on a graph.
    Permutations of the same match are not returned.


  The results list is a list of nodes and edges found in the
  isomorphism.

  Let's try matching g against itself.
  First create a matchable object.
  >>> h = g.to_graph()

  Now create a matcher
  >>> matcher = g.to_matcher()

  >>> results = matcher.match(h)
  >>> for nodes, edges in results:
  >>>     print nodes
  >>>     print edges
  (GraphNode(), GraphNode('blue'))
  (GraphEdge('my dog has fleas'),)

  Let's check this a little better and make a clone of g, add
  a node to the clone and see what matches.  But first, what
  is a clone?

  >>> clone = g.clone()

  Clone's contain the exact topology of their parent but have
  completely different internal nodes and objects.

  The following code loops through all the nodes in g
  and makes sure that they don't exist in the clone.

  >>> for node in g.nodes:
  >>>     assert not clone.has_node(node)

  However the same node in g should be equivalent to the same
  node in the clone (we'll use the handy python zip function
  to zip two lists together)

  >>> for original, cloned in zip(g.nodes, clone.nodes):
  >>>   assert original == cloned
  >>>   assert original is not cloned

  I'm beating this point to death to point out the fact that
  these are different graphs.  Matching results from a parent
  graph are not transferable to the clone graph.  The clone
  needs to be rematched.
  
  
  Okay, we've made a clone so let's add an edge and node to the clone.
  >>> node3 = GraphNode("I am a clone!")
  >>> edge2 = GraphEdge("new edge")
  >>> clone.add_node(node3)

  We need to get the clone's first node here since node1
  doesn't exist in the clone
  >>> n1 = clone.nodes[0]
  >>> clone.add_edge(edge2, node3, n1)

  We'll use the original matcher to match the original graph
  against the modified clone
  >>> matchableClone = clone.to_graph()
  >>> results = matcher.umatch(matchableClone)
  
  Now let's make a new graph with all of the matching nodes
  and edges removed

  >>> nodes, edges = results[0]
  >>> partialClone = clone.clone(ignoreNodes=nodes, ignoreEdges=edges)

  Notice how the partialClone only has the node we added.  Since
  all other nodes matched, they were removed.
  >>> partialClone.dump()
  Topology
  Nodes
       GraphNode('I am a clone!')

  Edges

IV
 Graph storage.  Matcher graphs and matchable graphs are not natively
 storable.  This is partly because they hold arbitrary python objects
 and code and partly because they are actually C++ objects that
 are wrapping this codebase.

 Graph objects however, are very storable using python's serialization
 module pickle.

 >>> import pickle
 >>> file = open("graphfile", "wb")
 >>> pickle.dump(clone, file)

 Perhaps a nicer mechanism is using shelve.  Shelve works quite
 nice if you have a real database installed.  See the shelve
 module or python documentation for details.  Shelve database
 behave like python dictionaries but can store picklable objects. 

 >>> import shelve
 >>> db = shelve.open("foo.database")
 >>> db['first graph'] = clone
 >>> db.close()
 
 >>> import shelve
 >>> db = shelve.open("foo.database")
 >>> graph = db['first graph']

 The berkeley database is particularly good for large objects.
 See pybsddb3.sourceforge.net for downloads.  You'll have to
 replace import shelve with something like
 >>> import bsddb3.dbshelve as shelve

 When loading shelve or pickle solutions it is a good idea to
 replace each graph with it's clone to reset the handles since
 they are not saved from one session to another.  In a future
 version this should not be necessary.

 >>> graph = graph.clone()
 """
