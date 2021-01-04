import argparse
import random
from environment import TreasureCube
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class QLearningAgent(object):
    def __init__(self, environment, epsilon=0.01, alpha=0.5, gamma=0.99):
        self.environment = environment
        self.action_space = ['left','right','forward','backward','up','down'] # in TreasureCube

        # INITIALISING THE Q_TABLE
        
        self.q_table = dict() # Store all Q-values in dictionary of dictionaries
        
        for x in range(4): # Loop through all possible grid spaces, create sub-dictionary for each
            for y in range(4):
                for z in range(4):
                    self.q_table[(x,y,z)] = {'left':0,'right':0,'forward':0,'backward':0,'up':0,'down':0}
                    #Initialise with zero values for possible moves
      
        #Initialize all parameters
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
      
    def take_action(self, state):
        # Returns either the optimal action which will maximise the reward,
        # or a random exploratory action.
        # The above choice depends on the value of epsilon

        if np.random.uniform(0,1) < self.epsilon:
            action = self.action_space[np.random.randint(0, len(self.action_space))]
            
        else:
            qValues = self.q_table[self.environment.curr_pos]
            maxValue = max(qValues.values())
            action = np.random.choice([k for k, v in qValues.items() if v == maxValue])

        return action

    def train(self, state, action, next_state, reward):
        #Updates the Q-value table using Q-learning
        
        qValues = self.q_table[next_state]
        max_q_value = max(qValues.values())
        current_q_value = self.q_table[state][action]
        
        self.q_table[state][action] = current_q_value + self.alpha * (reward + self.gamma * max_q_value - current_q_value)

def test_cube(max_episode, max_step, q_plot, q_table_output, rendEnv_output, epiSummary):
    env = TreasureCube(max_step=max_step)
    agent = QLearningAgent(env)
    reward_per_episode = []
    totalSteps=0
    totalRewards=0
    
    for epsisode_num in range(0, max_episode):
        state = env.reset()
        terminate = False
        t=0
        episode_reward = 0
        while not terminate:
            state = env.curr_pos
            action = agent.take_action(state)
            reward, terminate, next_state = env.step(action)
            next_state = env.curr_pos

            if (rendEnv_output==True):
                env.render() 
                print(f'step: {t}, action: {action}, reward: {reward}')
            t += 1
            
            #Updating the Q values
            agent.train(state, action, next_state, reward)
            state = next_state
            episode_reward += reward
            
        reward_per_episode.append(episode_reward)
        if epiSummary==True:
            print(f'epsisode: {epsisode_num}, total_steps: {t} episode reward: {episode_reward}')

        totalSteps+=t
        
    for r in range(len(reward_per_episode)):
        totalRewards += reward_per_episode[r]
        
    print("Average steps per episode=", totalSteps/(max_episode))
    print("Average rewards per episode=", totalRewards/(max_episode))

    if (q_table_output==True):
        qTableOutput(agent.q_table)

    if (q_plot==True):
        plt.plot(reward_per_episode)
        plt.ylabel('Reward per episode')
        plt.xlabel('Episode')
        plt.show()

import csv
def qTableOutput(d):
    df = pd.DataFrame(d.items(), columns=["state", "action"])
    action = df["action"].apply(pd.Series)

    frames = [df, action]
    results = pd.concat(frames, axis=1)
    results = results.drop(results.columns[1], axis=1)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(results)

    # Uncomment the following line if you want to save a csv
    #pd.DataFrame(results).to_csv("qTable.csv")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--max_episode', type=int, default=500,         help = 'Specify the maximum episodes eg. --max_episode 10')
    parser.add_argument('--max_step', type=int, default=500,            help = 'Specify the maximum steps eg. --max_step 10')
    parser.add_argument('--q_plot', type=bool, default=False,           help = 'Specify True if you want to see the trainning plot eg. --q_table_output True')
    parser.add_argument('--q_table_output', type=bool, default=False,   help = 'Specify True if you want to see the final q table eg. --q_plot True')
    parser.add_argument('--rendEnv_output', type=bool, default=False,   help = 'Specify True if you want to see the rendered environment output eg. --rendEnv_output True')
    parser.add_argument('--epiSummary', type=bool, default=False,       help = 'Specify True if you want to see statistics summary for each episode eg. --epiSummary True')
    
    args = parser.parse_args()

    test_cube(args.max_episode, args.max_step, args.q_plot, args.q_table_output, args.rendEnv_output, args.epiSummary)
