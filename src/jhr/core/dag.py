import networkx as nx

class DAG:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_calc(self, calc):
        """Add a calculation node to the DAG"""
        self.graph.add_node(calc.name, calc=calc)
    
    def add_dependency(self, parent, child):
        """Add a dependency (directed edge)"""
        self.graph.add_edge(parent.name, child.name)
    
    def execute(self):
        """Run calculations in topological order"""
        for node in nx.topological_sort(self.graph):
            self.graph.nodes[node]['calc'].run()

# Create calculations
calc_A = Calc("A")
calc_B = Calc("B", dependencies=[calc_A])
calc_C = Calc("C", dependencies=[calc_A])
calc_D = Calc("D", dependencies=[calc_B, calc_C])

# Create DAG
dag = DAG()
dag.add_calc(calc_A)
dag.add_calc(calc_B)
dag.add_calc(calc_C)
dag.add_calc(calc_D)

# Define dependencies
dag.add_dependency(calc_A, calc_B)
dag.add_dependency(calc_A, calc_C)
dag.add_dependency(calc_B, calc_D)
dag.add_dependency(calc_C, calc_D)

# Execute DAG
dag.execute()

