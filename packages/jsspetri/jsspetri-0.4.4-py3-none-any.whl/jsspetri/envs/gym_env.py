import numpy as np
from gymnasium import Env
from gymnasium import spaces


from jsspetri.envs.petri_simulator import JSSPSimulator
from jsspetri.render.solution_plot import plot_solution


class JsspetriEnv(Env):
    """
    Custom Gym environment for Job Shop Scheduling using a Petri net simulator.
    """
    metadata = {"render_modes": ["solution"]}

    def __init__(self, render_mode=None, instance_id="ta01",flexible=False,dynamic=False,observation_depth=1):
        """
        Initializes the JsspetriEnv.
        if the JSSP is flexible a maximum number of machines and jobs if predefined regardless le instance size 

        Parameters:
            render_mode (str): Rendering mode ("human" or "solution").
            instance_id (str): Identifier for the JSSP instance.
            observation_depth (int): Depth of observations in future.
        """

        self.instance_id=instance_id
        self.flexible=flexible
        self.dynamic=dynamic
        self.sim = JSSPSimulator(self.instance_id,self.flexible,self.dynamic)
        self.observation_depth = min(observation_depth, self.sim.n_machines)
        
        if self.flexible :
            observation_size= 3 * self.sim.max_nmachines + 2 * (self.sim.max_njobs * self.observation_depth) 
            actions_size = self.sim.max_nmachines*self.sim.max_njobs+1 
                
        else :   
            observation_size= 3 * self.sim.n_machines + 2 * (self.sim.n_jobs * self.observation_depth)  
            actions_size= self.sim.n_machines * self.sim.n_jobs + 1
            

        self.observation_space= spaces.Box(low=-1, high=self.sim.max_bound,shape=(observation_size,),dtype=np.int64)
        self.action_space = spaces.Discrete(actions_size)   
      
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode


    def _get_obs(self):

        """
        Get the observation of the state.

        Returns:
            np.ndarray: Observation array.
        """
 
        observation = []
        job_places = [p for p in self.sim.places.values() if p.uid in self.sim.filter_nodes("job")]
        machine_places = [p for p in self.sim.places.values() if p.uid in self.sim.filter_nodes("machine")]
        finished_places = [p for p in self.sim.places.values() if p.uid in self.sim.filter_nodes("finished_ops")]
       
        # Get the state of the machines, i.e., remaining time if not idle:

        for m in range(self.sim.n_machines) :
           if len ( machine_places[m].token_container) == 0:
               observation.extend([machine_places[m].color,0])
           else:
               in_process=machine_places[m].token_container[0]
               remaining_time =in_process.process_time - in_process.logging[list(in_process.logging.keys())[-1]][2]
               observation.extend([machine_places[m].color, remaining_time if remaining_time  >=0  else 0])
               
        # Get the waiting operation in the jobs depending on the depth:
        for level in range(self.observation_depth):
           for j in range(self.sim.n_jobs) :
               if job_places[j].token_container and level < len(job_places[j].token_container):
                   observation.extend([job_places[j].token_container[level].color[1], job_places[j].token_container[level].process_time])
               else:
                   observation.extend([0, 0])
                                
        # Get the number of deliverd operation 
        for delivery in finished_places:
           observation.append(len ( delivery.token_container))
           
           
       #   if flexible fill the rest of the observation with -1   
        if self.sim.flexible :
            for  i in range(len(observation),self.observation_space.shape[0]):  
               observation.append(-1)
               
        return np.array(observation, dtype=np.int64)

    def reset(self, seed=None, options=None):
        """
        Reset the environment.

        Returns:
            tuple: Initial observation and info.
        """
        self.sim.petri_reset()
        observation = self._get_obs()
        info = self._get_info(0, False)

        return observation, info

    def reward(self, advantage):
        """
        Calculate the reward.

        Parameters:
            advantage: Advantage given by the interaction.
        Returns:
            Any: Calculated reward .
        """
        reward=advantage
        
        return reward

    def action_masks(self):
        """
        Get the action masks.

        Returns:
            list: List of enabled actions.
        """
        enabled_mask = self.sim.enabled_allocations()
        return enabled_mask

    def step(self, action):
        """
        Take a step in the environment.

        Parameters:
            action: Action to be performed.
        Returns:
            tuple: New observation, reward, termination status, info.
        """

        advantage = self.sim.interact(action)   
        reward = self.reward(advantage)
        observation = self._get_obs()
        terminated = self.sim.is_terminal()
        info = self._get_info(reward, terminated)
        

        return observation, reward, terminated, False, info

    def render(self):
        """
        Render the environment.
        """
        if self.render_mode == "solution":
            plot_solution(self.sim)
       

    def close(self):
        """
        Close the environment.
        """
        if self.metadata["render_modes"] == "human":
            self.gui.on_window_close()

    def _get_info(self, reward, terminated):
        """
        Get information dictionary.

        Parameters:
            reward: Current reward.
            terminated (bool): Termination status.

        Returns:
            dict: Information dictionary.
        """
        return {"Reward": reward, "Terminated": terminated}

if __name__ == "__main__":
    
    pass
