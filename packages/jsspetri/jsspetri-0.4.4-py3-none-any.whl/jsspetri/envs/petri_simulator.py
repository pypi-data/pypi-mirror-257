import copy
from jsspetri.envs.petri_build import Petri_build


class JSSPSimulator(Petri_build):
    """
    Class representing the core logic of a Job Shop Scheduling Problem (JSSP) simulation using a Petri net.

    Attributes:
        internal_clock (int): The internal clock of the simulation.
        interaction_counter (int): Counter for interactions in the simulation.
        total_internal_steps (int): Total internal steps taken in the simulation.
        delivery_history (dict): Dictionary storing the delivery history.
        action_map (dict): Mapping for actions in the simulation.

    Methods:
        __init__(instanceID): Initializes the JSSPSimulator.
        time_tick(gui, action): Increments the internal clock and updates token logging.
        filter_nodes(node_type): Filters nodes based on node type.
        transfer_token(origin, destination, current_clock): Transfers a token from one place to another.
        fire_colored(action): Fires colored transitions based on the provided action.
        fire_timed(): Fires timed transitions based on completion times.
        petri_interact(gui, action): Performs Petri net interactions and updates internal state.
        petri_reset(): Resets the internal state of the Petri net.
        projected_makespan(): Calculates the projected makespan based on the current state.
        is_terminal(): Checks if the simulation has reached a terminal state.
        action_mapping(n_machines, n_jobs): Maps multidiscrete actions to a more usable format.
        enabled_allocations(): Checks which allocations are enabled.
    """

    def __init__(self, instance_id,flexible=False,dynamic=False):
        """
        Initializes the JSSPSimulator.

        Parameters:
            instanceID (str): Identifier for the JSSP instance.
            flexible (bool) : if True, a petrinet with 100*200  container is created regardless the actual instance size 
            dynamic (bool) : if True, appending  new operations is possile , the termination condition is that all queues are empty
            
        """
        super().__init__(instance_id,flexible,dynamic)
        
        self.dynamic=dynamic
        self.flexible=flexible  
        self.internal_clock = 0
        self.interaction_counter = 0
        self.delivery_history = {}
        
        
        if self.flexible :
            self.action_map=self.action_mapping(self.max_nmachines, self.max_njobs)
        else :
            self.action_map = self.action_mapping(self.n_machines, self.n_jobs)


    def time_tick(self,action):
        """
        Increments the internal clock and updates token logging.

        Parameters:
            action: Action to be performed.
        """
        self.internal_clock += 1
        # Increment time in token logging

        for place in self.places.values():
            for token in place.token_container:
                token.logging[list(token.logging.keys())[-1]][2] += 1


    def filter_nodes(self, node_type):
        """
        Filters nodes based on node type.
        Parameters:
            node_type (str): Type of nodes to filter.

        Returns:
            list: Filtered nodes.
        """

        filtered_nodes = []
        for place in self.places.values():
            if place.type == node_type:
                filtered_nodes.append(place.uid)

        for transition in self.transitions.values():
            if transition.type == node_type:
                filtered_nodes.append(transition.uid)

        return filtered_nodes

    def transfer_token(self, origin, destination, current_clock=0):
        """
        Transfers a token from one place to another.

        Parameters:
            origin: Origin place.
            destination: Destination place.
            current_clock (int): Current simulation clock.
        """
        logging = origin.token_container[0].logging[origin.uid]
        logging[1] = logging[0] + logging[2]

        token = copy.copy(origin.token_container[0])
        origin.token_container.pop(0)
        destination.token_container.append(token)
        
        token.logging[destination.uid] = [current_clock, 0, 0]

    def fire_colored(self, action):
        """
        Fires colored transitions based on the provided action.

        Parameters:
            action: Action to be performed.

        Returns:
            bool: True if a transition is fired, False otherwise.
        """
        self.interaction_counter += 1
        
        fired = False
  
        action = self.action_map[int(action)]
        transition_num = action[0]
        job_num = action[1]
        
        standby_id = self.max_nmachines if self.flexible else self.n_machines
            
        
        transition = [t for t in self.transitions.values() if t.uid in self.filter_nodes("allocate")][transition_num]
        if transition_num != standby_id:
            if len(transition.children[0].token_container) == 0:
                for job_queue in transition.parents:
                    if len(job_queue.token_container) > 0:
                        if job_queue.token_container[0].color == (job_num, transition.color):
                            self.transfer_token(
                                job_queue, transition.children[0], current_clock=self.internal_clock)
                            fired = True
        else:
            fired = True
        return fired

    def fire_timed(self):
        """
        Fires autonomous transitions based on completion times.
        """
        ready_transitions = []
        machine_places = [p for p in self.places.values() if p.uid in self.filter_nodes("machine")]
        for place in machine_places:
            for token in place.token_container:
                if token.logging[list(token.logging.keys())[-1]][2] > token.process_time:
                    ready_transitions.append(place.children[0])

        for transition in ready_transitions:
            self.transfer_token(
                transition.parents[0], transition.children[0], current_clock=self.internal_clock)

        # Keep a history of delivery (to use in solution later)
        finished_tokens = []
        finished_places = [p for p in self.places.values() if p.uid in self.filter_nodes("finished_ops")]
        for place in finished_places:
            finished_tokens.extend(place.token_container)
        self.delivery_history[self.internal_clock] = finished_tokens
        
        
    def petri_reset(self):
        """
        Resets the internal state of the Petri net.
        """
        self.internal_clock = 0
        for place in self.places.values():
            place.token_container = []
        # Add tokens
        self.add_tokens()


    # Utilities
    def projected_makespan(self):
        """
        Calculates the projected makespan based on the current state.

        Returns:
            int: Projected makespan.
        """
        waiting_penalty = self.n_machines

        completion_time = [1 for _ in range(self.n_machines)]
        
        jobs_queue = [p for p in self.places.values() if p.uid in self.filter_nodes("job")]
        machine_places = [p for p in self.places.values() if p.uid in self.filter_nodes("machine")]

        # Step 1: Estimate completion time for operations in process
        for machine in machine_places:
            if len(machine.token_container) > 0:
                for in_process in machine.token_container:
                    
                    elapsed = in_process.logging[list(in_process.logging.keys())[-1]][2]
                    remaining = in_process.process_time - elapsed
                    completion_time[in_process.color[1]] = self.internal_clock + remaining
            else:
                completion_time = [self.internal_clock for _ in range(self.n_machines)]

        # Step 2: Assume optimal processing of remaining operations
        for job in jobs_queue:
            if len(job.token_container) > 0:
                for operation in job.token_container:
                    completion_time[operation.color[1]] += operation.process_time * waiting_penalty


        return max(completion_time)

    def is_terminal(self):
        """
        Checks if the simulation has reached a terminal state.
        if flexiblethe state is terminal if all the machines and queues are empty 
        

        Returns:
            bool: True if the terminal state is reached, False otherwise.
        """
        
        terminal=False

        if self.dynamic: 
            queue=[p for p in self.places.values() if p.uid in self.filter_nodes("job")]
            terminal = all(len(p.token_container)==0 for p in queue)
            
        else:
            
            #check that all operation originally in queue are delivered 
            output_ = [p for p in self.places.values() if p.uid in self.filter_nodes("finished_ops")]
            to_deliver=[0]*self.n_machines 
            for job in self.instance :
                for op in job:
                    to_deliver[op]+=1
                    

            delivered = [len(out.token_container) for out in output_]
            terminal= all(to_deliver[i] <= delivered[i] for i in range(self.n_machines))
            
        return  terminal
    

    def action_mapping(self, n_machines, n_jobs):
        """
        Maps multidiscrete actions to a more versatile Descrite format to use with exp DQN.

        Parameters:
            n_machines (int): Number of machines.
            n_jobs (int): Number of jobs.

        Returns:
            dict: Mapping dictionary.
        """
        tuples = []
        mapping_dict = {}

        for machine in range(n_machines):
            for job in range(n_jobs):
                tuple_entry = (machine, job)
                tuples.append(tuple_entry)
                # Create an inverse mapping from the index to the tuple
                index = len(tuples) - 1
                mapping_dict[index] = tuple_entry

        idle = {len(mapping_dict.keys()): (n_machines,-1)}
        mapping_dict.update(idle)

        return mapping_dict
    
    
    def enabled_allocations(self):
        """
        Determine the enabled allocations based on the current state of the Petri net.
    
        Returns:
            list: A list indicating which allocations are enabled. True for enabled, False otherwise.
        """
        allocate_transitions = [t for t in self.transitions.values() if t.uid in self.filter_nodes("allocate")]
        jobs_queue=[p for p in self.places.values() if p.uid in self.filter_nodes("job")]
        
        enabled_mask = [False] * len (self.action_map.keys()) 
        for key,action in  self.action_map.items():
   
            idle =True 
            job_op=jobs_queue[action[1]]
            allocation =  allocate_transitions[action[0]]
            machine = allocation.children[0]
            
            if len (machine.token_container)>0:
                idle =False
              
            if len (job_op.token_container)>0 :
                operation_color =job_op.token_container[0].color[1]
                if machine.color==operation_color and  idle :
                    enabled_mask[key]=True
             
        # idles transition is always enabled      
        enabled_mask[-1]=True
        
        #filtered_actions = [value for value, mask in zip(self.action_map.values(), enabled_mask) if mask]
     
        return  enabled_mask 

    def interact(self, action):
        """
        Performs Petri net interactions and updates internal state.

        Parameters:
            gui: User interface (if available).
            action: Action to be performed.

        Returns:
            predited  makespan or other objectif.
        """
        
        before = self.projected_makespan()
        self.fire_timed()
        self.fire_colored(action)
        self.time_tick(action)
        # Only the idle is enabled (no action available)
       
        while sum(self.enabled_allocations()) == 1:
            self.fire_timed()
            self.time_tick( action)
            if self.is_terminal():
                break

        after = self.projected_makespan()

        return before - after

    
if __name__ == "__main__":
    sim = JSSPSimulator("ta01",True)
    

 