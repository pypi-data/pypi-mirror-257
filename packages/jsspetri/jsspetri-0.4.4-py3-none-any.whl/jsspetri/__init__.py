from gymnasium.envs.registration import register

register(
     id="Jsspetri",
     entry_point="jsspetri.envs.gym_env:JsspetriEnv",
     nondeterministic=False,   
)




