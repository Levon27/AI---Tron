from gym.envs.registration import register

# passar o 'id' para o openai gym no código principal
register(
    id='tron-v0',
    entry_point='gym_tron.envs:TronEnv',
)