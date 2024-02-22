from jsspetri.envs.instance_loader import load_instance
from jsspetri.envs.build_blocks import Token, Place, Transition


class Petri_build:
    """
    A class representing a Petri net for Job Shop Scheduling Problems (JSSP).

    Attributes:
        instance_id (str): The ID of the JSSP instance.
        instance (pd.DataFrame): The JSSP instance data.
        n_jobs (int): The number of jobs in the instance.
        n_machines (int): The number of machines in the instance.
        max_bound (int): The maximum number of operations or tokens.

        places (dict): A dictionary containing Place objects.
        transitions (dict): A dictionary containing Transition objects.
    """

    def __init__(self, instance_id,flexible=False,dynamic=False):
        """
        Initialize the Petri net with a JSSP instance.

        Parameters:
            instance_id (str): The ID of the JSSP instance.
        """
        self.flexible=flexible
        self.dynamic=dynamic
        self.instance_id = instance_id
        self.instance, specs = load_instance(self.instance_id)
        
        self.max_njobs=100
        self.max_nmachines=20
        self.n_jobs, self.n_machines, self.n_features,self.max_bound = specs

        self.places = {}
        self.transitions = {}
        
        if  self.flexible : 
            self.create_petri_flexible()       
        else : 
            self.create_petri()

    def __str__(self):
        """
        Get a string representation of the Petri net.

        Returns:
            str: A string representing the Petri net.
        """
        return f"JSSP {self.instance_id}: {self.n_jobs} jobs X {self.n_machines} machines"

    def add_nodes_layer(self, is_place=True, node_type="", number=1):
        """
        Add a layer of nodes (places or transitions) to the Petri net.

        Parameters:
            is_place (bool): True if nodes are places, False if transitions.
            node_type (str): The type of nodes to be added.
            number (int): The number of nodes to be added.
        """
        if is_place:
            for i in range(number):
                place_name = f"{node_type} {i}"
                place = Place(place_name, node_type, color=i)
                self.places[place.uid] = place
        else:
            for i in range(number):
                transition_name = f"{node_type} {i}"
                transition = Transition(transition_name, node_type, color=i)
                self.transitions[transition.uid] = transition

    def add_connection(self, parent_type, child_type, contype="p2t", full_connect=False):
        """
        Add connections (arcs) between nodes in the Petri net.

        Parameters:
            parent_type (str): The type of parent nodes.
            child_type (str): The type of child nodes.
            contype (str): Connection type ("p2t" for place to transition, "t2p" for transition to place).
            full_connect (bool): True for a fully connected graph, False for pairwise connections.
        """
        if contype == "p2t":
            parent_nodes = [p for p in self.places.values() if p.type == parent_type]
            child_nodes = [t for t in self.transitions.values() if t.type == child_type]
        elif contype == "t2p":
            parent_nodes = [t for t in self.transitions.values() if t.type == parent_type]
            child_nodes = [p for p in self.places.values() if p.type == child_type]

        if full_connect:
            for parent in parent_nodes:
                for child in child_nodes:
                    parent.add_arc(child, parent=False)
                    child.add_arc(parent, parent=True)
        else:
            for parent, child in zip(parent_nodes, child_nodes):
                parent.add_arc(child, parent=False)
                child.add_arc(parent, parent=True)

    def add_tokens(self):
        """
        Add tokens to the Petri net.
        Tokens represent job operations .
        """
        # Add idle tokens
        for uid in self.filter_nodes("idle"):
            self.places[uid].token_container.append(Token(initial_place=uid, color=(None, self.places[uid].color)))
            self.places[uid].color = None

        #Add tokens :
        for job, uid in enumerate(self.filter_nodes("job")):
            try:
                for i,(machine,features) in enumerate (self.instance[job].items()) : 
                    self.places[uid].token_container.append(
                        Token(initial_place=uid, color=(job, machine), features=features ,order=i))
            except:
                pass
            

    def filter_nodes(self, node_type):
        """
        Filter nodes in the Petri net based on node type.

        Parameters:
            node_type (str): The type of nodes to filter.

        Returns:
            list: A list of node UIDs that match the specified type.
        """
        filtered_nodes = [place.uid for place in self.places.values() if place.type == node_type]
        filtered_nodes.extend([transition.uid for transition in self.transitions.values() if transition.type == node_type])
        return filtered_nodes

    def create_petri(self):
        """Create the Petri net structure, adding nodes, connections, and tokens."""
        nodes_layers = [
            (True, "job", self.n_jobs),
            (False, "allocate", self.n_machines),
            (True, "machine", self.n_machines),
            (False, "finish_op", self.n_machines),
            (True, "finished_ops", self.n_machines),
        ]

        layers_to_connect = [
            ("job", "allocate", "p2t", True),
            ("allocate", "machine", "t2p", False),
            ("machine", "finish_op", "p2t", False),
            ("finish_op", "finished_ops", "t2p", False),
        ]

        # Add nodes: places and transitions
        for is_place, node_type, number in nodes_layers:
            self.add_nodes_layer(is_place, node_type, number)

        # Add arcs places and transitions
        for parent_type, child_type, contype, full_connect in layers_to_connect:
            self.add_connection(parent_type, child_type, contype, full_connect)

        # Add jobs tokens
        self.add_tokens()

        # Add idles transition
        transition = Transition("standby", "allocate", color=self.n_machines)
        transition.children.append(Place("standby_place", "idle_state", color=self.n_machines))
        self.transitions[transition.uid] = transition

        print (f"JSSP {self.instance_id} : {self.n_jobs} jobs X {self.n_machines} machines  loaded , flexible Mode: {self.flexible} ,Dynamic Mode: {self.dynamic}")
        
        
    def create_petri_flexible(self):
        
        """Create the Petri net structure, adding nodes, connections, and tokens. flexible mean create
        the maximun number of machine and jobs independent from the instance """
        

        nodes_layers=[ (True,"job",self.max_njobs),
                       (False,"allocate",self.max_nmachines),
                       (True,"machine",self.max_nmachines),
                       (False,"finish_op",self.max_nmachines),
                       (True,"finished_ops",self.max_nmachines),      
                       ]
                         
        layers_to_connect=[
                           ("job","allocate","p2t",True),
                           ("allocate","machine","t2p",False),
                           ("machine","finish_op","p2t",False),
                           ("finish_op","finished_ops","t2p",False),
                           ]
        
        #Add nodes : plaxes and transitions
        for is_place,node_type,number in nodes_layers:   
            self.add_nodes_layer(is_place,node_type,number)
    
        #Add arcs places and transitions 
        for parent_type, child_type, contype, full_connect in layers_to_connect:   
            self.add_connection(parent_type, child_type,contype, full_connect)
            
        #Add jobs tokens     
        self.add_tokens()

        # Add idles transition
        transition = Transition("standby", "allocate", color=self.max_nmachines)
        transition.children.append(Place("standby_place", "idle_state", color=self.max_nmachines))
        self.transitions[transition.uid] = transition

        print (f"JSSP {self.instance_id} : {self.n_jobs} jobs X {self.n_machines} machines  loaded , flexible Mode: {self.flexible} ,Dynamic Mode: {self.dynamic}" )
        
        

# %% Test
if __name__ == "__main__":
    petri = Petri_build("ta01",True)
    

    
  
    




