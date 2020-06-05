def run_exp_hist(random_agent, agent, env, nb_steps_history, nb_steps, env_seed):
    """
    Run an experiment for an agent with an history made by a random agent.
    Arguments
    ---------
    random_agent: RandomAgent
        the random agent.
    agent: Agent
        the agent.
    env: Environment
        the environment.
    nb_steps_history: int
        number of steps for the history.
    nb_steps: int
        number of steps for the experiment.
    action_size: int
        the action size.
    env_seed: int
        seed for the rng of the environment.
    Return
    -------
    dict
        the results of the experiment.
    """
    history = np.zeros((nb_steps_history, 4))
    rewards = np.zeros((nb_steps))
    regrets = np.zeros((nb_steps))
    actions = np.zeros((nb_steps))

    contexts_hist = []
    rewards_hist = np.zeros((nb_steps_history))
    actions_hist = np.zeros((nb_steps_history))

    actions = env.reset(env_seed)

    for i in range(nb_steps_history):
        # Select action from agent policy.
        action = random_agent.act(actions)
        
        # Play action in the environment and get reward.
        next_context, reward, best_reward = env.step(action)
        
        # Update history
        rewards_hist[i] = reward
        actions_hist[i] = action
        clicks_hist[i]  = click
        contexts_hist   += [context]
        
        # Update agent.
        random_agent.update(context, action, reward)
        context = next_context
        
    agent.train_agent(contexts_hist, actions_hist, rewards_hist, clicks_hist)
    
    for i in range(nb_steps):
        # Select action from agent policy.
        action = agent.act(context)
        
        # Play action in the environment and get reward.
        next_context, reward, click, best_reward  = env.step(action)

        
        # Update agent.
        agent.update(context, action, reward)
        context = next_context
        
        # Save history.
        #context[i] = context
        rewards[i] = reward
        actions[i] = action
        regrets[i] = best_reward - reward


    reward = rewards[:, 0].sum()
    regret = np.sum(regrets, axis = 0)

    return {'reward': reward, 
            'regret': regret,
            'rewards': rewards,
            'regrets': regrets,
            'actions': actions,
            'cum_rewards': np.cumsum(rewards, axis = 0), 
            'cum_regrets': np.cumsum(regrets, axis = 0),
            }